import time
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
sys.path.append(os.path.abspath("."))


def run(platform: str):
    st.markdown("""
    <h1 style="
        text-align:center;
        font-size:38px;
        font-weight:800;
        color:#111;
    ">
    🔥 Quick Performance Report 🔥
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* =====================================================
    KPI CARD
    ===================================================== */
    .kpi-card {
        position: relative;
        overflow: hidden;
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(12px);
        border-radius: 28px;
        padding: 26px;
        min-height: 180px;
        border: 1px solid rgba(255,255,255,0.6);
        box-shadow:
            0 10px 35px rgba(15,23,42,0.07),
            inset 0 1px 0 rgba(255,255,255,0.5);
        transition: all 0.28s ease;
    }

    /* Glow top */
    .kpi-card::before {
        content: "";
        position: absolute;
        top: -40px;
        right: -40px;
        width: 120px;
        height: 120px;
        background: rgba(59,130,246,0.08);
        border-radius: 50%;
    }

    /* Hover */
    .kpi-card:hover {
        transform: translateY(-6px);

        box-shadow:
            0 18px 45px rgba(15,23,42,0.12);
    }

    /* KPI TITLE */
    .kpi-title {
        font-size: 14px;

        color: #64748B;

        margin-bottom: 14px;

        font-weight: 600;

        letter-spacing: 0.3px;
    }

    /* KPI VALUE */
    .kpi-value {
        font-size: 40px;

        font-weight: 800;

        line-height: 1.2;

        margin-bottom: 18px;
    }

    /* =====================================================
    SECTION CARD
    ===================================================== */
    .section-card {
        background: rgba(255,255,255,0.92);

        backdrop-filter: blur(12px);

        border-radius: 28px;

        padding: 28px;

        border: 1px solid rgba(255,255,255,0.6);

        box-shadow:
            0 10px 30px rgba(15,23,42,0.06);

        margin-bottom: 22px;
    }

    /* =====================================================
    SECTION TEXT
    ===================================================== */
    .section-title {
        font-size: 26px;

        font-weight: 800;

        color: #0F172A;

        text-align: center;

        margin-bottom: 6px;
    }

    .section-subtitle {
        color: #64748B;

        font-size: 15px;

        text-align: center;

        line-height: 1.6;
    }

    /* =====================================================
    TAGS
    ===================================================== */
    .metric-tag-green {
        background: linear-gradient(
            135deg,
            #DCFCE7,
            #BBF7D0
        );

        color: #166534;

        padding: 7px 14px;

        border-radius: 999px;

        font-size: 11px;

        font-weight: 700;

        width: fit-content;

        box-shadow: 0 4px 10px rgba(34,197,94,0.12);
    }

    .metric-tag-red {
        background: linear-gradient(
            135deg,
            #FEE2E2,
            #FECACA
        );

        color: #991B1B;

        padding: 7px 14px;

        border-radius: 999px;

        font-size: 11px;

        font-weight: 700;

        width: fit-content;

        box-shadow: 0 4px 10px rgba(239,68,68,0.12);
    }

    .metric-tag-yellow {
        background: linear-gradient(
            135deg,
            #FEF3C7,
            #FDE68A
        );

        color: #92400E;

        padding: 7px 14px;

        border-radius: 999px;

        font-size: 11px;

        font-weight: 700;

        width: fit-content;

        box-shadow: 0 4px 10px rgba(245,158,11,0.12);
    }
                
    .metric-tag-blue {
        background: linear-gradient(
            135deg,
            #DBEAFE,
            #BFDBFE
        );

        color: #1D4ED8;

        padding: 7px 14px;

        border-radius: 999px;

        font-size: 11px;

        font-weight: 700;

        width: fit-content;

        box-shadow:
            0 4px 10px rgba(59,130,246,0.15);

        margin-top: 14px;
    }

    /* =====================================================
    CHART CARD
    ===================================================== */
    .chart-card {
        background: rgba(255,255,255,0.92);

        backdrop-filter: blur(12px);

        padding: 24px;

        border-radius: 28px;

        border: 1px solid rgba(255,255,255,0.6);

        box-shadow:
            0 10px 30px rgba(15,23,42,0.06);

        margin-bottom: 22px;

        transition: 0.25s ease;
    }

    .chart-card:hover {
        transform: translateY(-4px);
    }

    /* =====================================================
    PLOTLY CHART
    ===================================================== */
    [data-testid="stPlotlyChart"] {
        background: transparent;

        border-radius: 20px;

        padding: 6px;
    }

    /* =====================================================
    DATAFRAME
    ===================================================== */
    [data-testid="stDataFrame"] {
        border-radius: 24px;

        overflow: hidden;

        border: 1px solid #E5E7EB;

        box-shadow:
            0 8px 25px rgba(15,23,42,0.05);
    }



    /* =====================================================
    INPUT
    ===================================================== */
    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] {

        border-radius: 14px !important;

        border: 1px solid #E2E8F0 !important;
    }
                

    /* =====================================================
    GLOBAL VARIABLES
    ===================================================== */
    :root {

        --card-bg: #FFFFFF;

        --card-radius: 12px;

        --card-padding: 0px;

        --card-border: 1px solid #E5E7EB;

        --card-shadow:
            0 10px 30px rgba(15,23,42,0.06);

        --card-hover-shadow:
            0 18px 40px rgba(15,23,42,0.10);

        --transition-speed: 0.25s;
    }

    /* =====================================================
    CHART HEADER
    ===================================================== */
    .chart-header {

        background: var(--card-bg);

        padding:
            24px
            24px 
            12px
            24px;

        border-radius:
            var(--card-radius)
            var(--card-radius)
            0
            0;

        border: var(--card-border);

        border-bottom: none;

        transition:
            transform var(--transition-speed) ease,
            box-shadow var(--transition-speed) ease;
    }

    /* =====================================================
    PLOTLY OUTER CONTAINER
    ===================================================== */
    [data-testid="stPlotlyChart"] {

        background: var(--card-bg);

        padding:
            0
            var(--card-padding)
            var(--card-padding)
            var(--card-padding);

        border-radius:
            0
            0
            var(--card-radius)
            var(--card-radius);

        border: var(--card-border);

        border-top: none;

        margin-bottom: 24px;

        box-shadow: var(--card-shadow);

        transition:
            transform var(--transition-speed) ease,
            box-shadow var(--transition-speed) ease;
    }

    /* =====================================================
    PLOTLY INNER
    ===================================================== */
    [data-testid="stPlotlyChart"] > div {

        border-radius:
            calc(var(--card-radius) - 8px);

        overflow: hidden;
    }

    /* =====================================================
    PLOTLY REAL CONTAINER
    ===================================================== */
    .js-plotly-plot,
    .plot-container,
    .svg-container {

        border-radius:
            calc(var(--card-radius) - 8px) !important;

        overflow: hidden !important;
    }

    /* =====================================================
    HOVER EFFECT
    ===================================================== */
    .chart-header:hover,
    [data-testid="stPlotlyChart"]:hover {

        transform: translateY(-3px);

        box-shadow: var(--card-hover-shadow);
    }


    </style>
    """, unsafe_allow_html=True)

    def set_latest_df(df, name="df_latest"):
        # Xóa tất cả DataFrame cũ trong session_state trừ Flow nếu muốn giữ
        keys_to_remove = [k for k in st.session_state.keys()
                          if k.endswith("_df")]
        for k in keys_to_remove:
            del st.session_state[k]
        st.session_state[name] = df

    def process_data(df: pd.DataFrame):
        # Chuẩn hóa SKU Category
        df["SKU Category"] = df["Seller SKU"].copy()

        # Danh sách các mẫu thay thế
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
            df["SKU Category"] = df["SKU Category"].str.replace(
                pattern, replacement, regex=True
            )
        df["Province"] = df["Province"].str.replace(
            r"^(Tỉnh |Tinh )", "", regex=True
        )
        df["Province"] = df["Province"].str.replace(
            r"^(Thanh pho |Thành phố |Thành Phố )", "", regex=True
        )

        df["Country"] = df["Country"].replace(
            {
                "Viêt Nam",
                "Vietnam",
                "The Socialist Republic of Viet Nam",
                "Socialist Republic of Vietnam",
            },
            "Việt Nam",
        )

        df["Province"] = df["Province"].replace(
            {
                "Ba Ria– Vung Tau": "Bà Rịa - Vũng Tàu",
                "Bà Rịa-Vũng Tàu": "Bà Rịa - Vũng Tàu",
                "Ba Ria - Vung Tau": "Bà Rịa - Vũng Tàu",
                "Bac Giang": "Bắc Giang",
                "Bac Lieu": "Bạc Liêu",
                "Bac Ninh": "Bắc Ninh",
                "Ben Tre": "Bến Tre",
                "Binh Dinh": "Bình Định",
                "Binh Duong": "Bình Dương",
                "Binh Duong Province": "Bình Dương",
                "Binh Phuoc": "Bình Phước",
                "Binh Thuan": "Bình Thuận",
                "Ca Mau": "Cà Mau",
                "Ca Mau Province": "Cà Mau",
                "Can Tho": "Cần Thơ",
                "Phố Cần Thơ": "Cần Thơ",
                "Da Nang": "Đà Nẵng",
                "Da Nang City": "Đà Nẵng",
                "Phố Đà Nẵng": "Đà Nẵng",
                "Dak Lak": "Đắk Lắk",
                "Đắc Lắk": "Đắk Lắk",
                "Ðắk Nông": "Đắk Nông",
                "Đắk Nông": "Đắk Nông",
                "Dak Nong": "Đắk Nông",
                "Dong Nai": "Đồng Nai",
                "Dong Nai Province": "Đồng Nai",
                "Dong Thap": "Đồng Tháp",
                "Dong Thap Province": "Đồng Tháp",
                "Ha Nam": "Hà Nam",
                "Ha Noi": "Hà Nội",
                "Ha Noi City": "Hà Nội",
                "Phố Hà Nội": "Hà Nội",
                "Hai Phong": "Hải Phòng",
                "Phố Hải Phòng": "Hải Phòng",
                "Ha Tinh": "Hà Tĩnh",
                "Hau Giang": "Hậu Giang",
                "Hô-Chi-Minh-Ville": "Hồ Chí Minh",
                "Ho Chi Minh": "Hồ Chí Minh",
                "Ho Chi Minh City": "Hồ Chí Minh",
                "Kota Ho Chi Minh": "Hồ Chí Minh",
                "Hoa Binh": "Hòa Bình",
                "Hoà Bình": "Hòa Bình",
                "Hung Yen": "Hưng Yên",
                "Khanh Hoa": "Khánh Hòa",
                "Khanh Hoa Province": "Khánh Hòa",
                "Khánh Hoà": "Khánh Hòa",
                "Kien Giang": "Kiên Giang",
                "Kiến Giang": "Kiên Giang",
                "Long An Province": "Long An",
                "Nam Dinh": "Nam Định",
                "Nghe An": "Nghệ An",
                "Ninh Binh": "Ninh Bình",
                "Ninh Thuan": "Ninh Thuận",
                "Quang Binh": "Quảng Bình",
                "Quang Tri": "Quảng Trị",
                "Quang Nam": "Quảng Nam",
                "Quang Ngai": "Quảng Ngãi",
                "Quang Ninh": "Quảng Ninh",
                "Quang Ninh Province": "Quảng Ninh",
                "Soc Trang": "Sóc Trăng",
                "Tay Ninh": "Tây Ninh",
                "Thai Binh": "Thái Bình",
                "Thanh Hoa": "Thanh Hóa",
                "Thanh Hoá": "Thanh Hóa",
                "Hai Duong": "Hải Dương",
                "Thừa Thiên Huế": "Thừa Thiên-Huế",
                "Thua Thien Hue": "Thừa Thiên-Huế",
                "Vinh Long": "Vĩnh Long",
                "Tra Vinh": "Trà Vinh",
                "Vinh Phuc": "Vĩnh Phúc",
                "Cao Bang": "Cao Bằng",
                "Lai Chau": "Lai Châu",
                "Ha Giang": "Hà Giang",
                "Lam Dong": "Lâm Đồng",
                "Lao Cai": "Lào Cai",
                "Phu Tho": "Phú Thọ",
                "Phu Yen": "Phú Yên",
                "Thai Nguyen": "Thái Nguyên",
                "Son La": "Sơn La",
                "Tuyen Quang": "Tuyên Quang",
                "Yen Bai": "Yên Bái",
                "Dien Bien": "Điện Biên",
                "Tien Giang": "Tiền Giang",
            }
        )

        return df

    def process_data_shopee(df_all: pd.DataFrame):
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

        # Danh sách các mẫu thay thế
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

    def compute_kpi_shopee(df: pd.DataFrame):

        df_sp = process_data_shopee(df)
        # 1️⃣ Số đơn đã đặt
        total_orders_sp = df_sp["Mã đơn hàng"].nunique()

        # 2️⃣ Số đơn đã hủy
        canceled_orders_sp = df_sp[df_sp["Actually type"]
                                   == "Đã hủy"]["Mã đơn hàng"].nunique()
        cancel_rate_sp = canceled_orders_sp / total_orders_sp

        # 3️⃣ GMV ước tính
        nmv_sp = df[df_sp["Actually type"] !=
                    "Đã hủy"]["Tổng số tiền Người mua thanh toán"].sum()

        # 4️⃣ % đơn theo SKU
        sku_counts_sp = df.groupby('SKU Category')['Mã đơn hàng'].nunique()
        sku_percent_sp = (sku_counts_sp / total_orders_sp * 100).reset_index()
        sku_percent_sp.columns = ['SKU', '% đơn']

        # 5️⃣ % đơn theo khu vực

        if 'Tỉnh/Thành phố' in df.columns:
            region_counts_sp = df.groupby(
                'Tỉnh/Thành phố')['Mã đơn hàng'].nunique()
            region_percent_sp = (region_counts_sp /
                                 total_orders_sp * 100).reset_index()
            region_percent_sp.columns = ['Khu vực', '% đơn']

        return {
            "total_orders_sp": total_orders_sp,
            "canceled_orders_sp": canceled_orders_sp,
            "cancel_rate_sp": cancel_rate_sp,
            "nmv_sp": nmv_sp,
            "sku_percent_sp": sku_percent_sp,
            "region_percent_sp": region_percent_sp
        }

    def compute_kpi(df: pd.DataFrame):
        """
        Input: df = DataFrame AllOrder hoặc Income đã load
        Output: dict các KPI
        """
        # đảm bảo có các cột cần thiết
        df = process_data(df)

        # 1️⃣ Số đơn đã đặt
        total_orders = df['Order ID'].nunique()

        # 2️⃣ Số đơn đã hủy
        canceled_orders = df[df['Order Status']
                             == 'Cancelled']['Order ID'].nunique()

        cancel_rate = canceled_orders / total_orders

        # 3️⃣ GMV ước tính
        if 'SKU Subtotal After Discount' in df.columns and 'SKU Platform Discount' in df.columns:
            # Chỉ lấy các đơn không bị hủy
            df_valid = df[df["Order Status"] != 'Cancelled']
            nmv = df_valid['Order Amount'].sum()

        else:
            nmv = None

        # 4️⃣ % đơn theo SKU
        sku_counts = df.groupby('SKU Category')['Order ID'].nunique()
        sku_percent = (sku_counts / total_orders * 100).reset_index()
        sku_percent.columns = ['SKU', '% đơn']

        # 5️⃣ % đơn theo khu vực

        if 'Province' in df.columns:
            region_counts = df.groupby('Province')['Order ID'].nunique()
            region_percent = (region_counts / total_orders * 100).reset_index()
            region_percent.columns = ['Khu vực', '% đơn']
        else:
            region_percent = pd.DataFrame()

        return {
            "total_orders": total_orders,
            "canceled_orders": canceled_orders,
            "nmv": nmv,
            "sku_percent": sku_percent,
            "region_percent": region_percent,
            "cancel_rate": cancel_rate
        }

    def flow1(file_obj):
        df = pd.read_csv(file_obj)
        return df

    def flow2(file_obj):
        df = pd.read_excel(file_obj)
        return df

    if platform == "TikTok":
        uploaded_file = st.sidebar.file_uploader(
            "Upload File Tiktok (CSV) At Here", type="csv", key="csv_upload_sidebar"
        )

        if uploaded_file:
            st.sidebar.success("CSV Uploaded!")
            if st.sidebar.button("Check GMV Now"):
                df = flow1(uploaded_file)
                set_latest_df(df, "df_latest")
                st.session_state["flow_name"] = "Flow 1 Result"

        # ==============================
        # UI CHÍNH
        # ==============================
        if "df_latest" in st.session_state:
            df = st.session_state["df_latest"]
            df = process_data(df)
            kpi = compute_kpi(df)

            st.markdown("<div style='height:25px'></div>",
                        unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">📦 Tổng số đơn</div>
                        <div class="kpi-value" style="color:#2563EB">
                            {kpi['total_orders']:,}
                        </div>
                        <div class="metric-tag-blue">
                        All Orders
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">❌ Đơn đã hủy</div>
                        <div class="kpi-value" style="color:#C62828">
                            {kpi['canceled_orders']:,}
                        </div>
                        <div class="metric-tag-red">
                        Cancel Orders
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">⚠️ Tỷ lệ hủy</div>
                        <div class="kpi-value" style="color:#EF6C00">
                            {kpi['cancel_rate']*100:.2f}%
                        </div>
                        <div class="metric-tag-yellow">
                        Warning
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col4:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">💰 NMV ước tính</div>
                        <div class="kpi-value" style="color:#0F766E">{kpi['nmv']:,.0f}₫</div>
                        <div class="metric-tag-green">
                        Revenue prediction
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br><br>", unsafe_allow_html=True)

            # ================= SKU + REGION =================
            # =====================================================
            # DETAIL ANALYTICS SECTION
            # =====================================================
            st.markdown("""
            <div class="section-card">
                <div class="section-title">
                    📊 Detail Analytics
                </div>
                <div class="section-subtitle">
                    Advanced order performance & revenue insights
                </div>

            </div>
            """, unsafe_allow_html=True)

            # =====================================================
            # DATE PROCESSING
            # =====================================================
            df["Created Time"] = pd.to_datetime(
                df["Created Time"].astype(str).str.strip(),
                dayfirst=True,
                errors="coerce"
            )

            df["date"] = df["Created Time"].dt.date
            df["hour"] = df["Created Time"].dt.hour
            df["weekday"] = df["Created Time"].dt.day_name()

            # =====================================================
            # COMMON LAYOUT
            # =====================================================
            COMMON_LAYOUT = dict(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="white",
                font=dict(
                    family="Arial",
                    size=13,
                    color="#111827"
                ),
                margin=dict(l=20, r=20, t=60, b=20),
                hovermode="x unified"
            )

            # =====================================================
            # HEATMAP DATA
            # =====================================================
            weekday_order = [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ]

            heatmap_data = (
                df.groupby(["weekday", "hour"])
                .size()
                .unstack(fill_value=0)
            )

            heatmap_data = heatmap_data.reindex(
                columns=range(24),
                fill_value=0
            )

            heatmap_data = heatmap_data.reindex(
                weekday_order
            )

            # =====================================================
            # ORDER TREND
            # =====================================================
            orders_by_day = (
                df.groupby("date")["Order ID"]
                .nunique()
                .reset_index()
            )

            fig_orders_day = px.area(
                orders_by_day,
                x="date",
                y="Order ID",
                markers=True
            )

            fig_orders_day.update_traces(
                line=dict(
                    color="#16A34A",
                    width=3
                ),
                fill="tozeroy"
            )

            fig_orders_day.update_layout(
                title="📈 Daily Order Trend",
                xaxis_title="Date",
                yaxis_title="Orders",
                **COMMON_LAYOUT
            )

            # =====================================================
            # CANCEL RATE TREND
            # =====================================================

            cancel_orders_day = (
                df[df["Order Status"] == "Cancelled"]
                .groupby("date")["Order ID"]
                .nunique()
                .reset_index()
            )

            fig_cancel_orders_day = px.line(
                cancel_orders_day,
                x="date",
                y="Order ID",
                markers=True
            )

            fig_cancel_orders_day.update_traces(
                line=dict(color="#EF4444", width=3),
                marker=dict(size=8)
            )

            fig_cancel_orders_day.update_layout(
                title="❌ Xu hướng đơn hủy theo ngày",
                xaxis_title="Date",
                yaxis_title="Orders",

                **COMMON_LAYOUT
            )

            # =====================================================
            # TOP SKU
            # =====================================================
            top_sku = (
                df.groupby("SKU Category")
                .size()
                .reset_index(name="orders")
                .sort_values("orders", ascending=False)
                .head(10)
            )

            fig_topsku = px.bar(
                top_sku,
                x="orders",
                y="SKU Category",
                orientation="h",
                text="orders",
                color_discrete_sequence=["#2563EB"]
            )

            fig_topsku.update_layout(
                title="🚀 Top SKU Performance",
                yaxis=dict(autorange="reversed"),
                **COMMON_LAYOUT
            )

            fig_topsku.update_traces(
                textposition="outside"
            )

            # =====================================================
            # CANCEL SKU
            # =====================================================
            cancel_sku = (
                df[df["Order Status"] == "Cancelled"]
                .groupby("SKU Category")["Order ID"]
                .nunique()
                .reset_index(name="canceled_orders")
                .sort_values("canceled_orders", ascending=False)
            )

            fig_cancel = px.bar(
                cancel_sku.head(10),
                x="SKU Category",
                y="canceled_orders",
                text="canceled_orders",
                color_discrete_sequence=["#DC2626"]
            )

            fig_cancel.update_layout(
                title="❌ Cancelled Orders by SKU",
                xaxis_title="SKU",
                yaxis_title="Cancelled Orders",
                **COMMON_LAYOUT
            )

            # =====================================================
            # HEATMAP
            # =====================================================
            fig_heat = px.imshow(
                heatmap_data,
                color_continuous_scale="Turbo",
                labels=dict(
                    x="Hour",
                    y="Weekday",
                    color="Orders"
                ),
                aspect="auto"
            )

            fig_heat.update_layout(
                title="🔥 Order Heatmap",
                **COMMON_LAYOUT
            )

            # =====================================================
            # NMV PROCESSING
            # =====================================================
            df_cal = df[df["Order Status"] != "Cancelled"].copy()

            df_cal["NMV"] = (
                df_cal["SKU Subtotal After Discount"]
                + df_cal["SKU Platform Discount"]
            )

            # =====================================================
            # NMV DAILY
            # =====================================================
            nmv_day = (
                df_cal.groupby("date")["NMV"]
                .sum()
                .reset_index()
            )

            fig_nmv_day = px.area(
                nmv_day,
                x="date",
                y="NMV",
                markers=True
            )

            fig_nmv_day.update_traces(
                line=dict(
                    width=3,
                    color="#F97316"
                ),
                fill="tozeroy"
            )

            fig_nmv_day.update_layout(
                title="💰 NMV Daily Trend",
                xaxis_title="Date",
                yaxis_title="NMV",
                **COMMON_LAYOUT
            )

            fig_nmv_day.update_yaxes(
                tickformat=",.0f"
            )

            # =====================================================
            # NMV HOUR
            # =====================================================
            nmv_hour = (
                df_cal.groupby("hour")["NMV"]
                .sum()
                .reset_index()
            )

            fig_nmv_hour = px.bar(
                nmv_hour,
                x="hour",
                y="NMV",
                text="NMV",
                color_discrete_sequence=["#9333EA"]
            )

            fig_nmv_hour.update_layout(
                title="⏰ Revenue by Hour",
                xaxis_title="Hour",
                yaxis_title="NMV",
                **COMMON_LAYOUT
            )

            fig_nmv_hour.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="outside"
            )

            # =====================================================
            # SKU PIE
            # =====================================================
            fig_sku = px.pie(
                kpi["sku_percent"],
                names="SKU",
                values="% đơn",
                hole=0.3
            )

            fig_sku.update_traces(
                text=kpi["sku_percent"]["% đơn"]
                .round(1)
                .astype(str) + "%",
                textinfo="text+label"
            )

            fig_sku.update_layout(
                title="🥇 SKU Distribution",
                **COMMON_LAYOUT
            )

            # =====================================================
            # REGION PIE
            # =====================================================
            if not kpi["region_percent"].empty:

                fig_region = px.pie(
                    kpi["region_percent"],
                    names="Khu vực",
                    values="% đơn",
                    hole=0.3
                )

                fig_region.update_traces(
                    textinfo="percent+label"
                )

                fig_region.update_layout(
                    title="🌏 Regional Distribution",
                    **COMMON_LAYOUT
                )

            # =====================================================
            # DASHBOARD LAYOUT
            # =====================================================

            st.markdown("""
                <div class="chart-header">
                    <div class="section-title">
                        📈 Order Trend
                    </div>
                    <div class="section-subtitle">
                        Daily order tracking performance
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.plotly_chart(
                fig_orders_day,
                use_container_width=True
            )

            # ROW 1
            col1, col2 = st.columns([1, 1])

            with col1:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">📉 Cancel Orders by Day</div>
                    <div class="section-subtitle">
                        Daily trend of cancelled orders
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_cancel_orders_day,
                    use_container_width=True
                )

            with col2:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">
                        🥇 SKU Distribution
                    </div>
                    <div class="section-subtitle">
                        Order contribution by SKU
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_sku,
                    use_container_width=True
                )

            # ROW 2
            col1, col2 = st.columns([1.5, 2])

            with col1:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">
                        🔥 Order Heatmap
                    </div>
                    <div class="section-subtitle">
                        Best order time analysis
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_heat,
                    use_container_width=True
                )

            with col2:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">
                        💰 NMV Daily Trend
                    </div>
                    <div class="section-subtitle">
                        Revenue movement over time
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_nmv_day,
                    use_container_width=True
                )

            # ROW 3
            col1, col2 = st.columns([3, 2])

            with col1:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">
                        ⏰ Revenue by Hour
                    </div>
                    <div class="section-subtitle">
                        Peak revenue hours
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_nmv_hour,
                    use_container_width=True
                )

            with col2:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">
                        🚀 Top SKU
                    </div>
                    <div class="section-subtitle">
                        Best selling categories
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_topsku,
                    use_container_width=True
                )

            # ROW 4
            col1, col2 = st.columns(2)

            with col1:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">
                        ❌ Cancel Analysis
                    </div>
                    <div class="section-subtitle">
                        Most cancelled SKU categories
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_cancel,
                    use_container_width=True
                )

            with col2:

                if not kpi["region_percent"].empty:

                    st.markdown("""
                    <div class="chart-header">
                        <div class="section-title">
                            🌏 Region Distribution
                        </div>
                        <div class="section-subtitle">
                            Regional order contribution
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.plotly_chart(
                        fig_region,
                        use_container_width=True
                    )

    if platform == "Shopee":
        uploaded_file_sp = st.sidebar.file_uploader(
            "Upload File Shopee (XLSX) At Here", type="xlsx", key="xlsx_upload_sidebar"
        )

        if uploaded_file_sp:
            st.sidebar.success("File Uploaded!")
            if st.sidebar.button("Check GMV Now"):
                df_sp = flow2(uploaded_file_sp)
                set_latest_df(df_sp, "df_latest_sp")
        # =====================================================
        # GLOBAL CSS
        # =====================================================

        # =====================================================
        # LOAD DATA
        # =====================================================
        if "df_latest_sp" in st.session_state:

            df_sp = st.session_state["df_latest_sp"]
            df_sp = process_data_shopee(df_sp)
            kpi_sp = compute_kpi_shopee(df_sp)

            # =====================================================
            # KPI SECTION
            # =====================================================
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">📦 Tổng đơn</div>
                    <div class="kpi-value" style="color:#2563EB">
                        {kpi_sp['total_orders_sp']:,}
                    </div>
                    <div class="metric-tag-blue">
                        Active Orders
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">❌ Đơn huỷ</div>
                    <div class="kpi-value" style="color:#DC2626">
                        {kpi_sp['canceled_orders_sp']:,}
                    </div>
                    <div class="metric-tag-red">
                        Cancel Orders
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">⚠️ Tỷ lệ huỷ</div>
                    <div class="kpi-value" style="color:#D97706">
                        {kpi_sp['cancel_rate_sp']*100:.2f}%
                    </div>
                    <div class="metric-tag-yellow">
                        Warning
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">💰 NMV</div>
                    <div class="kpi-value" style="color:#0F766E">
                        {kpi_sp['nmv_sp']:,.0f}₫
                    </div>
                    <div class="metric-tag-green">
                        Revenue
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            # =====================================================
            # DATE PROCESSING
            # =====================================================
            df_sp["Ngày đặt hàng"] = pd.to_datetime(
                df_sp["Ngày đặt hàng"],
                errors="coerce"
            )

            df_sp["date"] = df_sp["Ngày đặt hàng"].dt.date
            df_sp["hour"] = df_sp["Ngày đặt hàng"].dt.hour
            df_sp["weekday"] = df_sp["Ngày đặt hàng"].dt.day_name()

            # =====================================================
            # COMMON CHART LAYOUT
            # =====================================================
            COMMON_LAYOUT = dict(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(
                    family="Arial",
                    size=13,
                    color="#111827"
                ),
                margin=dict(l=20, r=20, t=60, b=20),
                hovermode="x unified"
            )

            # =====================================================
            # ORDERS BY DAY
            # =====================================================
            orders_by_day_sp = (
                df_sp.groupby("date")["Mã đơn hàng"]
                .nunique()
                .reset_index()
            )

            fig_orders_day_sp = px.area(
                orders_by_day_sp,
                x="date",
                y="Mã đơn hàng",
                markers=True
            )

            fig_orders_day_sp.update_traces(
                line=dict(color="#F58B00", width=3)
            )

            fig_orders_day_sp.update_layout(
                title="📈 Xu hướng đơn hàng theo ngày",
                xaxis_title="Ngày",
                yaxis_title="Số đơn",
                **COMMON_LAYOUT
            )
            # =====================================================
            # CANCEL ORDERS BY DAY
            # =====================================================

            cancel_orders_day_sp = (
                df_sp[df_sp["Actually type"] == "Đã hủy"]
                .groupby("date")["Mã đơn hàng"]
                .nunique()
                .reset_index(name="Số đơn hủy")
            )

            fig_cancel_orders_day_sp = px.line(
                cancel_orders_day_sp,
                x="date",
                y="Số đơn hủy",
                markers=True
            )

            fig_cancel_orders_day_sp.update_traces(
                line=dict(color="#EF4444", width=3),
                marker=dict(size=8)
            )

            fig_cancel_orders_day_sp.update_layout(
                title="❌ Xu hướng đơn hủy theo ngày",
                xaxis_title="Ngày",
                yaxis_title="Số đơn hủy",

                **COMMON_LAYOUT
            )

            # =====================================================
            # SKU DONUT
            # =====================================================
            fig_sku_sp = px.pie(
                kpi_sp["sku_percent_sp"],
                names="SKU",
                values="% đơn",
                hole=0.3
            )

            fig_sku_sp.update_traces(
                text=kpi_sp["sku_percent_sp"]["% đơn"]
                .round(1)
                .astype(str) + "%",
                textinfo="text+label"
            )

            fig_sku_sp.update_layout(
                title="🥇 Tỷ lệ đơn theo SKU",
                **COMMON_LAYOUT
            )

            # =====================================================
            # TOP SKU
            # =====================================================
            top_sku_sp = (
                df_sp.groupby("SKU Category")
                .size()
                .reset_index(name="orders_sp")
                .sort_values("orders_sp", ascending=False)
                .head(10)
            )

            fig_topsku_sp = px.bar(
                top_sku_sp,
                x="orders_sp",
                y="SKU Category",
                orientation="h",
                text="orders_sp",
                color_discrete_sequence=["#0085A7"]
            )

            fig_topsku_sp.update_layout(
                title="🔥 Top 10 SKU bán chạy",
                yaxis=dict(autorange="reversed"),
                **COMMON_LAYOUT
            )

            # =====================================================
            # HEATMAP
            # =====================================================
            weekday_order_sp = [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ]

            heatmap_data_sp = (
                df_sp.groupby(["weekday", "hour"])
                .size()
                .unstack(fill_value=0)
            )

            heatmap_data_sp = heatmap_data_sp.reindex(
                columns=range(24),
                fill_value=0
            )

            heatmap_data_sp = heatmap_data_sp.reindex(
                weekday_order_sp
            )

            fig_heat_sp = px.imshow(
                heatmap_data_sp,
                color_continuous_scale="Turbo",
                aspect="auto",
                title="🔥 Heatmap đơn hàng"
            )

            fig_heat_sp.update_layout(
                **COMMON_LAYOUT
            )

            # =====================================================
            # FILTER CANCEL
            # =====================================================
            df_sp_new = df_sp[
                df_sp["Actually type"] != "Đã hủy"
            ].copy()

            # =====================================================
            # GMV BY DAY
            # =====================================================
            nmv_day_sp = (
                df_sp_new.groupby("date")[
                    "Tổng số tiền Người mua thanh toán"
                ]
                .sum()
                .reset_index()
            )

            fig_nmv_day_sp = px.area(
                nmv_day_sp,
                x="date",
                y="Tổng số tiền Người mua thanh toán",
                markers=True
            )

            fig_nmv_day_sp.update_traces(
                line=dict(width=3, color="#08750D"),
                fill="tozeroy"
            )

            fig_nmv_day_sp.update_layout(
                title="💰 Xu hướng NMV theo ngày",
                xaxis_title="Ngày",
                yaxis_title="NMV",
                **COMMON_LAYOUT
            )

            fig_nmv_day_sp.update_yaxes(
                tickformat=",.0f"
            )

            # =====================================================
            # GMV BY HOUR
            # =====================================================
            gmv_hour_sp = (
                df_sp.groupby("hour")[
                    "Tổng số tiền Người mua thanh toán"
                ]
                .sum()
                .reset_index()
            )

            fig_gmv_hour_sp = px.bar(
                gmv_hour_sp,
                x="hour",
                y="Tổng số tiền Người mua thanh toán",
                text="Tổng số tiền Người mua thanh toán",
                color_discrete_sequence=["#D4AD00"]
            )

            fig_gmv_hour_sp.update_layout(
                title="💰 Doanh thu theo giờ",
                xaxis_title="Giờ",
                yaxis_title="GMV",
                **COMMON_LAYOUT
            )

            fig_gmv_hour_sp.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="outside"
            )
            # =====================================================
            # ROW 1
            # =====================================================
            left_col, right_col = st.columns(2)

            with left_col:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">📈 Order Trend</div>
                    <div class="section-subtitle">
                        Daily order performance tracking
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_orders_day_sp,
                    use_container_width=True
                )

            with right_col:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">🥇 SKU Distribution</div>
                    <div class="section-subtitle">
                        Percentage contribution by SKU
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_sku_sp,
                    use_container_width=True
                )

            # =====================================================
            # ROW 2
            # =====================================================
            col1, col2 = st.columns([2, 3])

            with col1:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">🔥 Order Heatmap</div>
                    <div class="section-subtitle">
                        Order density by weekday & hour
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_heat_sp,
                    use_container_width=True
                )

            with col2:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">💰 GMV Daily Trend</div>
                    <div class="section-subtitle">
                        Revenue movement across dates
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_nmv_day_sp,
                    use_container_width=True
                )

            # =====================================================
            # ROW 3
            # =====================================================

            col1, col2 = st.columns([2, 1.5])

            with col1:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">📉 Cancel Orders by Day</div>
                    <div class="section-subtitle">
                        Daily trend of cancelled orders
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_cancel_orders_day_sp,
                    use_container_width=True
                )

            with col2:

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">🚀 Top SKU</div>
                    <div class="section-subtitle">
                        Best selling product categories
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_topsku_sp,
                    use_container_width=True
                )

                # =====================================================
                # REGION PIE
                # =====================================================

            st.markdown("""
            <div class="chart-header">
                <div class="section-title">⏰ Revenue by Hour</div>
                <div class="section-subtitle">
                    Best revenue hours during the day
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.plotly_chart(
                fig_gmv_hour_sp,
                use_container_width=True
            )
            if not kpi_sp["region_percent_sp"].empty:

                fig_region_sp = px.pie(
                    kpi_sp["region_percent_sp"],
                    names="Khu vực",
                    values="% đơn",
                    hole=0.3
                )

                fig_region_sp.update_traces(
                    textinfo="percent+label",
                    pull=[0.03] * len(kpi_sp["region_percent_sp"])
                )

                fig_region_sp.update_layout(
                    title="🌏 Regional Distribution",
                    **COMMON_LAYOUT
                )

                st.markdown("""
                <div class="chart-header">
                    <div class="section-title">
                        🌏 Regional Distribution
                    </div>
                    <div class="section-subtitle">
                        Percentage contribution by region
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.plotly_chart(
                    fig_region_sp,
                    use_container_width=True
                )

            # =====================================================
            # DATAFRAME
            # =====================================================
            st.markdown("""
            <div class="section-card">
                <div class="section-title">
                    📋 Order Detail Data
                </div>
                <div class="section-subtitle">
                    Detailed Shopee order tracking table
                </div>

            </div>
            """, unsafe_allow_html=True)

            # FILTER BAR
            filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

            with filter_col1:
                search_value = st.text_input(
                    "🔍 Search SKU / Order ID",
                    placeholder="Nhập SKU hoặc mã đơn..."
                )

            with filter_col2:
                selected_status = st.selectbox(
                    "📦 Order Status",
                    ["All"] + list(df_sp["Actually type"].dropna().unique())
                )

            with filter_col3:
                sort_option = st.selectbox(
                    "📊 Sort",
                    ["Newest", "Oldest"]
                )

            # =====================================================
            # FILTER LOGIC
            # =====================================================
            df_display = df_sp.copy()

            if search_value:

                df_display = df_display[
                    df_display.astype(str)
                    .apply(
                        lambda row: row.str.contains(
                            search_value,
                            case=False
                        ).any(),
                        axis=1
                    )
                ]

            if selected_status != "All":

                df_display = df_display[
                    df_display["Actually type"] == selected_status
                ]

            # =====================================================
            # SORT
            # =====================================================
            if "Ngày đặt hàng" in df_display.columns:

                df_display = df_display.sort_values(
                    "Ngày đặt hàng",
                    ascending=(sort_option == "Oldest")
                )

            # =====================================================
            # DATAFRAME STYLE
            # =====================================================
            st.dataframe(
                df_display,
                use_container_width=True,
                height=600
            )

            # FOOTER INFO
            st.markdown(f"""
            <div style="
                color:#6B7280;
                font-size:13px;
                margin-top:10px;
            ">
                Showing <b>{len(df_display):,}</b> rows
            </div>
            """, unsafe_allow_html=True)
