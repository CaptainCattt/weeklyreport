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


def read_file_tracking_tt(file_obj):

    file_name = file_obj.name.lower()

    if file_name.endswith(".csv"):
        # Đọc A1
        cell = pd.read_csv(
            file_obj,
            header=None,
            nrows=1,
            encoding="utf-8-sig"
        ).iloc[0, 0]

        date = str(cell).split(": ")[1].split("-")[0]

        # Đưa con trỏ về đầu file
        file_obj.seek(0)

        # Đọc dữ liệu
        df = pd.read_csv(
            file_obj,
            header=2,
            encoding="utf-8-sig"
        )

    elif file_name.endswith(".xlsx"):
        # Đọc A1
        cell = pd.read_excel(
            file_obj,
            header=None,
            nrows=1
        ).iloc[0, 0]

        date = str(cell).split(": ")[1].split("-")[0]

        # Đưa con trỏ về đầu file
        file_obj.seek(0)

        # Đọc dữ liệu
        df = pd.read_excel(
            file_obj,
            header=2
        )

    else:
        raise ValueError(
            "Unsupported file format. Please upload CSV or XLSX."
        )

    # Bỏ cột đầu tiên nếu là cột thừa
    df = df.iloc[:, 1:].copy()

    return df, date


def process_tracking_data(df):
    tracking_df = df
    tracking_df["Conversion rate"] = pd.to_numeric(
        tracking_df["Conversion rate"],
        errors="coerce"
    ).round(4)
    return tracking_df


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
                📑 Daily Tracking
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
                    df, date = read_file_tracking_tt(uploaded_file)
                    st.session_state.df = df
                    st.session_state.date = date
                except Exception as e:
                    st.sidebar.error(f"Cannot read file: {e}")

        if "df" in st.session_state:

            df = st.session_state["df"].copy()
            date = st.session_state["date"]
            result_box = st.empty()
            tracking_df = process_tracking_data(df)

            tracking_df_view = tracking_df[
                [
                    "Orders",
                    "GMV",
                    "Page views",
                    "Conversion rate",
                    "AOV",
                    "Product impressions",
                    "Unique product impressions",
                    "Product clicks",
                    "Unique clicks",
                    "Visitors",
                    "Creator LIVE-attributed GMV",
                    "Linked account LIVE-attributed GMV",
                    "Creator video-attributed GMV",
                    "Linked account video-attributed GMV"
                ]
            ]

            df_final = tracking_df_view.iloc[[0]].copy()

            df_final.insert(0, "Date", date)

            st.dataframe(df_final, use_container_width=True)

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
        <div style="
            font-size: 16px;
            font-weight: 400;
            padding-left: 12px;
            margin-bottom: 12px;
        ">
            Dữ liệu traffic từ Shopee
        </div>
        """, unsafe_allow_html=True)
