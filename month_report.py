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

        # Process data
        df = process_tiktok_data(df).copy()

        df["Created Time"] = pd.to_datetime(df["Created Time"])
        df["year"] = df["Created Time"].dt.year
        df["month"] = df["Created Time"].dt.month

        # Danh sách các tháng có dữ liệu
        months = (
            df[["year", "month"]]
            .drop_duplicates()
            .sort_values(["year", "month"])
            .reset_index(drop=True)
        )

        # Phải có ít nhất 2 tháng
        if len(months) < 2:
            raise ValueError("Dataset cần có ít nhất 2 tháng dữ liệu.")

        current_tt = months.iloc[-1]
        previous_tt = months.iloc[-2]

        current_year = int(current_tt["year"])
        current_month = int(current_tt["month"])

        previous_year = int(previous_tt["year"])
        previous_month = int(previous_tt["month"])

        # Data tháng hiện tại
        df_this_month = df[
            (df["year"] == current_year)
            & (df["month"] == current_month)
        ].copy()

        # Data tháng trước
        df_last_month = df[
            (df["year"] == previous_year)
            & (df["month"] == previous_month)
        ].copy()

        return df_this_month, df_last_month, current_tt, previous_tt

    def kpi_shopee_month(df: pd.DataFrame):

        # =========================
        # PROCESS DATA
        # =========================
        df_new = process_shopee_data(df)

        df_new["Ngày đặt hàng"] = pd.to_datetime(
            df_new["Ngày đặt hàng"],
            errors="coerce"
        )

        # =========================
        # YEAR / MONTH
        # =========================
        df_new["year"] = df_new["Ngày đặt hàng"].dt.year
        df_new["month"] = df_new["Ngày đặt hàng"].dt.month

        # =========================
        # GET ALL MONTHS
        # =========================
        all_months = (
            df_new[["year", "month"]]
            .drop_duplicates()
            .sort_values(["year", "month"])
            .reset_index(drop=True)
        )

        if len(all_months) < 2:
            return df_new, pd.DataFrame(), all_months

        # =========================
        # THIS MONTH
        # =========================
        current = all_months.iloc[-1]

        df_this_month = df_new[
            (df_new["year"] == current["year"]) &
            (df_new["month"] == current["month"])
        ].copy()

        # =========================
        # LAST MONTH
        # =========================
        previous = all_months.iloc[-2]

        df_last_month = df_new[
            (df_new["year"] == previous["year"]) &
            (df_new["month"] == previous["month"])
        ].copy()

        return df_this_month, df_last_month, current, previous

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
                🗓️ Tiktok Monthly Report
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

            if st.sidebar.button("Check Now"):
                try:
                    df_month = read_file_tiktok(uploaded_file)
                    st.session_state.df_month = df_month
                except Exception as e:
                    st.sidebar.error(f"Cannot read file: {e}")

        if "df_month" in st.session_state:
            df_month = st.session_state["df_month"].copy()

            df_this_month_tt, df_last_month_tt, current_tt, previous_tt = kpi_tiktok(
                df_month)

            current_month_tt = int(current_tt["month"])
            current_year_tt = int(current_tt["year"])
            previous_month_tt = int(previous_tt["month"])
            previous_year_tt = int(previous_tt["year"])

            # Khoảng thời gian
            current_start_tt = df_this_month_tt["Created Time"].min().strftime(
                "%d/%m/%Y")
            current_end_tt = df_this_month_tt["Created Time"].max().strftime(
                "%d/%m/%Y")
            previous_start_tt = df_last_month_tt["Created Time"].min().strftime(
                "%d/%m/%Y")
            previous_end_tt = df_last_month_tt["Created Time"].max().strftime(
                "%d/%m/%Y")

            #
            #  =====================================================
            # GMV - Gross Merchandise Value
            # =====================================================
            gmv_this_month_tt = df_this_month_tt["SKU Subtotal After Discount"].sum(
            )
            gmv_last_month_tt = df_last_month_tt["SKU Subtotal After Discount"].sum(
            )

            # =====================================================
            # NMV - Net Merchandise Value
            # =====================================================
            df_valid_this_month_tt = df_this_month_tt[
                df_this_month_tt["Order Status"] != "Cancelled"
            ]

            df_valid_last_month_tt = df_last_month_tt[
                df_last_month_tt["Order Status"] != "Cancelled"
            ]

            nmv_this_month_tt = df_valid_this_month_tt["SKU Subtotal After Discount"].sum(
            )
            nmv_last_month_tt = df_valid_last_month_tt["SKU Subtotal After Discount"].sum(
            )

            # =====================================================
            # ORDERS
            # =====================================================
            orders_this_month_tt = df_this_month_tt["Order ID"].nunique()
            orders_last_month_tt = df_last_month_tt["Order ID"].nunique()

            # =====================================================
            # MOM (Month over Month)
            # =====================================================
            gmv_mom_tt = (
                (gmv_this_month_tt - gmv_last_month_tt)
                / gmv_last_month_tt * 100
            ) if gmv_last_month_tt != 0 else 0

            nmv_mom_tt = (
                (nmv_this_month_tt - nmv_last_month_tt)
                / nmv_last_month_tt * 100
            ) if nmv_last_month_tt != 0 else 0

            orders_mom_tt = (
                (orders_this_month_tt - orders_last_month_tt)
                / orders_last_month_tt * 100
            ) if orders_last_month_tt != 0 else 0

            # =====================================================
            # Cancelled Orders
            # =====================================================
            orders_cancelled_this_month_tt = (
                df_this_month_tt[
                    df_this_month_tt["Order Status"] == "Cancelled"
                ]["Order ID"].nunique()
            )

            orders_cancelled_last_month_tt = (
                df_last_month_tt[
                    df_last_month_tt["Order Status"] == "Cancelled"
                ]["Order ID"].nunique()
            )

            orders_cancelled_mom_tt = (
                (orders_cancelled_this_month_tt - orders_cancelled_last_month_tt)
                / orders_cancelled_last_month_tt * 100
            ) if orders_cancelled_last_month_tt != 0 else 0

            # =====================================================
            # AOV
            # =====================================================
            aov_this_month_tt = (
                gmv_this_month_tt / orders_this_month_tt
                if orders_this_month_tt != 0 else 0
            )

            aov_last_month_tt = (
                gmv_last_month_tt / orders_last_month_tt
                if orders_last_month_tt != 0 else 0
            )

            aov_mom_tt = (
                (aov_this_month_tt - aov_last_month_tt)
                / aov_last_month_tt * 100
            ) if aov_last_month_tt != 0 else 0

            # =====================================================
            # Cancellation Rate
            # =====================================================
            cancel_rate_this_month_tt = (
                orders_cancelled_this_month_tt
                / orders_this_month_tt * 100
            ) if orders_this_month_tt != 0 else 0

            cancel_rate_last_month_tt = (
                orders_cancelled_last_month_tt
                / orders_last_month_tt * 100
            ) if orders_last_month_tt != 0 else 0

            cancel_rate_mom_tt = (
                cancel_rate_this_month_tt
                - cancel_rate_last_month_tt
            )

            # =====================================================
            # NMV Rate
            # =====================================================
            nmv_rate_this_month_tt = (
                nmv_this_month_tt
                / gmv_this_month_tt * 100
            ) if gmv_this_month_tt != 0 else 0

            nmv_rate_last_month_tt = (
                nmv_last_month_tt
                / gmv_last_month_tt * 100
            ) if gmv_last_month_tt != 0 else 0

            # =====================================================
            # CHART DATA - GMV theo ngày
            # =====================================================
            gmv_by_day_this = (
                df_this_month_tt
                .groupby(df_this_month_tt["Created Time"].dt.date)[
                    "SKU Subtotal After Discount"
                ]
                .sum()
                .reset_index()
            )
            gmv_by_day_this.columns = ["date", "gmv"]
            gmv_by_day_this["label"] = "Tháng này"

            gmv_by_day_last = (
                df_last_month_tt
                .groupby(df_last_month_tt["Created Time"].dt.date)[
                    "SKU Subtotal After Discount"
                ]
                .sum()
                .reset_index()
            )
            gmv_by_day_last.columns = ["date", "gmv"]
            gmv_by_day_last["label"] = "Tháng trước"

            # =====================================================
            # CHART DATA - Orders theo ngày
            # =====================================================
            orders_by_day_this = (
                df_this_month_tt
                .groupby(df_this_month_tt["Created Time"].dt.date)["Order ID"]
                .nunique()
                .reset_index()
            )
            orders_by_day_this.columns = ["date", "orders"]
            orders_by_day_this["label"] = "Tháng này"

            orders_by_day_last = (
                df_last_month_tt
                .groupby(df_last_month_tt["Created Time"].dt.date)["Order ID"]
                .nunique()
                .reset_index()
            )
            orders_by_day_last.columns = ["date", "orders"]
            orders_by_day_last["label"] = "Tháng trước"

            # =====================================================
            # WEEK BREAKDOWN
            # =====================================================
            df_week_tt = df_this_month_tt.copy()

            df_week_tt["Day"] = df_week_tt["Created Time"].dt.day

            df_week_tt["Week No"] = ((df_week_tt["Day"] - 1) // 7) + 1

            df_week_tt["Week"] = "Week " + df_week_tt["Week No"].astype(str)

            week_breakdown_tt = (
                df_week_tt.groupby("Week No")
                .agg(
                    StartDate=("Created Time", "min"),
                    EndDate=("Created Time", "max"),
                    GMV=("SKU Subtotal After Discount", "sum"),
                    Orders=("Order ID", "nunique"),
                )
                .reset_index()
            )

            week_breakdown_tt["Week"] = (
                "Week "
                + week_breakdown_tt["Week No"].astype(str)
                + "<br>"
                + week_breakdown_tt["StartDate"].dt.strftime("%d/%m")
                + " - "
                + week_breakdown_tt["EndDate"].dt.strftime("%d/%m")
            )

            week_breakdown_tt["AOV"] = (
                week_breakdown_tt["GMV"]
                / week_breakdown_tt["Orders"]
            )

            avg = week_breakdown_tt["GMV"].mean()

            # =====================================================
            # HEADER UI - COMPACT VERSION
            # =====================================================
            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,#0F172A,#1D4ED8,#2563EB);
                border-radius:18px;
                padding:22px 26px;
                color:white;
                margin-bottom:20px;
                box-shadow:0 10px 30px rgba(0,0,0,.18);
            ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                flex-wrap:wrap;
                gap:20px;
            ">
                <!-- Left -->
                <div>
                    <div style="
                        font-size:13px;
                        opacity:.85;
                        text-transform:uppercase;
                        font-weight:700;
                        letter-spacing:1px;
                    ">
                        📅 Monthly Performance Report
                    </div>
                    <div style="
                        font-size:34px;
                        font-weight:800;
                        margin-top:6px;
                        line-height:1;
                    ">
                        {current_month_tt:02d}/{current_year_tt}
                    </div>
                    <div style="
                        margin-top:8px;
                        font-size:15px;
                        opacity:.92;
                    ">
                        {current_start_tt} → {current_end_tt}
                    </div>
                </div>
                <!-- Right -->
                <div style="
                    background:rgba(255,255,255,.12);
                    border:1px solid rgba(255,255,255,.15);
                    border-radius:16px;
                    padding:16px 20px;
                    min-width:240px;
                    backdrop-filter: blur(10px);
                ">
                    <div style="
                        font-size:12px;
                        opacity:.8;
                        text-transform:uppercase;
                        font-weight:700;
                        margin-bottom:8px;
                    ">
                        Compare with
                    </div>
                    <div style="
                        font-size:24px;
                        font-weight:700;
                    ">
                        {previous_month_tt:02d}/{previous_year_tt}
                    </div>
                    <div style="
                        margin-top:6px;
                        font-size:14px;
                        opacity:.9;
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
                    <div class="kpi-title">GMV THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#2563EB;">{gmv_this_month_tt:,.0f}₫</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{gmv_last_month_tt:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if gmv_mom_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if gmv_mom_tt >= 0 else '▼'} {gmv_mom_tt:+.2f}% vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">💵</div></div>
                    <div class="kpi-title">NMV THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#0F766E;">{nmv_this_month_tt:,.0f}₫</div>
                    <div style="font-size:13px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{nmv_last_month_tt:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if nmv_mom_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if nmv_mom_tt >= 0 else '▼'} {nmv_mom_tt:+.2f}% vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">📦</div></div>
                    <div class="kpi-title">ORDERS THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#7C3AED;">{orders_this_month_tt:,}</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{orders_last_month_tt:,}</b>
                    </div>
                    <div class="{'metric-tag-green' if orders_mom_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if orders_mom_tt >= 0 else '▼'} {orders_mom_tt:+.2f}% vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">❌</div></div>
                    <div class="kpi-title">CANCELLED THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#DC2626;">{orders_cancelled_this_month_tt:,}</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{orders_cancelled_last_month_tt:,}</b>
                    </div>
                    <div class="{'metric-tag-green' if orders_cancelled_mom_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if orders_cancelled_mom_tt >= 0 else '▼'} {orders_cancelled_mom_tt:+.2f}% vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)
            # =======================================

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
                    <div class="kpi-title">AOV THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#D97706;">{aov_this_month_tt:,.0f}₫</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{aov_last_month_tt:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if aov_mom_tt >= 0 else 'metric-tag-red'}">
                        {'▲' if aov_mom_tt >= 0 else '▼'} {aov_mom_tt:+.2f}% vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col6:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">✅</div></div>
                    <div class="kpi-title">NMV RATE THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#0F766E;">{nmv_rate_this_month_tt:.1f}%</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{nmv_rate_last_month_tt:.1f}%</b>
                    </div>
                    <div class="{'metric-tag-green' if nmv_rate_this_month_tt >= nmv_rate_last_month_tt else 'metric-tag-red'}">
                        {'▲' if nmv_rate_this_month_tt >= nmv_rate_last_month_tt else '▼'}
                        {nmv_rate_this_month_tt - nmv_rate_last_month_tt:+.2f}pp vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col7:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">📉</div></div>
                    <div class="kpi-title">CANCEL RATE THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#DC2626;">{cancel_rate_this_month_tt:.1f}%</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{cancel_rate_last_month_tt:.1f}%</b>
                    </div>
                    <div class="{'metric-tag-red' if cancel_rate_mom_tt >= 0 else 'metric-tag-green'}">
                        {'▲' if cancel_rate_mom_tt >= 0 else '▼'}
                        {cancel_rate_mom_tt:+.2f}pp vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # =====================================================
            # CHARTS
            # =====================================================
            st.markdown("""
            <div class="kpi-card">
                <div class="section-title">
                    📈 Biểu đồ theo ngày trong tháng
                </div>
                <div class="section-subtitle">
                    Month-over-Month Revenue & Order Performance
                </div>
            </div>
            """, unsafe_allow_html=True)

            # =====================================================
            # GMV
            # =====================================================
            with st.container(border=True):

                fig_gmv = go.Figure()

                fig_gmv.add_trace(go.Bar(
                    x=[str(d) for d in gmv_by_day_last["date"]],
                    y=gmv_by_day_last["gmv"],
                    name="Tháng trước",
                    marker_color="#CBD5E1"
                ))

                fig_gmv.add_trace(go.Bar(
                    x=[str(d) for d in gmv_by_day_this["date"]],
                    y=gmv_by_day_this["gmv"],
                    name="Tháng này",
                    marker_color="#007A00"
                ))

                fig_gmv.update_layout(
                    title="GMV theo ngày trong tháng",
                    xaxis_title="Ngày",
                    yaxis_title="GMV (₫)",
                    barmode="group",
                    height=340,
                    margin=dict(l=0, r=0, t=45, b=0),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )

                st.plotly_chart(fig_gmv, use_container_width=True)

                # =====================================================
                # Orders
                # =====================================================

            with st.container(border=True):

                fig_orders = go.Figure()

                fig_orders.add_trace(go.Bar(
                    x=[str(d) for d in orders_by_day_last["date"]],
                    y=orders_by_day_last["orders"],
                    name="Tháng trước",
                    marker_color="#CBD5E1"
                ))

                fig_orders.add_trace(go.Bar(
                    x=[str(d) for d in orders_by_day_this["date"]],
                    y=orders_by_day_this["orders"],
                    name="Tháng này",
                    marker_color="#0026FF"
                ))

                fig_orders.update_layout(
                    title="Orders theo ngày trong tháng",
                    xaxis_title="Ngày",
                    yaxis_title="Orders",
                    barmode="group",
                    height=340,
                    margin=dict(l=0, r=0, t=45, b=0),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )

                st.plotly_chart(fig_orders, use_container_width=True)

            with st.container(border=True):
                fig_week = px.bar(
                    week_breakdown_tt,
                    x="Week",
                    y="GMV",
                    text_auto=",.0f",
                    color="GMV",
                    color_continuous_scale="Blues",
                    custom_data=["Orders", "AOV"]
                )

                fig_week.update_traces(
                    textposition="outside",
                    hovertemplate="<b>%{x}</b><br>"
                    "GMV: %{y:,.0f}<br>"
                    "Orders: %{customdata[0]:,.0f}<br>"
                    "AOV: %{customdata[1]:,.0f}"
                    "<extra></extra>"
                )

                fig_week.update_layout(
                    title="📅 Weekly GMV Breakdown",
                    height=450,
                    xaxis_title="",
                    yaxis_title="GMV",
                    coloraxis_showscale=False,
                    bargap=0.3
                )
                fig_week.add_hline(
                    y=avg,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Avg {avg/1e6:.1f}M"
                )

                st.plotly_chart(fig_week, use_container_width=True)

            # =====================================================
            # DONUT CHART
            # =====================================================
            with st.container(border=True):

                chart_col3, chart_col4 = st.columns(2)

                with chart_col3:

                    fig_donut = go.Figure(data=[go.Pie(

                        labels=[
                            "Completed / Other",
                            "Cancelled"
                        ],

                        values=[
                            orders_this_month_tt - orders_cancelled_this_month_tt,
                            orders_cancelled_this_month_tt
                        ],

                        hole=0.65,

                        marker_colors=[
                            "#2563EB",
                            "#DC2626"
                        ],

                        textinfo="percent+label"
                    )])

                    fig_donut.update_layout(
                        title=f"Cancelled Rate - Tháng này ({cancel_rate_this_month_tt:.1f}%)",
                        height=340,
                        margin=dict(l=0, r=0, t=45, b=0),
                        showlegend=True
                    )

                    st.plotly_chart(fig_donut, use_container_width=True)

                with chart_col4:

                    fig_donut2 = go.Figure(data=[go.Pie(

                        labels=[
                            "Completed / Other",
                            "Cancelled"
                        ],

                        values=[
                            orders_last_month_tt - orders_cancelled_last_month_tt,
                            orders_cancelled_last_month_tt
                        ],

                        hole=0.65,

                        marker_colors=[
                            "#006D88",
                            "#FF0A0A"
                        ],

                        textinfo="percent+label"
                    )])

                    fig_donut2.update_layout(
                        title=f"Cancelled Rate - Tháng trước ({cancel_rate_last_month_tt:.1f}%)",
                        height=340,
                        margin=dict(l=0, r=0, t=45, b=0),
                        showlegend=True
                    )

                    st.plotly_chart(fig_donut2, use_container_width=True)

    elif platform == "Shopee":
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
                🗓️ Shopee Monthly Report
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

        if uploaded_file:
            st.sidebar.success("XLSX Uploaded!")
            if st.sidebar.button("Check GMV Now"):
                shoppe_data = read_file_shopee(uploaded_file)
                st.session_state.shoppe_data = shoppe_data

        if "shoppe_data" in st.session_state:

            data_shopee = st.session_state["shoppe_data"]

            df_this_month, df_last_month, current, previous = kpi_shopee_month(
                data_shopee
            )

            # =====================================================
            # GMV
            # =====================================================
            gmv_this_month = df_this_month["Tổng số tiền Người mua thanh toán"].sum(
            )
            gmv_last_month = df_last_month["Tổng số tiền Người mua thanh toán"].sum(
            )

            # =====================================================
            # NMV
            # =====================================================
            df_valid_this_month = df_this_month[
                df_this_month["Actually type"] != "Đã hủy"
            ]

            df_valid_last_month = df_last_month[
                df_last_month["Actually type"] != "Đã hủy"
            ]

            nmv_this_month = (
                df_valid_this_month["Tổng số tiền Người mua thanh toán"].sum()
                - df_valid_this_month["Mã giảm giá của Shop"].sum()
            )

            nmv_last_month = (
                df_valid_last_month["Tổng số tiền Người mua thanh toán"].sum()
                - df_valid_last_month["Mã giảm giá của Shop"].sum()
            )

            # =====================================================
            # ORDERS
            # =====================================================
            orders_this_month = df_this_month["Mã đơn hàng"].nunique()
            orders_last_month = df_last_month["Mã đơn hàng"].nunique()

            # =====================================================
            # CANCELLED
            # =====================================================
            orders_cancelled_this_month = df_this_month[
                df_this_month["Actually type"] == "Đã hủy"
            ]["Mã đơn hàng"].nunique()

            orders_cancelled_last_month = df_last_month[
                df_last_month["Actually type"] == "Đã hủy"
            ]["Mã đơn hàng"].nunique()

            # =====================================================
            # AOV
            # =====================================================
            aov_this_month = (
                gmv_this_month / orders_this_month
                if orders_this_month != 0 else 0
            )

            aov_last_month = (
                gmv_last_month / orders_last_month
                if orders_last_month != 0 else 0
            )

            # =====================================================
            # RATES
            # =====================================================
            nmv_rate_this_month = (
                nmv_this_month / gmv_this_month * 100
                if gmv_this_month != 0 else 0
            )

            nmv_rate_last_month = (
                nmv_last_month / gmv_last_month * 100
                if gmv_last_month != 0 else 0
            )

            cancel_rate_this_month = (
                orders_cancelled_this_month / orders_this_month * 100
                if orders_this_month != 0 else 0
            )

            cancel_rate_last_month = (
                orders_cancelled_last_month / orders_last_month * 100
                if orders_last_month != 0 else 0
            )

            # =====================================================
            # MOM
            # =====================================================
            mom_gmv = (
                (gmv_this_month - gmv_last_month)
                / gmv_last_month * 100
                if gmv_last_month != 0 else 0
            )

            mom_nmv = (
                (nmv_this_month - nmv_last_month)
                / nmv_last_month * 100
                if nmv_last_month != 0 else 0
            )

            mom_orders = (
                (orders_this_month - orders_last_month)
                / orders_last_month * 100
                if orders_last_month != 0 else 0
            )

            mom_aov = (
                (aov_this_month - aov_last_month)
                / aov_last_month * 100
                if aov_last_month != 0 else 0
            )

            mom_cancelled = (
                (orders_cancelled_this_month - orders_cancelled_last_month)
                / orders_cancelled_last_month * 100
                if orders_cancelled_last_month != 0 else 0
            )

            cancel_rate_delta = (
                cancel_rate_this_month - cancel_rate_last_month
            )

            nmv_rate_delta = (
                nmv_rate_this_month - nmv_rate_last_month
            )

            # =====================================================
            # MONTH LABELS
            # =====================================================
            current_month = int(current["month"])
            current_year = int(current["year"])

            previous_month = int(previous["month"])
            previous_year = int(previous["year"])

            current_start = (
                df_this_month["Ngày đặt hàng"]
                .min()
                .strftime("%d/%m")
            )

            current_end = (
                df_this_month["Ngày đặt hàng"]
                .max()
                .strftime("%d/%m/%Y")
            )

            previous_start = (
                df_last_month["Ngày đặt hàng"]
                .min()
                .strftime("%d/%m")
            )

            previous_end = (
                df_last_month["Ngày đặt hàng"]
                .max()
                .strftime("%d/%m/%Y")
            )

            # =====================================================
            # SKU GMV / NMV
            # =====================================================
            sku_gmv = (
                df_this_month
                .groupby("SKU Category", as_index=False)["Tổng số tiền Người mua thanh toán"]
                .sum()
                .rename(columns={"Tổng số tiền Người mua thanh toán": "GMV"})
            )

            sku_nmv = (
                df_valid_this_month
                .groupby("SKU Category", as_index=False)["Tổng số tiền Người mua thanh toán"]
                .sum()
                .rename(columns={"Tổng số tiền Người mua thanh toán": "NMV"})
            )

            sku_metrics = (
                sku_gmv
                .merge(sku_nmv, on="SKU Category", how="left")
                .fillna(0)
                .sort_values("GMV", ascending=False)
                .head(8)
            )

            total_gmv_all = sku_metrics["GMV"].sum()

            sku_metrics["GMV_pct"] = (
                sku_metrics["GMV"] / total_gmv_all * 100
                if total_gmv_all != 0 else 0
            )

            # =====================================================
            # CHART DATA
            # =====================================================
            gmv_by_day_this = (
                df_this_month
                .groupby(df_this_month["Ngày đặt hàng"].dt.date)["Tổng số tiền Người mua thanh toán"]
                .sum()
                .reset_index()
            )
            gmv_by_day_this.columns = ["date", "gmv"]

            gmv_by_day_last = (
                df_last_month
                .groupby(df_last_month["Ngày đặt hàng"].dt.date)["Tổng số tiền Người mua thanh toán"]
                .sum()
                .reset_index()
            )
            gmv_by_day_last.columns = ["date", "gmv"]

            orders_by_day_this = (
                df_this_month
                .groupby(df_this_month["Ngày đặt hàng"].dt.date)["Mã đơn hàng"]
                .nunique()
                .reset_index()
            )
            orders_by_day_this.columns = ["date", "orders"]

            orders_by_day_last = (
                df_last_month
                .groupby(df_last_month["Ngày đặt hàng"].dt.date)["Mã đơn hàng"]
                .nunique()
                .reset_index()
            )
            orders_by_day_last.columns = ["date", "orders"]

            # =====================================================
            # FEES
            # =====================================================
            df_fees_this_month = df_this_month.drop_duplicates(
                subset=["Mã đơn hàng"]
            )

            df_fees_this_month["Piship"] = 1620

            fees_predicted = (
                df_fees_this_month["Phí cố định"].sum()
                + df_fees_this_month["Phí Dịch Vụ"].sum()
                + df_fees_this_month["Piship"].sum()
                + df_fees_this_month["Phí xử lý giao dịch"].sum()
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
                    🛒 Shopee Monthly Performance
                </div>
                <div style="margin-top:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                    <div>
                        <div style="font-size:22px;font-weight:800;line-height:1.1;">
                            Month {current_month} - {current_year}
                        </div>
                        <div style="font-size:13px;opacity:0.92;margin-top:4px;">
                            📅 {current_start} → {current_end}
                        </div>
                    </div>
                    <div style="background:rgba(255,255,255,0.18);padding:10px 14px;border-radius:14px;backdrop-filter:blur(6px);">
                        <div style="font-size:11px;opacity:0.85;font-weight:600;text-transform:uppercase;">
                            Compare To
                        </div>
                        <div style="font-size:15px;font-weight:700;margin-top:2px;">
                            Month {previous_month} - {previous_year}
                        </div>
                        <div style="font-size:12px;opacity:0.9;margin-top:2px;">
                            {previous_start} → {previous_end}
                        </div>
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
                    <div class="kpi-title">GMV THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#EE4D2D;">{gmv_this_month:,.0f}₫</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{gmv_last_month:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if mom_gmv >= 0 else 'metric-tag-red'}">
                        {'▲' if mom_gmv >= 0 else '▼'} {mom_gmv:+.2f}% vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">💵</div></div>
                    <div class="kpi-title">NMV THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#0F766E;">{nmv_this_month:,.0f}₫</div>
                    <div style="font-size:13px;color:#64748b;margin-bottom:8px;">
                        Tháng trước: <b>{nmv_last_month:,.0f}₫</b>
                    </div>
                    <div class="{'metric-tag-green' if mom_nmv >= 0 else 'metric-tag-red'}">
                        {'▲' if mom_nmv >= 0 else '▼'} {mom_nmv:+.2f}% vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">📦</div></div>
                    <div class="kpi-title">ORDERS THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#7C3AED;">{orders_this_month:,}</div>
                    <div style="font-size:14px;color:#64748b;margin-bottom:12px;">
                        Tháng trước: <b>{orders_last_month:,}</b>
                    </div>
                    <div class="{'metric-tag-green' if mom_orders >= 0 else 'metric-tag-red'}">
                        {'▲' if mom_orders >= 0 else '▼'} {mom_orders:+.2f}% vs Tháng trước
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top"><div class="kpi-icon">💸</div></div>
                    <div class="kpi-title">FEES THÁNG NÀY</div>
                    <div class="kpi-value" style="color:#DC2626;">{fees_predicted:,.0f}₫</div>
                    <div style="font-size:12px;color:#64748b;margin-bottom:12px;">
                        Fixed + Service + Transaction + Piship
                    </div>
                    <div style="
                        display:inline-block;
                        padding:6px 14px;
                        border-radius:999px;
                        background:#FEF3C7;
                        color:#B45309;
                        font-size:13px;
                        font-weight:700;">
                        Chi phí ước tính
                    </div>
                </div>
                """, unsafe_allow_html=True)
