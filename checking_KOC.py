from google_sheets import GOOGLE_SHEETS
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


def read_file_video_tt(file_obj):
    dtype_dict = {
        "Video ID": str,
        "Creator name": str,
    }
    file_name = file_obj.name.lower()

    if file_name.endswith(".csv"):
        # bỏ dòng thứ 2 của file
        df = pd.read_csv(file_obj, skiprows=[1], dtype=dtype_dict)

    elif file_name.endswith(".xlsx"):
        # bỏ dòng thứ 2 của file
        df = pd.read_excel(file_obj, skiprows=[1], dtype=dtype_dict)

    else:
        raise ValueError("Unsupported file format. Please upload CSV or XLSX.")

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

        video_file = st.sidebar.file_uploader(
            "Upload TikTok Video File (CSV/XLSX)",
            type=["csv", "xlsx"],
            key="video_file_upload_sidebar",
        )

        if uploaded_file and video_file:
            st.sidebar.success(
                f"{uploaded_file.name} uploaded! and {video_file.name} uploaded!")

            if st.sidebar.button("Check Now"):
                try:
                    df = read_file_checking_tt(uploaded_file)
                    video_df = read_file_video_tt(video_file)
                    st.session_state.df = df
                    st.session_state.video_df = video_df
                except Exception as e:
                    st.sidebar.error(f"Cannot read file: {e}")

        if "df" in st.session_state and "video_df" in st.session_state:

            df = st.session_state["df"].copy()
            video_df = st.session_state["video_df"].copy()
            result_box = st.empty()

            # =========================================================
            # 1. CLEAN ORDER DATA
            # =========================================================
            df["Time Created"] = pd.to_datetime(
                df["Time Created"].astype(str).str.strip(),
                dayfirst=True,
                errors="coerce"
            )
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
                    "Content Type",
                    "Content ID",
                    "Order Status"
                ]
            ].copy()

            tracking_df = process_checking_data(df_view)

            # =========================================================
            # 2. CLEAN VIDEO DATA
            # =========================================================

            video_df = video_df[
                [
                    "Video ID",
                    "Creator name",
                    "Affiliate video-attributed GMV",
                    "Video-attributed orders",
                    "AOV",
                    "Likes",
                    "Comments",
                    "Shares",
                    "Video product impressions",
                    "Video product clicks",
                    "Completion rate",
                    "Video views",
                    "CTR",
                    "Video GPM",
                    "Engagement",
                    "Avg. GMV per customer"
                ]
            ].copy()

            # =========================================================
            # 3. CHUẨN HÓA DATA TYPE
            # =========================================================

            tracking_df["Content ID"] = (
                tracking_df["Content ID"]
                .astype(str)
                .str.strip()
            )

            tracking_df["Creator Username"] = (
                tracking_df["Creator Username"]
                .astype(str)
                .str.strip()
            )

            video_df["Video ID"] = (
                video_df["Video ID"]
                .astype(str)
                .str.strip()
            )

            video_df["Creator name"] = (
                video_df["Creator name"]
                .astype(str)
                .str.strip()
            )

            # =========================================================
            # 4. TỔNG HỢP ORDER
            # =========================================================

            summary_df = (
                tracking_df
                .groupby(
                    [
                        "Time Created",
                        "Creator Username",
                        "Content Type",
                        "Content ID"
                    ],
                    as_index=False
                )
                .agg(
                    Orders=("Order ID", "nunique"),
                    GMV=("GMV", "sum"),
                    Commission=("Commission", "sum")
                )
            )

            # =========================================================
            # 5. MERGE ORDER + VIDEO
            # =========================================================
            #
            # Dùng LEFT JOIN thay vì OUTER
            # vì summary_df là bảng chính.
            #
            # Mỗi dòng = 1 ngày + 1 creator + 1 content
            #

            df_merged = pd.merge(
                summary_df,
                video_df,
                left_on=[
                    "Content ID",
                    "Creator Username"
                ],
                right_on=[
                    "Video ID",
                    "Creator name"
                ],
                how="right"
            )

            # =========================================================
            # 6. CHỌN KOC
            # =========================================================

            creator_list = sorted(
                df_merged["Creator name"]
                .dropna()
                .unique()
            )

            selected_creators = st.multiselect(
                "Chọn KOC",
                options=creator_list,
                default=creator_list
            )

            # =========================================================
            # 7. FILTER SAU KHI MERGE
            # =========================================================

            if selected_creators:

                df_merged_final = df_merged[
                    df_merged["Creator name"].isin(selected_creators)
                ].copy()

            else:

                df_merged_final = df_merged.copy()

            # =========================================================
            # 8. SELECT COLUMN HIỂN THỊ
            # =========================================================

            df_merged_final = df_merged_final[[
                "Time Created",
                "Creator Username",
                "Content Type",
                "Content ID",
                "Orders",
                "GMV",
                "Commission",
                "Creator name",
                "AOV",
                "Likes",
                "Comments",
                "Shares",
                "Video product impressions",
                "Video product clicks",
                "Completion rate",
                "Video views",
                "CTR",
                "Video GPM",
                "Engagement",
            ]]

            # =========================================================
            # 10. DISPLAY
            # =========================================================

            st.dataframe(
                df_merged_final,
                use_container_width=True,
                hide_index=True
            )

            st.session_state["fill_ggsheet"] = df_merged_final.copy()

            if st.button("📤 Ghi dữ liệu doanh thu vào Google Sheet"):
                with result_box:
                    with st.spinner("⏳ Đang ghi dữ liệu..."):
                        spreadsheet = client.open_by_url(GOOGLE_SHEETS)
                        worksheet = spreadsheet.worksheet(
                            "7. Tracking Booking KOC")

                        # Dòng tiếp theo để ghi
                        next_row_index = len(worksheet.get_all_values()) + 1

                        from gspread_dataframe import set_with_dataframe

                        df_to_write = st.session_state["fill_ggsheet"].copy()

                        # Làm sạch dữ liệu
                        df_to_write = df_to_write.map(clean_value)

                        set_with_dataframe(
                            worksheet,
                            df_to_write,
                            row=next_row_index,
                            include_column_header=False,
                            resize=False,
                        )

                with result_box:
                    st.success(
                        f"✅ Đã ghi {len(df_to_write)} dòng vào Google Sheet!")

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
