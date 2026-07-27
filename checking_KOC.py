import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
# ... các import khác
# Setting API
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
sys.path.append(os.path.abspath("."))

######## FUNCTONS ##########
try:
    creds_info = st.secrets["google"]

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_info, scope
    )

    client = gspread.authorize(credentials)

    st.success("🔐 Đã đăng nhập và kết nối Google Sheets API thành công!")

except Exception as e:

    st.error(f"❌ Lỗi khi kết nối Google Sheets API: {e}")


def clean_value(x):
    if pd.isna(x):
        return ""
    elif isinstance(x, (int, float)):
        return x  # giữ nguyên kiểu số
    elif isinstance(x, str):
        return x.replace("'", "''")  # escape dấu nháy đơn nếu có
    else:
        return str(x)


def read_file_checking_tt(file_obj):

    dtype_dict = {
        "Order ID": str,
        "Product ID": str,
        "Content ID": str,
        "SKU ID": str,
        "Tracking ID": str,
        "Package ID": str,
    }

    file_name = file_obj.name.lower()

    if file_name.endswith(".csv"):
        df = pd.read_csv(file_obj, dtype=dtype_dict)

    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(file_obj, dtype=dtype_dict)

    else:
        raise ValueError(
            "Unsupported file format. Please upload CSV or XLSX.")

    return df


def process_checking_data(df):
    checking_df = df.copy()

    checking_df["Time Created"] = (
        pd.to_datetime(
            checking_df["Time Created"],
            errors="coerce"
        ).dt.strftime("%d/%m/%Y")
    )

    checking_df_video = checking_df[(checking_df["Content Type"] == "Video") & (
        checking_df["Order Status"] != "Cancelled")]

    return checking_df_video


def read_file_tracking_sp(file_obj):
    df = pd.read_excel(file_obj)
    return df


def run(platform: str):

    if platform == "TikTok":

        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h1 style="
                font-size:38px;
                font-weight:800;
                color:#111;
                margin-bottom:5px;
            ">
                📑 Daily Checking KOC Tiktok
            </h1>
            <p style="
                color:#6B7280;
                font-size:15px;
                margin-top:0;
            ">
                Tracking weekly revenue, orders, ads performance and livestream efficiency
            </p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.sidebar.file_uploader(
            "Upload TikTok File (CSV/XLSX)",
            type=["csv", "xlsx"],
            key="file_upload_sidebar",
        )

        if uploaded_file:
            st.sidebar.success(f"{uploaded_file.name} uploaded!")

            if st.sidebar.button("Check GMV Now"):
                try:
                    df = read_file_checking_tt(uploaded_file)
                    st.session_state.df = df
                except Exception as e:
                    st.sidebar.error(f"Cannot read file: {e}")

        if "df" in st.session_state:

            df = st.session_state["df"].copy()
            result_box = st.empty()
            df.rename(
                columns={
                    "Est. Commission Base": "GMV",
                    "Est. standard commission payment": "Commission"
                },
                inplace=True
            )

            df_view = df[
                [
                    "Time Created",
                    "Order ID",
                    "Creator Username",
                    "GMV",
                    "Commission",
                    "Seller SKU",
                    "Content Type",
                    "Content ID",
                    "Order Status"
                ]
            ]

            tracking_df = process_checking_data(df_view)

            # Chọn KOC
            creator_list = sorted(
                tracking_df["Creator Username"].dropna().unique()
            )

            selected_creators = st.multiselect(
                "Chọn KOC",
                options=creator_list,
                default=creator_list
            )

            # Lọc KOC
            if selected_creators:
                df_final = tracking_df[
                    tracking_df["Creator Username"].isin(selected_creators)
                ]
            else:
                df_final = tracking_df.copy()

            # Tổng hợp theo ngày + Creator + Content
            summary_df = (
                df_final.groupby(
                    [
                        "Time Created",
                        "Creator Username",
                        "Content Type",
                        "Content ID",
                    ],
                    as_index=False
                )
                .agg(
                    Orders=("Order ID", "nunique"),
                    GMV=("GMV", "sum"),
                    Commission=("Commission", "sum"),
                )
                .sort_values(
                    ["Time Created", "Creator Username"],
                    ascending=[False, True]
                )
            )

            st.dataframe(summary_df, use_container_width=True)

            fill_ggsheet = df_final
            st.session_state["fill_ggsheet"] = (fill_ggsheet)

            if st.button("📤 Ghi dữ liệu doanh thu vào Google Sheet"):
                with result_box:
                    with st.spinner("⏳ Đang ghi dữ liệu..."):
                        spreadsheet = client.open_by_url(
                            "https://docs.google.com/spreadsheets/d/1U2jeDMar2RgqwX3yMGv1C4aESvTdP3fAq8wPVW4NWuE/edit?usp=sharing"
                        )
                        worksheet = spreadsheet.worksheet("Tiktok")
                        existing_data = worksheet.get_all_values()
                        next_row_index = None
                        for i in range(1, len(existing_data)):
                            if all(cell.strip() == "" for cell in existing_data[i]):
                                next_row_index = i + 1
                                break
                        if next_row_index is None:
                            next_row_index = len(existing_data) + 1

                        from gspread_dataframe import set_with_dataframe
                        df_to_write = pd.DataFrame([{
                            col: clean_value(val)
                            for col, val in zip(
                                st.session_state["fill_ggsheet"].columns,
                                st.session_state["fill_ggsheet"].iloc[0]
                            )
                        }])

                        set_with_dataframe(
                            worksheet, df_to_write,
                            row=next_row_index,
                            include_column_header=False
                        )

                with result_box:
                    st.success("✅ Dữ liệu đã được ghi vào Google Sheet!")

    elif platform == "Shopee":

        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h1 style="
                font-size:38px;
                font-weight:800;
                color:#111;
                margin-bottom:5px;
            ">
                📑 Daily Tracking Shopee
            </h1>
            <p style="
                color:#6B7280;
                font-size:15px;
                margin-top:0;
            ">
                Tracking weekly revenue, orders, ads performance and livestream efficiency
            </p>
        </div>
        """, unsafe_allow_html=True)

        # uploaded_file_sp = st.sidebar.file_uploader(
        #     "Upload File Shopee (XLSX) At Here", type="xlsx", key="xlsx_upload_sidebar"
        # )

        # if uploaded_file_sp:
        #     st.sidebar.success("File Uploaded!")
        #     if st.sidebar.button("Check GMV Now"):
        #         df_sp = read_file_tracking_sp(uploaded_file_sp)
        #         st.session_state.df_sp = df_sp

        # if "df_sp" in st.session_state:
        #     df_sp = st.session_state["df_sp"].copy()
        #     result_box = st.empty()
        #     tracking_dfsp_view = df_sp[
        #         [
        #             "Ngày",
        #             "Tổng số đơn hàng",
        #             "Tổng doanh số (VND)",
        #             "Doanh số đơn hủy",
        #             "Tỷ lệ chuyển đổi đơn hàng",
        #             "Doanh số trên mỗi đơn hàng",
        #             "Số lượt truy cập",
        #             "Lượt nhấp vào sản phẩm",
        #             "số người mua",
        #             "số người mua mới",
        #             "số người mua tiềm năng",
        #             "Tỉ lệ quay lại của người mua"
        #         ]
        #     ]
        #     tracking_dfsp_view["Ngày"] = tracking_dfsp_view["Ngày"].str[:10]

        #     df_final_sp = tracking_dfsp_view.iloc[[0]].copy()
        #     st.dataframe(df_final_sp, width='stretch')
        #     fill_ggsheet_sp = df_final_sp
        #     st.session_state["fill_ggsheet_sp"] = (fill_ggsheet_sp)

        #     if st.button("📤 Ghi dữ liệu doanh thu vào Google Sheet"):
        #         with result_box:
        #             with st.spinner("⏳ Đang ghi dữ liệu..."):
        #                 spreadsheet = client.open_by_url(
        #                     "https://docs.google.com/spreadsheets/d/1U2jeDMar2RgqwX3yMGv1C4aESvTdP3fAq8wPVW4NWuE/edit?usp=sharing"
        #                 )
        #                 worksheet_sp = spreadsheet.worksheet("Shopee")
        #                 existing_data_sp = worksheet_sp.get_all_values()
        #                 next_row_index = None
        #                 for i in range(1, len(existing_data_sp)):
        #                     if all(cell.strip() == "" for cell in existing_data_sp[i]):
        #                         next_row_index = i + 1
        #                         break
        #                 if next_row_index is None:
        #                     next_row_index = len(existing_data_sp) + 1

        #                 from gspread_dataframe import set_with_dataframe
        #                 df_to_write = pd.DataFrame([{
        #                     col: clean_value(val)
        #                     for col, val in zip(
        #                         st.session_state["fill_ggsheet_sp"].columns,
        #                         st.session_state["fill_ggsheet_sp"].iloc[0]
        #                     )
        #                 }])

        #                 set_with_dataframe(
        #                     worksheet_sp, df_to_write,
        #                     row=next_row_index,
        #                     include_column_header=False
        #                 )

        #         with result_box:
        #             st.success("✅ Dữ liệu đã được ghi vào Google Sheet!")
