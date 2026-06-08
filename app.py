import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Weekly Report Dashboard",
    page_icon="📊",
    layout="wide"
)

######## FUNCTONS ##########


def read_file_tiktok(file_obj):
    df = pd.read_csv(file_obj)
    return df


def read_file_shopee(file_obj):
    df = pd.read_excel(file_obj)
    return df


def process_shopee_data(df_all: pd.DataFrame):
    df_all.columns = df_all.columns.str.strip()
    df_all["Actually type"] = df_all["Trạng Thái Đơn Hàng"]
    df_all["Actually type"] = df_all["Actually type"].apply(
        lambda x: (
            "Đơn hàng đã đến User"
            if isinstance(x, str) and "Người mua xác nhận đã nhận được hàng" in x
            else x
        )
    )
    df_all["SKU Category"] = df_all["SKU phân loại hàng"].copy()
    replacements = {
        r"^(COMBO-SC-ANHDUC|COMBO-SC-NGOCTRINH|COMBO-SC-MIX|SC_COMBO_MIX|SC_COMBO_MIX_LIVESTREAM|COMBO-SC_LIVESTREAM|SC_COMBO_MIX_01|MIX_X1\+X2|MIX_X1\+X2_LIVESTREAM)$": "COMBO-SC",
        r"^(SC_X1|X1|X1_LIVESTREAM)$": "SC-450g",
        r"^(SC_X2|X2|X2_LIVESTREAM)$": "SC-x2-450g",
        r"^(SC_COMBO_X1|COMBO-CAYVUA-X1|SC_COMBO_X1_LIVESTREAM|COMBO-SCX1|COMBO-SCX1_LIVESTREAM|COMBO_X1_LIVESTREAM|COMBO_X1)$": "COMBO-SCX1",
        r"^(SC_COMBO_X2|COMBO-SIEUCAY-X2|SC_COMBO_X2_LIVESTREAM|COMBO-SCX2|COMBO-SCX2_LIVESTREAM|COMBO_X2_LIVESTREAM|COMBO_X2)$": "COMBO-SCX2",
        r"^(BTHP-Cay-200gr|BTHP_Cay|BTHP_Cay_LIVESTREAM)$": "BTHP-CAY",
        r"^(BTHP-200gr|BTHP_KhongCay|BTHP_KhongCay_LIVESTREAM)$": "BTHP-0CAY",
        r"^(BTHP_COMBO_MIX|BTHP003_combo_mix|MIX_Cay\+KhongCay|MIX_Cay\+KhongCay_LIVESTREAM)$": "BTHP-COMBO",
        r"^(BTHP_COMBO_KhongCay|BTHP003_combo_kocay|COMBO_BTHP_KhongCay|COMBO_BTHP_KhongCay_LIVESTREAM)$": "BTHP-COMBO-0CAY",
        r"^(BTHP_COMBO_Cay|BTHP003_combo_cay|COMBO_BTHP_Cay|COMBO_BTHP_Cay_LIVESTREAM)$": "BTHP-COMBO-CAY",
        r"^(BTHP-COMBO\+SC_X1|BTHP_COMBO_MIX\+SC_X1|MIX_BTHP\+X1|MIX_BTHP\+X1_LIVESTREAM)$": "MIX_BTHP+X1",
        r"^(BTHP-COMBO\+SC_X2|BTHP_COMBO_MIX\+SC_X2|MIX_BTHP\+X2|MIX_BTHP\+X2_LIVESTREAM)$": "MIX_BTHP+X2",

        r"^(BTHP-2Cay-2KhongCay|MIX_2Cay\+2KhongCay|MIX_2Cay\+2KhongCay_LIVESTREAM)": "COMBO_4BTHP",
        r"^(BTHP-4Hu-KhongCay|4HU_BTHP_KhongCay|4Hu_BTHP_KhongCay|4Hu_BTHP_KhongCay_LIVESTREAM)$": "4BTHP_0CAY",
        r"^(BTHP-4Hu-Cay|4HU_BTHP_Cay|4Hu_BTHP_Cay|4Hu_BTHP_Cay_LIVESTREAM)$": "4BTHP_CAY",
        r"^(ST-SATETOM-X1|SC-SATE-TOM-X1|ST_STT|STT|STT_LIVESTREAM)$": "SATETOM_X1",
        r"^(SC-TIEUCHAY-X1|SC_TCLC|TCLC|TCLC_LIVESTREAM)$": "TIEUCHAY_X1",
        r"^(MIX_STT\+TCLC|MIX_STT\+TCLC_LIVESTREAM)$": "MIX_STT_TCLC",
        r"^(COMBO_STT|COMBO_STT_LIVESTREAM)$": "COMBO_STT",
        r"^(COMBO_TCLC|COMBO_TCLC_LIVESTREAM)$": "COMBO_TCLC",
        # Newadd
        r"^(MIX_X1\+STT|MIX_X1\+STT_LIVESTREAM)$": "MIX_X1_STT",
        r"^(MIX_X2\+STT|MIX_X2\+STT_LIVESTREAM)$": "MIX_X2_STT",
        r"^(MIX_X1\+TCLC|MIX_X1\+TCLC_LIVESTREAM)$": "MIX_X1_TCLC",
        r"^(MIX_X2\+TCLC|MIX_X2\+TCLC_LIVESTREAM)$": "MIX_X2_TCLC",

        # Ao caytedai
        r"^(ClothSet_X1_M)$": "ClothSet_X1_M",
        r"^(ClothSet_X1_L)$": "ClothSet_X1_L",
        r"^(ClothSet_X1_XL)$": "ClothSet_X1_XL",
        r"^(ClothSet_X2_M)$": "ClothSet_X2_M",
        r"^(ClothSet_X2_L)$": "ClothSet_X2_L",
        r"^(ClothSet_X2_XL)$": "ClothSet_X2_XL",

        # Ao Tshirt
        r"^(TShirt_White_M)$": "TShirt_White_M",
        r"^(TShirt_White_L)$": "TShirt_White_L",
        r"^(TShirt_White_XL)$": "TShirt_White_XL",
        r"^(TShirt_Black_M)$": "TShirt_Black_M",
        r"^(TShirt_Black_L)$": "TShirt_Black_L",
        r"^(TShirt_Black_XL)$": "TShirt_Black_XL",

        # San pham moi & combo mới
        r"^(COMBO_X1_200g|COMBO_X1_200g_LIVESTREAM)$": "COMBO_X1_200",
        r"^(COMBO_X2_200g|COMBO_X2_200g_LIVESTREAM)$": "COMBO_X2_200",
        r"^(COMBO_TCLC_200g|COMBO_TCLC_200g_LIVESTREAM)$": "COMBO_TCLC_200",
        r"^(MIX_200g_X1\+X2\+TCLC|MIX_200g_X1\+X2\+TCLC_LIVESTREAM)$": "MIX_X1_X2_TCLC_200",
        r"^(MIX_200g_X1\+X2\+TCLC\+STT|MIX_200g_X1\+X2\+TCLC\+STT_LIVESTREAM)$": "MIX_ALL_200",
        r"^(MIX_200g_X1\+X2|MIX_200g_X1\+X2_LIVESTREAM)$": "MIX_X1_X2_200",
        r"^(MIX_200g_X1\+TCLC|MIX_200g_X1\+TCLC_LIVESTREAM)$": "MIX_X1_TCLC_200",
        r"^(MIX_200g_X2\+TCLC|MIX_200g_X2\+TCLC_LIVESTREAM)$": "MIX_X2_TCLC_200",

    }

    for pattern, replacement in replacements.items():
        df_all["SKU Category"] = df_all["SKU Category"].str.replace(
            pattern, replacement, regex=True
        )

    return df_all


def kpi_shopee(df: pd.DataFrame):

    # Process data
    df_new = process_shopee_data(df)

    # =========================
    # DATE
    # =========================
    df_new["Ngày đặt hàng"] = pd.to_datetime(
        df_new["Ngày đặt hàng"],
        errors="coerce"
    )

    # =========================
    # ISO WEEK
    # =========================
    iso = df_new["Ngày đặt hàng"].dt.isocalendar()

    df_new["week"] = iso.week.astype(int)
    df_new["year"] = iso.year.astype(int)

    # =========================
    # GET UNIQUE WEEKS
    # =========================
    all_weeks = (
        df_new[["year", "week"]]
        .drop_duplicates()
        .sort_values(["year", "week"])
        .reset_index(drop=True)
    )

    # Need at least 2 weeks
    if len(all_weeks) < 2:
        return df_new, pd.DataFrame(), all_weeks

    # =========================
    # THIS WEEK / LAST WEEK
    # =========================

    # Current week
    current = all_weeks.iloc[-1]

    df_this_week = df_new[
        (df_new["week"] == current["week"]) &
        (df_new["year"] == current["year"])
    ].copy()

    # Previous week
    previous = all_weeks.iloc[-2]

    df_last_week = df_new[
        (df_new["week"] == previous["week"]) &
        (df_new["year"] == previous["year"])
    ].copy()

    return df_this_week, df_last_week, current, previous


# =========================
# CUSTOM CSS
# =========================
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #edf0f7;
    }

    .metric-title {
        font-size: 14px;
        color: #7b8190;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
    }

    .metric-growth {
        font-size: 13px;
        font-weight: 600;
        margin-top: 6px;
    }

    .section-card {
        background: white;
        padding: 24px;
        border-radius: 22px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #edf0f7;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 6px;
    }

    .section-subtitle {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .placeholder-chart {
        height: 350px;
        border-radius: 18px;
        background: #f8fafc;
        border: 2px dashed #cbd5e1;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #94a3b8;
        font-size: 18px;
        font-weight: 600;
    }

    .status-good {
        background: #dcfce7;
        color: #166534;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        width: fit-content;
    }

    .status-warning {
        background: #fef3c7;
        color: #92400e;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        width: fit-content;
    }

    .status-bad {
        background: #fee2e2;
        color: #991b1b;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        width: fit-content;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div style="
        font-size: 22px;
        font-weight: 700;
        border-left: 6px solid #4CAF50;
        padding-left: 12px;
        margin-bottom: 10px;
    ">
        🛒 Nền tảng
    </div>
    """, unsafe_allow_html=True)

    # INIT SESSION STATE
    if "platform" not in st.session_state:
        st.session_state.platform = "TikTok"

    # CSS
    st.markdown("""
    <style>
    button[kind="primary"] {
        background-color: #16a34a !important;
        color: white !important;
        border: 2px solid #15803d !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # TikTok
    with col1:
        # CSS
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://img.icons8.com/color/96/tiktok--v1.png" width="70">
            </div>
            """,
            unsafe_allow_html=True
        )
        # Button
        if st.button(
            "TikTok",
            use_container_width=True,
            type="primary" if st.session_state.platform == "TikTok" else "secondary"
        ):
            st.session_state.platform = "TikTok"
            st.rerun()

    # Shopee
    with col2:
        # CSS
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://img.icons8.com/color/96/shopee.png" width="70">
            </div>
            """,
            unsafe_allow_html=True
        )

        # Button
        if st.button(
            "Shopee",
            use_container_width=True,
            type="primary" if st.session_state.platform == "Shopee" else "secondary"
        ):
            st.session_state.platform = "Shopee"
            st.rerun()  # 🔥 FIX

    platform = st.session_state.platform

# =========================
# TIKTOK UI
# =========================
if platform == "TikTok":
    # =========================
    # HEADER
    # =========================
    st.title("📊 Weekly Report Dashboard")
    st.caption(
        "Tracking weekly revenue, orders, ads performance and livestream efficiency")

    # Upload file
    uploaded_file = st.sidebar.file_uploader(
        "Upload File Tiktok (CSV)", type="csv", key="csv_upload_sidebar"
    )

    if uploaded_file:
        st.sidebar.success("CSV Uploaded!")
        if st.sidebar.button("Check GMV Now"):
            df = read_file_tiktok(uploaded_file)

    # =========================
    # KPI SECTION
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Total Revenue</div>
                <div class="metric-value">₫245M</div>
                <div class="metric-growth" style="color:#16a34a;">▲ +12.4%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Total Orders</div>
                <div class="metric-value">3,452</div>
                <div class="metric-growth" style="color:#16a34a;">▲ +8.1%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Ads Cost</div>
                <div class="metric-value">₫52M</div>
                <div class="metric-growth" style="color:#dc2626;">▼ -4.6%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Profit</div>
                <div class="metric-value">₫68M</div>
                <div class="metric-growth" style="color:#16a34a;">▲ +15.2%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =========================
    # CHART SECTION
    # =========================
    left_chart, right_chart = st.columns([2, 1])

    with left_chart:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Revenue Trend</div>
                <div class="section-subtitle">
                    Weekly revenue performance overview
                </div>
                <div class="placeholder-chart">
                    Revenue Line Chart Placeholder
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right_chart:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Platform Share</div>
                <div class="section-subtitle">
                    Distribution by platform
                </div>
                <div class="placeholder-chart">
                    Pie Chart Placeholder
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =========================
    # DATA TABLE SECTION
    # =========================
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Weekly Report Details</div>
            <div class="section-subtitle">
                Detail performance tracking for each campaign and platform
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Dummy Data
    report_df = pd.DataFrame({
        "Week": ["2026-W20", "2026-W20", "2026-W20", "2026-W20"],
        "Platform": ["TikTok Shop", "Shopee", "Livestream", "Affiliate"],
        "Revenue": [120000000, 95000000, 30000000, 15000000],
        "Orders": [1420, 1032, 810, 190],
        "Ads Cost": [25000000, 18000000, 5000000, 3000000],
        "Profit": [32000000, 21500000, 12000000, 4500000],
        "Status": ["Good", "Average", "Excellent", "Low"]
    })

    st.dataframe(
        report_df,
        use_container_width=True,
        height=350
    )

    # =========================
    # PERFORMANCE CARDS
    # =========================
    st.write("")

    st.subheader("🚀 Campaign Performance")

    campaign_col1, campaign_col2, campaign_col3 = st.columns(3)

    with campaign_col1:
        st.markdown(
            """
            <div class="section-card">
                <h4>GMV Max Campaign</h4>
                <p style="color:#6b7280; font-size:14px;">
                    Main ads campaign this week
                </p>
                <hr>
                <p><b>GMV:</b> ₫82M</p>
                <p><b>ROAS:</b> 5.6</p>
                <p><b>Orders:</b> 942</p>
                <div class="status-good">Good Performance</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with campaign_col2:
        st.markdown(
            """
            <div class="section-card">
                <h4>Livestream Session</h4>
                <p style="color:#6b7280; font-size:14px;">
                    Weekly livestream tracking
                </p>
                <hr>
                <p><b>View:</b> 120K</p>
                <p><b>CTOR:</b> 4.8%</p>
                <p><b>GMV:</b> ₫30M</p>
                <div class="status-warning">Average Performance</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with campaign_col3:
        st.markdown(
            """
            <div class="section-card">
                <h4>Affiliate Campaign</h4>
                <p style="color:#6b7280; font-size:14px;">
                    Creator & affiliate performance
                </p>
                <hr>
                <p><b>Revenue:</b> ₫15M</p>
                <p><b>Orders:</b> 190</p>
                <p><b>Commission:</b> ₫3M</p>
                <div class="status-bad">Need Optimization</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # FOOTER
    # =========================
    st.write("")
    st.caption("Built with Streamlit • Weekly Tracking UI Template")

# =========================
# SHOPEE UI
# =========================
elif platform == "Shopee":

    st.title("📈 Shopee Weekly Report")
    st.caption(
        "Tracking weekly revenue, orders, ads performance and livestream efficiency")
    col1_sp, col2_sp, col3_sp, col4_sp = st.columns(4)

    # Upload file
    uploaded_file = st.sidebar.file_uploader(
        "Upload File Shopee (XLSX)", type="xlsx", key="xlsx_upload_sidebar"
    )

    # Upload file ads
    uploaded_file_ads = st.sidebar.file_uploader(
        "Upload File Shopee Ads CSV", type="csv", key="csv_upload_sidebar"
    )

    if uploaded_file and uploaded_file_ads:
        st.sidebar.success("XLSX Uploaded!")

        if st.sidebar.button("Check GMV Now"):
            shoppe_data = read_file_shopee(uploaded_file)
            st.session_state.shoppe_data = shoppe_data
            st.session_state.shoppe_ads_data = pd.read_csv(
                uploaded_file_ads, skiprows=7)

    # Handle logic after file upload
    if "shoppe_data" in st.session_state:
        data_shopee = st.session_state["shoppe_data"]
        df_this_week, df_last_week, current, previous = kpi_shopee(data_shopee)

        # =====================================================
        # GMV - Gross Merchandise Value
        # =====================================================
        gmv_this_week = df_this_week["Tổng số tiền Người mua thanh toán"].sum()
        gmv_last_week = df_last_week["Tổng số tiền Người mua thanh toán"].sum()

        # =====================================================
        # NMV = Net Merchandise Value (Giá trị hàng hóa thuần)
        # =====================================================
        df_valid_this_week = df_this_week[
            df_this_week["Actually type"] != "Đã hủy"
        ]

        nmv_this_week = (
            df_valid_this_week["Tổng số tiền Người mua thanh toán"].sum(
            ) - df_valid_this_week["Mã giảm giá của Shop"].sum()
        )

        df_valid_last_week = df_last_week[
            df_last_week["Actually type"] != "Đã hủy"
        ]

        nmv_last_week = (
            df_valid_last_week["Tổng số tiền Người mua thanh toán"].sum(
            ) - df_valid_last_week["Mã giảm giá của Shop"].sum()
        )

        # =====================================================
        # ORDERS
        # =====================================================
        orders_this_week = (
            df_this_week["Mã đơn hàng"]
            .nunique()
        )
        orders_last_week = (
            df_last_week["Mã đơn hàng"]
            .nunique()
        )

        # =====================================================
        # WOW
        # =====================================================
        wow_gmv = (
            (gmv_this_week - gmv_last_week)
            / gmv_last_week
        ) * 100

        wow_orders = (
            (orders_this_week - orders_last_week)
            / orders_last_week
        ) * 100

        wow_nmv = (
            (nmv_this_week - nmv_last_week)
            / nmv_last_week
        ) * 100

        # CSS
        st.markdown("""
        <style>
        .kpi-card{
            background: linear-gradient(
                135deg,
                #ffffff 0%,
                #f8fafc 100%
            );

            padding: 24px;
            border-radius: 22px;

            border: 1px solid #e2e8f0;

            box-shadow:
                0 4px 20px rgba(0,0,0,0.05);

            transition: all 0.25s ease;

            margin-bottom: 10px;
        }

        .kpi-card:hover{
            transform: translateY(-4px);
            box-shadow:
                0 10px 30px rgba(0,0,0,0.10);
        }

        .kpi-top{
            display:flex;
            align-items:center;
            justify-content:space-between;
        }

        .kpi-icon{
            font-size:32px;
        }

        .kpi-title{
            font-size:15px;
            font-weight:600;
            color:#64748b;

            margin-top:10px;
        }

        .kpi-value{
            font-size:34px;
            font-weight:800;

            margin-top:8px;
            margin-bottom:14px;

            letter-spacing:-1px;
        }

        .metric-tag-green{
            display:inline-block;

            padding:6px 14px;

            border-radius:999px;

            background:#DCFCE7;
            color:#15803d;

            font-size:14px;
            font-weight:700;
        }

        .metric-tag-red{
            display:inline-block;

            padding:6px 14px;

            border-radius:999px;

            background:#FEE2E2;
            color:#DC2626;

            font-size:14px;
            font-weight:700;
        }

        </style>
        """, unsafe_allow_html=True)

        # =====================================================
        # GET WEEK LABEL
        # =====================================================
        current_week = int(current["week"])
        current_year = int(current["year"])
        previous_week = int(previous["week"])
        previous_year = int(previous["year"])

        current_start = (
            df_this_week["Ngày đặt hàng"]
            .min()
            .strftime("%d/%m")
        )

        current_end = (
            df_this_week["Ngày đặt hàng"]
            .max()
            .strftime("%d/%m/%Y")
        )

        previous_start = (
            df_last_week["Ngày đặt hàng"]
            .min()
            .strftime("%d/%m")
        )

        previous_end = (
            df_last_week["Ngày đặt hàng"]
            .max()
            .strftime("%d/%m/%Y")
        )

        # =====================================================
        # SKU GMV
        # =====================================================
        sku_gmv = (
            df_this_week
            .groupby("SKU Category", as_index=False)[
                "Tổng số tiền Người mua thanh toán"
            ]
            .sum()
        )

        sku_gmv = sku_gmv.rename(
            columns={
                "Tổng số tiền Người mua thanh toán": "GMV"
            }
        )

        # =====================================================
        # SKU NMV
        # =====================================================
        sku_nmv = (
            df_valid_this_week
            .groupby("SKU Category", as_index=False)[
                "Tổng số tiền Người mua thanh toán"
            ]
            .sum()
        )

        sku_nmv = sku_nmv.rename(
            columns={
                "Tổng số tiền Người mua thanh toán": "NMV"
            }
        )

        # =====================================================
        # MERGE
        # =====================================================
        sku_metrics = (
            sku_gmv
            .merge(
                sku_nmv,
                on="SKU Category",
                how="left"
            )
            .fillna(0)
            .sort_values(
                "GMV",
                ascending=False
            )
            .head(8)
        )

        # =====================================================
        # Fees platform
        # =====================================================
        df_fees_this_week = df_this_week.drop_duplicates(
            subset=["Mã đơn hàng"])

        df_fees_this_week["Piship"] = 1620

        fees_predicted = (
            df_fees_this_week["Phí cố định"].sum()
            + df_fees_this_week["Phí Dịch Vụ"].sum()
            + df_fees_this_week["Piship"].sum()
            + df_fees_this_week["Phí xử lý giao dịch"].sum()
        )

        # =====================================================
        # HEADER UI - COMPACT VERSION
        # =====================================================
        st.markdown(f"""
        <div style="
            background: linear-gradient(
                135deg,
                #1E3A8A 0%,
                #2563EB 50%,
                #38BDF8 100%
            );
            padding:12px 18px;
            border-radius:18px;
            margin-bottom:18px;
            color:white;
            box-shadow:
                0 6px 20px rgba(37,99,235,0.18);
        ">
            <div style="
                font-size:12px;
                opacity:0.85;
                font-weight:700;
                letter-spacing:1px;
                text-transform:uppercase;
            ">
                📊 Weekly Performance
            </div>
            <div style="
                margin-top:8px;
                display:flex;
                justify-content:space-between;
                align-items:center;
                flex-wrap:wrap;
                gap:10px;
            ">
                <!-- Current Week -->
                <div>
                    <div style="
                        font-size:22px;
                        font-weight:800;
                        line-height:1.1;
                    ">
                        Week {current_week} - {current_year}
                    </div>
                    <div style="
                        font-size:13px;
                        opacity:0.92;
                        margin-top:4px;
                    ">
                        📅 {current_start} → {current_end}
                    </div>
                </div>
                <!-- Compare -->
                <div style="
                    background:rgba(255,255,255,0.15);
                    padding:10px 14px;
                    border-radius:14px;
                    backdrop-filter: blur(6px);
                ">
                    <div style="
                        font-size:11px;
                        opacity:0.85;
                        font-weight:600;
                        text-transform:uppercase;
                    ">
                        Compare To
                    </div>
                    <div style="
                        font-size:15px;
                        font-weight:700;
                        margin-top:2px;
                    ">
                        Week {previous_week}
                    </div>
                    <div style="
                        font-size:12px;
                        opacity:0.9;
                        margin-top:2px;
                    ">
                        {previous_start} → {previous_end}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # =====================================================
        # KPI UI
        # =====================================================
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <div class="kpi-icon">💰</div>
                </div>
                <div class="kpi-title">
                    GMV TUẦN NÀY
                </div>
                <div class="kpi-value"
                    style="color:#2563EB;">
                    {gmv_this_week:,.0f}₫
                </div>
                <div style="
                    font-size:14px;
                    color:#64748b;
                    margin-bottom:12px;
                ">
                    Tuần trước:
                    <b>{gmv_last_week:,.0f}₫</b>
                </div>
                <div class="
                    {'metric-tag-green'
                    if wow_gmv >= 0
                    else 'metric-tag-red'}
                ">
                    {'▲' if wow_gmv >= 0 else '▼'}
                    {wow_gmv:+.2f}% vs Tuần trước
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <div class="kpi-icon">📦</div>
                </div>
                <div class="kpi-title">
                    ORDERS TUẦN NÀY
                </div>
                <div class="kpi-value"
                    style="color:#7C3AED;">
                    {orders_this_week:,}
                </div>
                <div style="
                    font-size:14px;
                    color:#64748b;
                    margin-bottom:12px;
                ">
                    Tuần trước:
                    <b>{orders_last_week:,}</b>
                </div>
                <div class="
                    {'metric-tag-green'
                    if wow_orders >= 0
                    else 'metric-tag-red'}
                ">
                    {'▲' if wow_orders >= 0 else '▼'}
                    {wow_orders:+.2f}% vs Tuần trước
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <div class="kpi-icon">💵</div>
                </div>
                <div class="kpi-title">
                    NMV TUẦN NÀY
                </div>
                <div class="kpi-value"
                    style="color:#0F766E;">
                    {nmv_this_week:,.0f}₫
                </div>
                <div style="
                    font-size:13px;
                    color:#64748b;
                    margin-bottom:12px;
                ">
                    Tuần trước:
                    <b>{nmv_last_week:,.0f}₫</b>
                </div>
                <div class="
                    {'metric-tag-green'
                    if wow_nmv >= 0
                    else 'metric-tag-red'}
                ">
                    {'▲' if wow_nmv >= 0 else '▼'}
                    {wow_nmv:+.2f}% vs Tuần trước
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:

            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <div class="kpi-icon">💸</div>
                </div>
                <div class="kpi-title">
                    FEES TUẦN NÀY
                </div>
                <div class="kpi-value"
                    style="color:#DC2626;">
                    {fees_predicted:,.0f}₫
                </div>
                <div style="
                    font-size:13px;
                    color:#64748b;
                    margin-bottom:12px;
                ">
                    Fixed + Service + Transaction + Piship
                </div>
                <div style="
                    display:inline-block;
                    padding:6px 14px;
                    border-radius:999px;
                    background:#FEF3C7;
                    color:#B45309;
                    font-size:13px;
                    font-weight:700;
                ">
                    Chi phí ước tính
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
            font-size:18px;
            font-weight:800;
            color:#0F172A;
            margin-top:8px;
            margin-bottom:14px;
        ">
            🛒 Top SKU GMV
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(8)

        for idx, (_, row) in enumerate(sku_metrics.iterrows()):
            sku_name = row["SKU Category"]
            if len(sku_name) > 22:
                sku_name = sku_name[:22] + "..."
            gmv = row["GMV"]
            nmv = row["NMV"]

            with cols[idx % 8]:

                st.markdown(f"""
                <div style="
                    background:white;
                    border:1px solid #E2E8F0;
                    border-radius:16px;
                    padding:18px 10px;
                    height:180px;
                    box-shadow:
                        0 2px 8px rgba(0,0,0,0.04);
                    display:flex;
                    flex-direction:column;
                    justify-content:space-between;
                    margin-top: 10px;
                ">
                    <!-- TOP -->
                    <div style="
                        font-size:12px;
                        font-weight:700;
                        color:#64748B;
                    ">
                        TOP #{idx+1}
                    </div>
                    <!-- SKU -->
                    <div style="
                        font-size:12px;
                        font-weight:700;
                        color:#0F172A;
                        line-height:1.35;
                    ">
                        {sku_name}
                    </div>
                    <!-- GMV -->
                    <div>
                        <div style="
                            font-size:24px;
                            font-weight:800;
                            color:#2563EB;
                            line-height:1;
                            margin-top:6px;
                        ">
                            {gmv/1_000_000:.1f}M
                        </div>
                        <div style="
                            font-size:12px;
                            color:#94A3B8;
                            font-weight:600;
                            margin-top:4px;
                        ">
                            GMV
                        </div>
                    </div>
                    <!-- NMV -->
                    <div style="
                        margin-top:8px;
                        padding-top:8px;
                        border-top:1px solid #F1F5F9;
                    ">
                        <div style="
                            font-size:18px;
                            font-weight:700;
                            color:#0F766E;
                            line-height:1;
                        ">
                            {nmv/1_000_000:.1f}M
                        </div>
                        <div style="
                            font-size:12px;
                            color:#15803d;
                            font-weight:600;
                            margin-top:4px;
                        ">
                            NMV
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        df_ads = st.session_state.shoppe_ads_data

        st.subheader("📊 Ads Performance Overview")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">💸 Ad Spend</div>
                <div class="kpi-value" style="color:#DC2626;">
                    {df_ads["Chi phí"].iloc[0]:,.0f}₫
                </div>
                <div class="metric-tag-red">
                    Chi phí chạy ads
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title"> 🛒 GMV</div>
                <div class="kpi-value" style="color:#2563EB;">
                    {df_ads["Doanh số"].iloc[0]:,.0f}
                </div>
                <div class="metric-tag-green">
                    Doanh số ghi nhận
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">👀 Impressions</div>
                <div class="kpi-value" style="color:#2563EB;">
                    {df_ads["Số lượt xem"].iloc[0]}
                </div>
                <div class="metric-tag-green">
                    Số lần hiển thị
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">👆 Clicks</div>
                <div class="kpi-value" style="color:#7C3AED;">
                    {df_ads["Số lượt click"].iloc[0]}
                </div>
                <div class="metric-tag-green">
                    Lượt nhấp
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">🚀 ROAS</div>
                <div class="kpi-value" style="color:#7C3AED;">
                    {df_ads["ROAS"].iloc[0]}
                </div>
                <div class="metric-tag-green">
                    Hiệu quả qc
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">📦 Product</div>
                <div class="kpi-value" style="color:#DC2626;">
                    {df_ads["Sản phẩm đã bán"].iloc[0]}
                </div>
                <div class="metric-tag-red">
                    Sản phẩm đã bán
                </div>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.markdown(f"""
            <div style="
                background:#F0F9FF;
                border-left:4px solid #0891B2;
                border-radius:12px;
                padding:12px;
                height:105px;
            ">
                <div style="font-size:12px;color:#64748B;">
                    🎯 CTR
                </div>
                <div style="
                    font-size:24px;
                    font-weight:800;
                    color:#0891B2;
                    margin-top:6px;
                ">
                    {df_ads["Tỷ Lệ Click"].iloc[0]}
                </div>
                <div style="
                    font-size:11px;
                    color:#64748B;
                    margin-top:8px;
                ">
                    Tỷ lệ nhấp
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                background:#F0FDF4;
                border-left:4px solid #16A34A;
                border-radius:12px;
                padding:12px;
                height:105px;
            ">
                <div style="font-size:12px;color:#64748B;">
                    🔥 CVR
                </div>
                <div style="
                    font-size:24px;
                    font-weight:800;
                    color:#16A34A;
                    margin-top:6px;
                ">
                    {df_ads["Tỷ lệ chuyển đổi"].iloc[0]}
                </div>
                <div style="
                    font-size:11px;
                    color:#64748B;
                    margin-top:8px;
                ">
                    Tỷ lệ chuyển đổi
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="
                background:#FEF2F2;
                border-left:4px solid #DC2626;
                border-radius:12px;
                padding:12px;
                height:105px;
            ">
                <div style="font-size:12px;color:#64748B;">
                    💰 CPA
                </div>
                <div style="
                    font-size:22px;
                    font-weight:800;
                    color:#DC2626;
                    margin-top:6px;
                ">
                    {df_ads["Chi phí cho mỗi lượt chuyển đổi"].iloc[0]:,.0f}₫
                </div>
                <div style="
                    font-size:11px;
                    color:#64748B;
                    margin-top:8px;
                ">
                    Chi phí / đơn hàng
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="
                background:#FAF5FF;
                border-left:4px solid #7C3AED;
                border-radius:12px;
                padding:12px;
                height:105px;
            ">
                <div style="font-size:12px;color:#64748B;">
                    📈 CPM
                </div>
                <div style="
                    font-size:22px;
                    font-weight:800;
                    color:#7C3AED;
                    margin-top:6px;
                ">
                    {(df_ads["Chi phí"].iloc[0] / df_ads["Số lượt xem"].iloc[0]) * 1000:,.0f}₫
                </div>
                <div style="
                    font-size:11px;
                    color:#64748B;
                    margin-top:8px;
                ">
                    Chi phí / 1000 lượt xem
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div style="
                background:#EFF6FF;
                border-left:4px solid #2563EB;
                border-radius:12px;
                padding:12px;
                height:105px;
            ">
                <div style="font-size:12px;color:#64748B;">
                    🛍️ AOV
                </div>
                <div style="
                    font-size:22px;
                    font-weight:800;
                    color:#2563EB;
                    margin-top:6px;
                ">
                    {df_ads["Doanh số"].iloc[0] / df_ads["Sản phẩm đã bán"].iloc[0]:,.0f}₫
                </div>
                <div style="
                    font-size:11px;
                    color:#64748B;
                    margin-top:8px;
                ">
                    Giá trị đơn TB
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            st.markdown(f"""
            <div style="
                background:#FFFBEB;
                border-left:4px solid #F59E0B;
                border-radius:12px;
                padding:12px;
                height:105px;
            ">
                <div style="font-size:12px;color:#64748B;">
                    💵 CPC
                </div>
                <div style="
                    font-size:22px;
                    font-weight:800;
                    color:#F59E0B;
                    margin-top:6px;
                ">
                    {df_ads["Chi phí"].iloc[0] / df_ads["Số lượt click"].iloc[0]:,.0f}₫
                </div>
                <div style="
                    font-size:11px;
                    color:#64748B;
                    margin-top:8px;
                ">
                    Chi phí / click
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.dataframe(st.session_state.shoppe_ads_data,
                     use_container_width=True)

        st.info("Chart Shopee ở đây")
