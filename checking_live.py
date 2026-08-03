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


def clean_value(x):
    if pd.isna(x):
        return ""
    elif isinstance(x, (int, float)):
        return x  # giữ nguyên kiểu số
    elif isinstance(x, str):
        return x.replace("'", "''")  # escape dấu nháy đơn nếu có
    else:
        return str(x)


def read_file_aff_tt(file_obj):

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

    checking_df_live = checking_df[(checking_df["Content Type"] == "Livestream") & (
        checking_df["Order Status"] != "Ineligible")]

    return checking_df_live


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
                📑 Daily Checking LIVESTREAM Tiktok
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
            st.sidebar.success(
                f"{uploaded_file.name} uploaded!")

            if st.sidebar.button("Check Now"):
                try:
                    df = read_file_aff_tt(uploaded_file)
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
            st.markdown("""
            <style>

            /* Background của metric */
            div[data-testid="stMetric"]{
                background: linear-gradient(135deg,#ffffff 0%,#f8fbff 100%);
                border: 1px solid rgba(0,0,0,0.06);
                border-radius:20px;
                padding:22px 15px;
                box-shadow:
                    0 6px 20px rgba(0,0,0,.08),
                    inset 0 1px 0 rgba(255,255,255,.7);
                transition:all .3s ease;
                position:relative;
                overflow:hidden;
                min-height:120px;
            }

            /* Thanh màu phía trên */
            div[data-testid="stMetric"]::before{
                content:"";
                position:absolute;
                left:0;
                top:0;
                width:100%;
                height:5px;
                background:linear-gradient(
                    90deg,
                    #2563eb,
                    #06b6d4,
                    #10b981
                );
            }

            /* Hover */
            div[data-testid="stMetric"]:hover{
                transform:translateY(-8px) scale(1.02);
                box-shadow:
                    0 14px 35px rgba(37,99,235,.18);
            }

            /* Label */
            div[data-testid="stMetricLabel"]{
                justify-content:center;
            }

            div[data-testid="stMetricLabel"] p{
                font-size:15px;
                font-weight:600;
                color:#6b7280;
                letter-spacing:.4px;
            }

            /* Value */
            div[data-testid="stMetricValue"]{
                justify-content:center;
            }

            div[data-testid="stMetricValue"] p{
                font-size:36px;
                font-weight:800;

                background:linear-gradient(
                    90deg,
                    #2563eb,
                    #06b6d4
                );

                -webkit-background-clip:text;
                -webkit-text-fill-color:transparent;
            }

            /* Delta */
            div[data-testid="stMetricDelta"]{
                justify-content:center;
                font-weight:700;
            }

            /* Khoảng cách giữa các card */
            div[data-testid="column"]{
                padding:4px;
            }

            </style>
            """, unsafe_allow_html=True)
            col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 1, 1, 2])

            col1.metric("📦 Orders", summary_df["Orders"].sum())
            col2.metric(
                "💰 GMV",
                f"{summary_df['GMV'].sum():,.0f}"
            )
            col3.metric(
                "💸 Commission",
                f"{summary_df['Commission'].sum():,.0f}"
            )
            col4.metric(
                "👤 Creators",
                summary_df["Creator Username"].nunique()
            )
            col5.metric(
                "🎬 Contents",
                summary_df["Content ID"].nunique()
            )
            col6.metric(
                "🛒 AOV",
                f"{summary_df['GMV'].sum()/summary_df['Orders'].sum():,.0f}"
            )
            daily = summary_df.groupby("Time Created", as_index=False).agg(
                GMV=("GMV", "sum")
            )

            fig_gmvday = px.line(
                daily,
                x="Time Created",
                y="GMV",
                markers=True
            )

            daily_order = summary_df.groupby("Time Created", as_index=False).agg(
                Orders=("Orders", "sum")
            )

            fig_daily_order = px.bar(
                daily_order,
                x="Time Created",
                y="Orders"
            )

            creator = (
                summary_df
                .groupby("Creator Username", as_index=False)
                .agg(
                    Orders=("Orders", "sum"),
                    GMV=("GMV", "sum"),
                    Commission=("Commission", "sum"),
                    Contents=("Content ID", "nunique")
                )
            )

            creator["AOV"] = creator["GMV"]/creator["Orders"]
            creator["Commission Rate"] = creator["Commission"]/creator["GMV"]

            fig_bubble = px.scatter(
                creator,
                x="Orders",
                y="GMV",
                size="Commission",
                color="Creator Username",
                hover_name="Creator Username"
            )

            st.plotly_chart(fig_gmvday, width='stretch')
            st.plotly_chart(fig_daily_order, width='stretch')
            st.plotly_chart(fig_bubble, width='stretch')

            # st.session_state["fill_ggsheet"] = summary_df.copy()
            # if st.button("📤 Ghi dữ liệu doanh thu vào Google Sheet"):
            #     with result_box:
            #         with st.spinner("⏳ Đang ghi dữ liệu..."):
            #             spreadsheet = client.open_by_url(
            #                 "https://docs.google.com/spreadsheets/d/1U2jeDMar2RgqwX3yMGv1C4aESvTdP3fAq8wPVW4NWuE/edit?usp=sharing"
            #             )
            #             worksheet = spreadsheet.worksheet(
            #                 "7. Tracking Booking KOC")

            #             # Dòng tiếp theo để ghi
            #             next_row_index = len(worksheet.get_all_values()) + 1

            #             from gspread_dataframe import set_with_dataframe

            #             df_to_write = st.session_state["fill_ggsheet"].copy()

            #             # Làm sạch dữ liệu
            #             df_to_write = df_to_write.map(clean_value)

            #             set_with_dataframe(
            #                 worksheet,
            #                 df_to_write,
            #                 row=next_row_index,
            #                 include_column_header=False,
            #                 resize=False,
            #             )

            #     with result_box:
            #         st.success(
            #             f"✅ Đã ghi {len(df_to_write)} dòng vào Google Sheet!")

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
