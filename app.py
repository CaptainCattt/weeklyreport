import streamlit as st

st.set_page_config(
    page_title="Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ─── CSS CHUNG ────────────────────────────────────────────────
st.markdown("""
<style>
button[kind="primary"] {
    background-color: #16a34a !important;
    color: white !important;
    border: 2px solid #15803d !important;
}
div.stButton > button {
    border-radius: 10px;
    height: 44px;
    font-size: 14px;
    font-weight: 500;
    margin-top: 8px;
}
            
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────
if "platform" not in st.session_state:
    st.session_state.platform = "TikTok"
if "active_tool" not in st.session_state:
    st.session_state.active_tool = None

# ─── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    if st.button("🔄 Reset dữ liệu", use_container_width=True):
        # Xóa cache
        st.cache_data.clear()
        st.cache_resource.clear()

        # Reset session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
    st.markdown("---")
    st.markdown("""
    <div style="
        font-size: 22px;
        font-weight: 700;
        border-left: 6px solid #2563EB;
        padding-left: 12px;
        margin-bottom: 16px;
    ">
        🧰 Công cụ
    </div>
    """, unsafe_allow_html=True)
    cola, colb = st.columns(2)
    with cola:
        if st.button("📅 Order Report", use_container_width=True, key="sb_order",
                     type="primary" if st.session_state.active_tool == "order" else "secondary"):
            st.session_state.active_tool = "order"
            st.rerun()

    with colb:
        if st.button("📈 Week Report", use_container_width=True, key="sb_week",
                     type="primary" if st.session_state.active_tool == "week" else "secondary"):
            st.session_state.active_tool = "week"
            st.rerun()

    st.markdown("---")

    st.markdown("""
    <div style="
        font-size: 22px;
        font-weight: 700;
        border-left: 6px solid #4CAF50;
        padding-left: 12px;
        margin-bottom: 12px;
    ">
        🛒 Nền tảng
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div style="text-align:center;"><img src="https://img.icons8.com/color/96/tiktok--v1.png" width="50"></div>', unsafe_allow_html=True)
        if st.button("TikTok", use_container_width=True, key="sb_tiktok",
                     type="primary" if st.session_state.platform == "TikTok" else "secondary"):
            st.session_state.platform = "TikTok"
            st.rerun()

    with col2:
        st.markdown(
            '<div style="text-align:center;"><img src="https://img.icons8.com/color/96/shopee.png" width="50"></div>', unsafe_allow_html=True)
        if st.button("Shopee", use_container_width=True, key="sb_shopee",
                     type="primary" if st.session_state.platform == "Shopee" else "secondary"):
            st.session_state.platform = "Shopee"
            st.rerun()

    st.markdown("---")


# ─── MAIN CONTENT ──────────────────────────────────────────────
if st.session_state.active_tool == "order":
    import day_report
    day_report.run(platform=st.session_state.platform)

elif st.session_state.active_tool == "week":
    import week_report
    week_report.run(platform=st.session_state.platform)

else:
    st.markdown("<div style='height: 80px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 64px">📊</div>
        <div style="font-size: 28px; font-weight: 700; color: #111; margin-top: 12px;">
            Performance Dashboard
        </div>
        <div style="font-size: 16px; color: #6B7280; margin-top: 8px;">
            Chọn công cụ bên trái để bắt đầu
        </div>
    </div>
    """, unsafe_allow_html=True)
