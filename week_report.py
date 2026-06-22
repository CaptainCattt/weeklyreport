import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
# ... các import khác

sys.path.append(os.path.abspath("."))

######## FUNCTONS ##########


def run(platform: str):

    def read_file_tiktok(file_obj):
        dtype_dict = {
            "Order ID": str,
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

    def read_file_shopee(file_obj):
        df = pd.read_excel(file_obj)
        return df

    def process_tiktok_data(df: pd.DataFrame):
        df.columns = df.columns.str.strip()
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

    def kpi_tiktok(df: pd.DataFrame):
        # process data
        df_tt = process_tiktok_data(df)

        df_tt["Created Time"] = pd.to_datetime(
            df_tt["Created Time"],
            errors="coerce"
        )
        # =========================
        # ISO WEEK
        # =========================
        iso = df_tt["Created Time"].dt.isocalendar()

        df_tt["week"] = iso.week.astype(int)
        df_tt["year"] = iso.year.astype(int)

        # =========================
        # GET UNIQUE WEEKS
        # =========================
        all_weeks = (
            df_tt[["year", "week"]]
            .drop_duplicates()
            .sort_values(["year", "week"])
            .reset_index(drop=True)
        )

        # Need at least 2 weeks
        if len(all_weeks) < 2:
            return df_tt, pd.DataFrame(), all_weeks

        # =========================
        # THIS WEEK / LAST WEEK
        # =========================

        # Current week
        current_tt = all_weeks.iloc[-1]

        df_this_week_tt = df_tt[
            (df_tt["week"] == current_tt["week"]) &
            (df_tt["year"] == current_tt["year"])
        ].copy()

        # Previous week
        previous_tt = all_weeks.iloc[-2]

        df_last_week_tt = df_tt[
            (df_tt["week"] == previous_tt["week"]) &
            (df_tt["year"] == previous_tt["year"])
        ].copy()

        return df_this_week_tt, df_last_week_tt, current_tt, previous_tt

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
            margin-bottom: 8px;
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
        
        </style>
        """,
        unsafe_allow_html=True
    )
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

    # =========================
    # TIKTOK UI
    # =========================
    if platform == "TikTok":
        # =========================
        # HEADER
        # =========================
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h1 style="
                font-size:38px;
                font-weight:800;
                color:#111;
                margin-bottom:5px;
            ">
                📊 Weekly Report Dashboard
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
                    df = read_file_tiktok(uploaded_file)
                    st.session_state.df = df
                except Exception as e:
                    st.sidebar.error(f"Cannot read file: {e}")

        if "df" in st.session_state:
            # get data
            df = st.session_state["df"]
            df_this_week_tt, df_last_week_tt, current_tt, previous_tt = kpi_tiktok(
                df)

            # handle logic date

            current_week_tt = int(current_tt["week"])
            current_year_tt = int(current_tt["year"])
            previous_week_tt = int(previous_tt["week"])
            previous_year_tt = int(previous_tt["year"])

            current_start_tt = (
                df_this_week_tt["Created Time"]
                .min()
                .strftime("%d/%m")
            )

            current_end_tt = (
                df_this_week_tt["Created Time"]
                .max()
                .strftime("%d/%m")
            )

            previous_start_tt = (
                df_last_week_tt["Created Time"]
                .min()
                .strftime("%d/%m")
            )

            previous_end_tt = (
                df_last_week_tt["Created Time"]
                .max()
                .strftime("%d/%m")
            )

            # handle logic caculate KPI, charts, .....

            # GMV - Gross Merchandise Value
            # =====================================================
            gmv_this_week_tt = df_this_week_tt["SKU Subtotal After Discount"].sum(
            )
            gmv_last_week_tt = df_last_week_tt["SKU Subtotal After Discount"].sum(
            )

            # NMV = Net Merchandise Value (Giá trị hàng hóa thuần)
            # =====================================================

            df_valid_this_week_tt = df_this_week_tt[df_this_week_tt["Order Status"] != 'Cancelled']
            df_valid_last_week_tt = df_last_week_tt[df_last_week_tt["Order Status"] != 'Cancelled']

            nmv_this_week_tt = df_valid_this_week_tt["SKU Subtotal After Discount"].sum(
            )
            nmv_last_week_tt = df_valid_last_week_tt["SKU Subtotal After Discount"].sum(
            )

            # ORDERS
            # =====================================================
            orders_this_week_tt = df_this_week_tt["Order ID"].nunique()
            orders_last_week_tt = df_last_week_tt["Order ID"].nunique()

            # WOW
            # =====================================================
            gmv_wow_tt = ((gmv_this_week_tt - gmv_last_week_tt) /
                          gmv_last_week_tt * 100) if gmv_last_week_tt != 0 else 0
            nmv_wow_tt = ((nmv_this_week_tt - nmv_last_week_tt) /
                          nmv_last_week_tt * 100) if nmv_last_week_tt != 0 else 0
            orders_wow_tt = ((orders_this_week_tt - orders_last_week_tt) /
                             orders_last_week_tt * 100) if orders_last_week_tt != 0 else 0
            orders_cancelled_this_week_tt = df_this_week_tt[df_this_week_tt["Order Status"]
                                                            == 'Cancelled']["Order ID"].nunique()
            orders_cancelled_last_week_tt = df_last_week_tt[df_last_week_tt["Order Status"]
                                                            == 'Cancelled']["Order ID"].nunique()
            orders_cancelled_wow_tt = ((orders_cancelled_this_week_tt - orders_cancelled_last_week_tt) /
                                       orders_cancelled_last_week_tt * 100) if orders_cancelled_last_week_tt != 0 else 0

            # AOV - Average Order Value
            # =====================================================
            aov_this_week_tt = gmv_this_week_tt / \
                orders_this_week_tt if orders_this_week_tt != 0 else 0
            aov_last_week_tt = gmv_last_week_tt / \
                orders_last_week_tt if orders_last_week_tt != 0 else 0
            aov_wow_tt = ((aov_this_week_tt - aov_last_week_tt) /
                          aov_last_week_tt * 100) if aov_last_week_tt != 0 else 0

            # CANCELLATION RATE
            # =====================================================
            cancel_rate_this_week_tt = (orders_cancelled_this_week_tt /
                                        orders_this_week_tt * 100) if orders_this_week_tt != 0 else 0
            cancel_rate_last_week_tt = (orders_cancelled_last_week_tt /
                                        orders_last_week_tt * 100) if orders_last_week_tt != 0 else 0
            cancel_rate_wow_tt = cancel_rate_this_week_tt - cancel_rate_last_week_tt

            # NMV RATE
            # =====================================================
            nmv_rate_this_week_tt = (
                nmv_this_week_tt / gmv_this_week_tt * 100) if gmv_this_week_tt != 0 else 0
            nmv_rate_last_week_tt = (
                nmv_last_week_tt / gmv_last_week_tt * 100) if gmv_last_week_tt != 0 else 0

            # CHART DATA - GMV & Orders theo ngày
            # =====================================================
            gmv_by_day_this = (
                df_this_week_tt.groupby(df_this_week_tt["Created Time"].dt.date)[
                    "SKU Subtotal After Discount"]
                .sum().reset_index()
            )
            gmv_by_day_this.columns = ["date", "gmv"]
            gmv_by_day_this["label"] = "Tuần này"

            gmv_by_day_last = (
                df_last_week_tt.groupby(df_last_week_tt["Created Time"].dt.date)[
                    "SKU Subtotal After Discount"]
                .sum().reset_index()
            )
            gmv_by_day_last.columns = ["date", "gmv"]
            gmv_by_day_last["label"] = "Tuần trước"

            orders_by_day_this = (
                df_this_week_tt.groupby(df_this_week_tt["Created Time"].dt.date)[
                    "Order ID"]
                .nunique().reset_index()
            )
            orders_by_day_this.columns = ["date", "orders"]
            orders_by_day_this["label"] = "Tuần này"

            orders_by_day_last = (
                df_last_week_tt.groupby(df_last_week_tt["Created Time"].dt.date)[
                    "Order ID"]
                .nunique().reset_index()
            )
            orders_by_day_last.columns = ["date", "orders"]
            orders_by_day_last["label"] = "Tuần trước"

            # TOP PRODUCTS
            # =====================================================
            top_products_tt = (
                df_valid_this_week_tt.groupby("SKU Category")
                .agg(
                    nmv=("SKU Subtotal After Discount", "sum"),
                    orders=("Order ID", "nunique")
                )
                .sort_values("nmv", ascending=False)
                .head(10)
                .reset_index()
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
                            Week {current_week_tt} - {current_year_tt}
                        </div>
                        <div style="
                            font-size:13px;
                            opacity:0.92;
                            margin-top:4px;
                        ">
                            📅 {current_start_tt} → {current_end_tt}
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
                            Week {previous_week_tt} - {previous_year_tt}
                        </div>
                        <div style="
                            font-size:12px;
                            opacity:0.9;
                            margin-top:2px;
                        ">
                            {previous_start_tt} → {previous_end_tt}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # =====================================================
            # KPI ROW 1: GMV, NMV, ORDERS, CANCELLED
            # =====================================================
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">💰</div></div>
                    <div class="kpi-title">GMV TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#2563EB;">{gmv_this_week_tt:,.0f}₫</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{gmv_last_week_tt:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if gmv_wow_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if gmv_wow_tt >= 0 else '▼'} {gmv_wow_tt:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">💵</div></div>
                    <div class="kpi-title">NMV TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#0F766E;">{nmv_this_week_tt:,.0f}₫</div>
                    <div style="font-size:13px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{nmv_last_week_tt:,.0f}₫</b>
                    </div>
                     <div class="{'metric-tag-green' if nmv_wow_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if nmv_wow_tt >= 0 else '▼'} {nmv_wow_tt:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">📦</div></div>
                    <div class="kpi-title">ORDERS TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#7C3AED;">{orders_this_week_tt:,}</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{orders_last_week_tt:,}</b>
                    </div>
                    <div class="{'metric-tag-green' if orders_wow_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if orders_wow_tt >= 0 else '▼'} {orders_wow_tt:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">❌</div></div>
                    <div class="kpi-title">CANCELLED TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#DC2626;">{orders_cancelled_this_week_tt:,}</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{orders_cancelled_last_week_tt:,}</b>
                    </div>
                    <div class="{'metric-tag-green' if orders_cancelled_wow_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if orders_cancelled_wow_tt >= 0 else '▼'} {orders_cancelled_wow_tt:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # =====================================================
            # KPI ROW 2: AOV + NMV RATE + CANCEL RATE
            # =====================================================
            st.markdown("<div style='margin-top:16px;'></div>",
                        unsafe_allow_html=True)
            col5, col6, col7 = st.columns(3)

            with col5:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">🛒</div></div>
                    <div class="kpi-title">AOV TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#D97706;">{aov_this_week_tt:,.0f}₫</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{aov_last_week_tt:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if aov_wow_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if aov_wow_tt >= 0 else '▼'} {aov_wow_tt:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col6:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">✅</div></div>
                    <div class="kpi-title">NMV RATE TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#0F766E;">{nmv_rate_this_week_tt:.1f}%</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{nmv_rate_last_week_tt:.1f}%</b>
                    </div>
                    <div class="{'metric-tag-green' if nmv_rate_this_week_tt >= nmv_rate_last_week_tt else 'metric-tag-red'}">
                        {'▲' if nmv_rate_this_week_tt >= nmv_rate_last_week_tt else '▼'}
                        {nmv_rate_this_week_tt - nmv_rate_last_week_tt:+.2f}pp vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col7:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">📉</div></div>
                    <div class="kpi-title">CANCEL RATE TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#DC2626;">{cancel_rate_this_week_tt:.1f}%</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{cancel_rate_last_week_tt:.1f}%</b>
                    </div>
                    <div class="{'metric-tag-red' if cancel_rate_wow_tt >= 0 else 'metric-tag-green'}">
                        {'▲' if cancel_rate_wow_tt >= 0 else '▼'} {cancel_rate_wow_tt:+.2f}pp vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # =====================================================
            # CHARTS
            # =====================================================
            st.markdown("""
            <div class="kpi-card">
                <div class="section-title">
                    📈 Biểu đồ theo ngày
                </div>
                <div class="section-subtitle">
                    Advanced order performance & revenue insights
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.container(border=True):
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    import plotly.graph_objects as go
                    fig_gmv = go.Figure()
                    fig_gmv.add_trace(go.Bar(
                        x=[str(d) for d in gmv_by_day_last["date"]],
                        y=gmv_by_day_last["gmv"],
                        name="Tuần trước",
                        marker_color="#CBD5E1"
                    ))
                    fig_gmv.add_trace(go.Bar(
                        x=[str(d) for d in gmv_by_day_this["date"]],
                        y=gmv_by_day_this["gmv"],
                        name="Tuần này",
                        marker_color="#2563EB"
                    ))
                    fig_gmv.update_layout(
                        title="GMV theo ngày",
                        barmode="group",
                        height=320,
                        margin=dict(l=0, r=0, t=40, b=0),
                        legend=dict(orientation="h", yanchor="bottom",
                                    y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_gmv, use_container_width=True)

                with chart_col2:
                    fig_orders = go.Figure()
                    fig_orders.add_trace(go.Bar(
                        x=[str(d) for d in orders_by_day_last["date"]],
                        y=orders_by_day_last["orders"],
                        name="Tuần trước",
                        marker_color="#CBD5E1"
                    ))
                    fig_orders.add_trace(go.Bar(
                        x=[str(d) for d in orders_by_day_this["date"]],
                        y=orders_by_day_this["orders"],
                        name="Tuần này",
                        marker_color="#7C3AED"
                    ))
                    fig_orders.update_layout(
                        title="Orders theo ngày",
                        barmode="group",
                        height=320,
                        margin=dict(l=0, r=0, t=40, b=0),
                        legend=dict(orientation="h", yanchor="bottom",
                                    y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_orders, use_container_width=True)

            with st.container(border=True):
                # Donut chart cancel rate
                chart_col3, chart_col4 = st.columns(2)

                with chart_col3:
                    fig_donut = go.Figure(data=[go.Pie(
                        labels=["Completed / Other", "Cancelled"],
                        values=[
                            orders_this_week_tt - orders_cancelled_this_week_tt,
                            orders_cancelled_this_week_tt
                        ],
                        hole=0.6,
                        marker_colors=["#2563EB", "#DC2626"]
                    )])
                    fig_donut.update_layout(
                        title=f"Tỷ lệ Cancelled tuần này ({cancel_rate_this_week_tt:.1f}%)",
                        height=320,
                        margin=dict(l=0, r=0, t=40, b=0),
                        showlegend=True
                    )
                    st.plotly_chart(fig_donut, use_container_width=True)

                with chart_col4:
                    fig_donut2 = go.Figure(data=[go.Pie(
                        labels=["Completed / Other", "Cancelled"],
                        values=[
                            orders_last_week_tt - orders_cancelled_last_week_tt,
                            orders_cancelled_last_week_tt
                        ],
                        hole=0.6,
                        marker_colors=["#CBD5E1", "#FCA5A5"]
                    )])
                    fig_donut2.update_layout(
                        title=f"Tỷ lệ Cancelled tuần trước ({cancel_rate_last_week_tt:.1f}%)",
                        height=320,
                        margin=dict(l=0, r=0, t=40, b=0),
                        showlegend=True
                    )
                    st.plotly_chart(fig_donut2, use_container_width=True)

            # =====================================================
            # TOP PRODUCTS CHART + TABLE
            # =====================================================
            st.markdown("""
            <div class="kpi-card">
                <div class="section-title">
                    🏆 Top 10 sản phẩm theo GMV (tuần này)
                </div>
                <div class="section-subtitle">
                    Advanced order performance & revenue insights
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):

                # Tính tỷ trọng GMV
                top_products_tt = top_products_tt.copy()
                total_nmv = top_products_tt["nmv"].sum()

                top_products_tt["percent"] = (
                    top_products_tt["nmv"] / total_nmv * 100
                ).round(1)

                # Rút gọn tên sản phẩm
                top_products_tt["short_name"] = (
                    top_products_tt["SKU Category"]
                    .str.replace("\n", " ", regex=False)
                    .str.slice(0, 28)
                )

                fig_top = px.treemap(
                    top_products_tt,
                    path=["short_name"],
                    values="nmv",
                    color="nmv",
                    color_continuous_scale=[
                        "#00441A",
                        "#797700",
                        "#60A5FA",
                        "#2563EB",
                        "#1E40AF"
                    ],
                    custom_data=[
                        "SKU Category",
                        "orders",
                        "percent"
                    ]
                )

                fig_top.update_traces(

                    marker=dict(
                        line=dict(
                            color="white",
                            width=2
                        )
                    ),

                    texttemplate=(
                        "<b>%{label}</b>"
                        "<br>%{customdata[2]}%"
                    ),

                    textfont=dict(
                        family="Inter",
                        size=14,
                        color="white"
                    ),

                    textposition="middle center",

                    hovertemplate=(
                        "<b>%{customdata[0]}</b><br><br>"
                        "NMV: %{value:,.0f}₫<br>"
                        "Orders: %{customdata[1]:,}<br>"
                        "Tỷ trọng: %{customdata[2]}%"
                        "<extra></extra>"
                    ),

                    root_color="rgba(0,0,0,0)"
                )

                fig_top.update_layout(

                    height=520,

                    margin=dict(
                        l=5,
                        r=5,
                        t=10,
                        b=5
                    ),

                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",

                    coloraxis_showscale=False,

                    uniformtext=dict(
                        minsize=11,
                        mode="hide"
                    ),

                    hoverlabel=dict(
                        bgcolor="white",
                        font_size=13,
                        font_family="Inter",
                        font_color="#111827"
                    ),

                    font=dict(
                        family="Inter",
                        color="#111827"
                    )
                )

                st.plotly_chart(fig_top, use_container_width=True)

    # =========================
    # SHOPEE UI
    # =========================
    elif platform == "Shopee":
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h1 style="
                font-size:38px;
                font-weight:800;
                color:#111;
                margin-bottom:5px;
            ">
                📈 Shopee Weekly Report
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

        # Upload file
        uploaded_file = st.sidebar.file_uploader(
            "Upload File Shopee (XLSX) At Here", type="xlsx", key="xlsx_upload_sidebar"
        )
        uploaded_file_ads = st.sidebar.file_uploader(
            "Upload File Shopee Ads CSV At Here", type="csv", key="csv_upload_sidebar"
        )

        if uploaded_file and uploaded_file_ads:
            st.sidebar.success("XLSX Uploaded!")
            if st.sidebar.button("Check GMV Now"):
                shoppe_data = read_file_shopee(uploaded_file)
                st.session_state.shoppe_data = shoppe_data
                st.session_state.shoppe_ads_data = pd.read_csv(
                    uploaded_file_ads, skiprows=7)

        if "shoppe_data" in st.session_state:
            import plotly.graph_objects as go

            data_shopee = st.session_state["shoppe_data"]
            df_this_week, df_last_week, current, previous = kpi_shopee(
                data_shopee)

            # =====================================================
            # GMV
            # =====================================================
            gmv_this_week = df_this_week["Tổng số tiền Người mua thanh toán"].sum(
            )
            gmv_last_week = df_last_week["Tổng số tiền Người mua thanh toán"].sum(
            )

            # =====================================================
            # NMV
            # =====================================================
            df_valid_this_week = df_this_week[df_this_week["Actually type"] != "Đã hủy"]
            df_valid_last_week = df_last_week[df_last_week["Actually type"] != "Đã hủy"]

            nmv_this_week = (
                df_valid_this_week["Tổng số tiền Người mua thanh toán"].sum()
                - df_valid_this_week["Mã giảm giá của Shop"].sum()
            )
            nmv_last_week = (
                df_valid_last_week["Tổng số tiền Người mua thanh toán"].sum()
                - df_valid_last_week["Mã giảm giá của Shop"].sum()
            )

            # =====================================================
            # ORDERS
            # =====================================================
            orders_this_week = df_this_week["Mã đơn hàng"].nunique()
            orders_last_week = df_last_week["Mã đơn hàng"].nunique()

            # =====================================================
            # CANCELLED
            # =====================================================
            orders_cancelled_this_week = df_this_week[
                df_this_week["Actually type"] == "Đã hủy"
            ]["Mã đơn hàng"].nunique()
            orders_cancelled_last_week = df_last_week[
                df_last_week["Actually type"] == "Đã hủy"
            ]["Mã đơn hàng"].nunique()

            # =====================================================
            # AOV
            # =====================================================
            aov_this_week = gmv_this_week / orders_this_week if orders_this_week != 0 else 0
            aov_last_week = gmv_last_week / orders_last_week if orders_last_week != 0 else 0

            # =====================================================
            # RATES
            # =====================================================
            nmv_rate_this_week = (nmv_this_week / gmv_this_week *
                                  100) if gmv_this_week != 0 else 0
            nmv_rate_last_week = (nmv_last_week / gmv_last_week *
                                  100) if gmv_last_week != 0 else 0
            cancel_rate_this_week = (orders_cancelled_this_week /
                                     orders_this_week * 100) if orders_this_week != 0 else 0
            cancel_rate_last_week = (orders_cancelled_last_week /
                                     orders_last_week * 100) if orders_last_week != 0 else 0

            # =====================================================
            # WOW
            # =====================================================
            wow_gmv = ((gmv_this_week - gmv_last_week) /
                       gmv_last_week * 100) if gmv_last_week != 0 else 0
            wow_nmv = ((nmv_this_week - nmv_last_week) /
                       nmv_last_week * 100) if nmv_last_week != 0 else 0
            wow_orders = ((orders_this_week - orders_last_week) /
                          orders_last_week * 100) if orders_last_week != 0 else 0
            wow_aov = ((aov_this_week - aov_last_week) /
                       aov_last_week * 100) if aov_last_week != 0 else 0
            wow_cancelled = ((orders_cancelled_this_week - orders_cancelled_last_week) /
                             orders_cancelled_last_week * 100) if orders_cancelled_last_week != 0 else 0
            cancel_rate_delta = cancel_rate_this_week - cancel_rate_last_week
            nmv_rate_delta = nmv_rate_this_week - nmv_rate_last_week

            # =====================================================
            # WEEK LABELS
            # =====================================================
            current_week = int(current["week"])
            current_year = int(current["year"])
            previous_week = int(previous["week"])
            previous_year = int(previous["year"])

            current_start = df_this_week["Ngày đặt hàng"].min().strftime(
                "%d/%m")
            current_end = df_this_week["Ngày đặt hàng"].max().strftime(
                "%d/%m/%Y")
            previous_start = df_last_week["Ngày đặt hàng"].min().strftime(
                "%d/%m")
            previous_end = df_last_week["Ngày đặt hàng"].max().strftime(
                "%d/%m/%Y")

            # =====================================================
            # SKU GMV / NMV
            # =====================================================
            sku_gmv = (
                df_this_week
                .groupby("SKU Category", as_index=False)["Tổng số tiền Người mua thanh toán"]
                .sum()
                .rename(columns={"Tổng số tiền Người mua thanh toán": "GMV"})
            )
            sku_nmv = (
                df_valid_this_week
                .groupby("SKU Category", as_index=False)["Tổng số tiền Người mua thanh toán"]
                .sum()
                .rename(columns={"Tổng số tiền Người mua thanh toán": "NMV"})
            )
            sku_metrics = (
                sku_gmv.merge(sku_nmv, on="SKU Category", how="left")
                .fillna(0)
                .sort_values("GMV", ascending=False)
                .head(8)
            )
            total_gmv_all = sku_metrics["GMV"].sum()
            sku_metrics["GMV_pct"] = sku_metrics["GMV"] / \
                total_gmv_all * 100 if total_gmv_all != 0 else 0

            # =====================================================
            # CHART DATA
            # =====================================================
            gmv_by_day_this = (
                df_this_week.groupby(df_this_week["Ngày đặt hàng"].dt.date)[
                    "Tổng số tiền Người mua thanh toán"]
                .sum().reset_index()
            )
            gmv_by_day_this.columns = ["date", "gmv"]

            gmv_by_day_last = (
                df_last_week.groupby(df_last_week["Ngày đặt hàng"].dt.date)[
                    "Tổng số tiền Người mua thanh toán"]
                .sum().reset_index()
            )
            gmv_by_day_last.columns = ["date", "gmv"]

            orders_by_day_this = (
                df_this_week.groupby(df_this_week["Ngày đặt hàng"].dt.date)[
                    "Mã đơn hàng"]
                .nunique().reset_index()
            )
            orders_by_day_this.columns = ["date", "orders"]

            orders_by_day_last = (
                df_last_week.groupby(df_last_week["Ngày đặt hàng"].dt.date)[
                    "Mã đơn hàng"]
                .nunique().reset_index()
            )
            orders_by_day_last.columns = ["date", "orders"]

            # =====================================================
            # FEES
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
            # HEADER UI
            # =====================================================
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #EE4D2D 0%, #FF7337 50%, #FFB347 100%);
                padding:12px 18px;
                border-radius:18px;
                margin-bottom:18px;
                color:white;
                box-shadow: 0 6px 20px rgba(238,77,45,0.25);
            ">
                <div style="font-size:12px;opacity:0.85;font-weight:700;letter-spacing:1px;text-transform:uppercase;">
                    🛒 Shopee Weekly Performance
                </div>
                <div style="margin-top:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                    <div>
                        <div style="font-size:22px;font-weight:800;line-height:1.1;">
                            Week {current_week} - {current_year}
                        </div>
                        <div style="font-size:13px;opacity:0.92;margin-top:4px;">
                            📅 {current_start} → {current_end}
                        </div>
                    </div>
                    <div style="background:rgba(255,255,255,0.18);padding:10px 14px;border-radius:14px;backdrop-filter:blur(6px);">
                        <div style="font-size:11px;opacity:0.85;font-weight:600;text-transform:uppercase;">Compare To</div>
                        <div style="font-size:15px;font-weight:700;margin-top:2px;">Week {previous_week} - {previous_year}</div>
                        <div style="font-size:12px;opacity:0.9;margin-top:2px;">{previous_start} → {previous_end}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # =====================================================
            # KPI ROW 1
            # =====================================================
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">💰</div></div>
                    <div class="kpi-title">GMV TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#EE4D2D;">{gmv_this_week:,.0f}₫</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{gmv_last_week:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if wow_gmv >= 0 else 'metric-tag-red'}">
                        {'▲' if wow_gmv >= 0 else '▼'} {wow_gmv:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">💵</div></div>
                    <div class="kpi-title">NMV TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#0F766E;">{nmv_this_week:,.0f}₫</div>
                    <div style="font-size:13px;color:#64748b;margin-bottom:8px;">
                        Tuần trước: <b>{nmv_last_week:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if wow_nmv >= 0 else 'metric-tag-red'}">
                        {'▲' if wow_nmv >= 0 else '▼'} {wow_nmv:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">📦</div></div>
                    <div class="kpi-title">ORDERS TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#7C3AED;">{orders_this_week:,}</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{orders_last_week:,}</b>
                    </div>
                    <div class="{'metric-tag-green' if wow_orders >= 0 else 'metric-tag-red'}">
                        {'▲' if wow_orders >= 0 else '▼'} {wow_orders:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">💸</div></div>
                    <div class="kpi-title">FEES TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#DC2626;">{fees_predicted:,.0f}₫</div>
                    <div style="font-size:12px;color:#64748b;margin-bottom:12px;">
                        Fixed + Service + Transaction + Piship
                    </div>
                    <div style="display:inline-block;padding:6px 14px;border-radius:999px;
                        background:#FEF3C7;color:#B45309;font-size:13px;font-weight:700;">
                        Chi phí ước tính
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # =====================================================
            # KPI ROW 2: AOV + CANCEL + RATES
            # =====================================================
            st.markdown("<div style='margin-top:16px;'></div>",
                        unsafe_allow_html=True)

            col5, col6, col7 = st.columns(3)

            with col5:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">🛒</div></div>
                    <div class="kpi-title">AOV TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#D97706;">{aov_this_week:,.0f}₫</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{aov_last_week:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if wow_aov >= 0 else 'metric-tag-red'}">
                        {'▲' if wow_aov >= 0 else '▼'} {wow_aov:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col6:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">❌</div></div>
                    <div class="kpi-title">CANCELLED TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#DC2626;">{orders_cancelled_this_week:,}</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:8px;">
                        Tuần trước: <b>{orders_cancelled_last_week:,}</b>
                    </div>
                    <div class="{'metric-tag-red' if wow_cancelled >= 0 else 'metric-tag-green'}">
                        {'▲' if wow_cancelled >= 0 else '▼'} {wow_cancelled:+.2f}% vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col7:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">✅</div></div>
                    <div class="kpi-title">NMV RATE TUẦN NÀY</div>
                    <div class="kpi-value" style="color:#0F766E;">{nmv_rate_this_week:.1f}%</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tuần trước: <b>{nmv_rate_last_week:.1f}%</b>
                    </div>
                    <div class="{'metric-tag-green' if nmv_rate_delta >= 0 else 'metric-tag-red'}">
                        {'▲' if nmv_rate_delta >= 0 else '▼'} {nmv_rate_delta:+.2f}pp vs Tuần trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # =====================================================
            # CHARTS
            # =====================================================

            st.markdown("""
            <div class="kpi-card">
                <div class="section-title">
                    📈 Biểu đồ theo ngày
                </div>
                <div class="section-subtitle">
                    Advanced order performance & revenue insights
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    fig_gmv = go.Figure()
                    fig_gmv.add_trace(go.Bar(
                        x=[str(d) for d in gmv_by_day_last["date"]],
                        y=gmv_by_day_last["gmv"],
                        name="Tuần trước",
                        marker_color="#FDBA74"
                    ))
                    fig_gmv.add_trace(go.Bar(
                        x=[str(d) for d in gmv_by_day_this["date"]],
                        y=gmv_by_day_this["gmv"],
                        name="Tuần này",
                        marker_color="#EE4D2D"
                    ))
                    fig_gmv.update_layout(
                        title="GMV theo ngày",
                        barmode="group",
                        height=320,
                        margin=dict(l=0, r=0, t=40, b=0),
                        legend=dict(orientation="h", yanchor="bottom",
                                    y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_gmv, use_container_width=True)

                with chart_col2:
                    fig_orders = go.Figure()
                    fig_orders.add_trace(go.Bar(
                        x=[str(d) for d in orders_by_day_last["date"]],
                        y=orders_by_day_last["orders"],
                        name="Tuần trước",
                        marker_color="#CBD5E1"
                    ))
                    fig_orders.add_trace(go.Bar(
                        x=[str(d) for d in orders_by_day_this["date"]],
                        y=orders_by_day_this["orders"],
                        name="Tuần này",
                        marker_color="#7C3AED"
                    ))
                    fig_orders.update_layout(
                        title="Orders theo ngày",
                        barmode="group",
                        height=320,
                        margin=dict(l=0, r=0, t=40, b=0),
                        legend=dict(orientation="h", yanchor="bottom",
                                    y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_orders, use_container_width=True)
            with st.container(border=True):
                chart_col3, chart_col4 = st.columns(2)

                with chart_col3:
                    fig_donut = go.Figure(data=[go.Pie(
                        labels=["Hoàn thành", "Đã hủy"],
                        values=[orders_this_week - orders_cancelled_this_week,
                                orders_cancelled_this_week],
                        hole=0.6,
                        marker_colors=["#EE4D2D", "#FCA5A5"]
                    )])
                    fig_donut.update_layout(
                        title=f"Cancel Rate tuần này ({cancel_rate_this_week:.1f}%)",
                        height=300,
                        margin=dict(l=0, r=0, t=40, b=0)
                    )
                    st.plotly_chart(fig_donut, use_container_width=True)

                with chart_col4:
                    fig_sku = go.Figure(go.Bar(
                        x=sku_metrics["GMV"] / 1_000_000,
                        y=sku_metrics["SKU Category"],
                        orientation="h",
                        marker_color="#EE4D2D",
                        text=[f"{v:.1f}M ({p:.1f}%)" for v, p in zip(
                            sku_metrics["GMV"] / 1_000_000,
                            sku_metrics["GMV_pct"]
                        )],
                        textposition="outside"
                    ))
                    fig_sku.update_layout(
                        title="GMV theo SKU (triệu ₫)",
                        height=300,
                        margin=dict(l=0, r=120, t=40, b=0),
                        xaxis_title="GMV (triệu ₫)",
                        yaxis=dict(autorange="reversed")
                    )
                    st.plotly_chart(fig_sku, use_container_width=True)

            # =====================================================
            # SKU CARDS
            # =====================================================

            st.markdown("""
            <div class="kpi-card">
                <div class="section-title">
                    🛒 Top SKU GMV
                </div>
                <div class="section-subtitle">
                    Advanced order performance & revenue insights
                </div>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(8)
            for idx, (_, row) in enumerate(sku_metrics.iterrows()):
                sku_name = row["SKU Category"]
                if len(sku_name) > 22:
                    sku_name = sku_name[:22] + "..."
                gmv = row["GMV"]
                nmv = row["NMV"]
                pct = row["GMV_pct"]

                with cols[idx % 8]:
                    st.markdown(f"""
                    <div style="
                        background:white;border:1px solid #E2E8F0;border-radius:16px;
                        padding:18px 10px;height:200px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.04);
                        display:flex;flex-direction:column;justify-content:space-between;
                        margin-top:10px;
                    ">
                        <div style="font-size:12px;font-weight:700;color:#64748B;">TOP #{idx+1}</div>
                        <div style="font-size:12px;font-weight:700;color:#0F172A;line-height:1.35;">{sku_name}</div>
                        <div>
                            <div style="font-size:22px;font-weight:800;color:#EE4D2D;line-height:1;margin-top:6px;">
                                {gmv/1_000_000:.1f}M
                            </div>
                            <div style="font-size:11px;color:#94A3B8;font-weight:600;margin-top:2px;">GMV</div>
                            <div style="font-size:11px;color:#EE4D2D;font-weight:700;margin-top:2px;">{pct:.1f}% tổng</div>
                        </div>
                        <div style="margin-top:8px;padding-top:8px;border-top:1px solid #F1F5F9;">
                            <div style="font-size:18px;font-weight:700;color:#0F766E;line-height:1;">
                                {nmv/1_000_000:.1f}M
                            </div>
                            <div style="font-size:11px;color:#15803d;font-weight:600;margin-top:2px;">NMV</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()

            # =====================================================
            # ADS SECTION
            # =====================================================
            df_ads = st.session_state.shoppe_ads_data

            st.markdown("""
            <div class="kpi-card">
                <div class="section-title">
                    📊 Ads Performance Overview
                </div>
                <div class="section-subtitle">
                    Advanced order performance & revenue insights
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">💸 Ad Spend</div>
                    <div class="kpi-value" style="color:#DC2626;">{df_ads["Chi phí"].iloc[0]:,.0f}₫</div>
                    <div class="metric-tag-red">Chi phí chạy ads</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">🛒 GMV Ads</div>
                    <div class="kpi-value" style="color:#EE4D2D;">{df_ads["Doanh số"].iloc[0]:,.0f}₫</div>
                    <div class="metric-tag-green">Doanh số ghi nhận</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">👀 Impressions</div>
                    <div class="kpi-value" style="color:#2563EB;">{df_ads["Số lượt xem"].iloc[0]:,}</div>
                    <div class="metric-tag-green">Số lần hiển thị</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">👆 Clicks</div>
                    <div class="kpi-value" style="color:#7C3AED;">{df_ads["Số lượt click"].iloc[0]:,}</div>
                    <div class="metric-tag-green">Lượt nhấp</div>
                </div>
                """, unsafe_allow_html=True)

            with col5:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">🚀 ROAS</div>
                    <div class="kpi-value" style="color:#7C3AED;">{df_ads["ROAS"].iloc[0]}</div>
                    <div class="metric-tag-green">Hiệu quả QC</div>
                </div>
                """, unsafe_allow_html=True)

            with col6:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">📦 Products Sold</div>
                    <div class="kpi-value" style="color:#DC2626;">{df_ads["Sản phẩm đã bán"].iloc[0]:,}</div>
                    <div class="metric-tag-red">Sản phẩm đã bán</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px;'></div>",
                        unsafe_allow_html=True)
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            def metric_tile(icon, label, value, bg, border, color, sub):
                return f"""
                <div style="background:{bg};border-left:4px solid {border};border-radius:12px;
                    padding:12px;height:105px;">
                    <div style="font-size:12px;color:#64748B;">{icon} {label}</div>
                    <div style="font-size:22px;font-weight:800;color:{color};margin-top:6px;">{value}</div>
                    <div style="font-size:11px;color:#64748B;margin-top:8px;">{sub}</div>
                </div>"""

            ctr = df_ads["Tỷ Lệ Click"].iloc[0]
            cvr = df_ads["Tỷ lệ chuyển đổi"].iloc[0]
            cpa = df_ads["Chi phí cho mỗi lượt chuyển đổi"].iloc[0]
            cpm = (df_ads["Chi phí"].iloc[0] /
                   df_ads["Số lượt xem"].iloc[0]) * 1000
            aov_ads = df_ads["Doanh số"].iloc[0] / \
                df_ads["Sản phẩm đã bán"].iloc[0]
            cpc = df_ads["Chi phí"].iloc[0] / df_ads["Số lượt click"].iloc[0]

            with col1:
                st.markdown(metric_tile("🎯", "CTR", ctr, "#F0F9FF", "#0891B2",
                            "#0891B2", "Tỷ lệ nhấp"), unsafe_allow_html=True)

            with col2:
                st.markdown(metric_tile("🔥", "CVR", cvr, "#F0FDF4", "#16A34A",
                            "#16A34A", "Tỷ lệ chuyển đổi"), unsafe_allow_html=True)

            with col3:
                st.markdown(metric_tile("💰", "CPA", f"{cpa:,.0f}₫", "#FEF2F2",
                            "#DC2626", "#DC2626", "Chi phí / đơn"), unsafe_allow_html=True)

            with col4:
                st.markdown(metric_tile("📈", "CPM", f"{cpm:,.0f}₫", "#FAF5FF", "#7C3AED",
                            "#7C3AED", "Chi phí / 1000 views"), unsafe_allow_html=True)

            with col5:
                st.markdown(metric_tile("🛍️", "AOV", f"{aov_ads:,.0f}₫", "#EFF6FF",
                            "#2563EB", "#2563EB", "Giá trị đơn TB"), unsafe_allow_html=True)

            with col6:
                st.markdown(metric_tile("💵", "CPC", f"{cpc:,.0f}₫", "#FFFBEB",
                            "#F59E0B", "#F59E0B", "Chi phí / click"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(st.session_state.shoppe_ads_data,
                         use_container_width=True)
