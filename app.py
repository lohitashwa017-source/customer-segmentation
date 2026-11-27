import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(
    page_title="SegmaPulse Analytics | Targeted Marketing System",
    page_icon="📊",
    layout="wide"
)

# ================= SESSION & LOGIN PORTAL =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if not st.session_state.logged_in:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #090d16, #1e293b); padding: 32px; border-radius: 16px; color: white; margin-bottom: 24px;">
            <h1 style="margin:0; font-size: 32px;">SegmaPulse <span style="color:#60a5fa;">Analytics</span></h1>
            <p style="color:#94a3b8; margin-top:8px;">Enterprise Customer Segmentation (K-Means) & Campaign Response Prediction Portal</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("Platform Highlights")
        st.markdown("""
        - **1,000+ Customer Behavioral Profiles** analyzed and standardized
        - **K-Means Clustering (k=3)** separating VIP Big Spenders, Affluent Careful Savers & Budget Shoppers
        - **Random Forest Classifier** delivering **86.4% prediction accuracy**
        - **3.6x Higher Conversion Lift** on VIP segments vs. untargeted ads
        """)
        st.info("Demo Credentials: `admin@segmapulse.in` | Password: `Segma2026`")

    with col2:
        st.subheader("Sign In to Marketing Console")
        with st.form("login_form"):
            email = st.text_input("Work Email", value="admin@segmapulse.in")
            password = st.text_input("Password", value="Segma2026", type="password")
            submitted = st.form_submit_button("Sign In to Dashboard →", use_container_width=True)
            if submitted:
                if email.strip() and password.strip():
                    st.session_state.logged_in = True
                    st.session_state.user_email = email.strip()
                    st.rerun()
                else:
                    st.error("Please enter both work email and password.")

        if st.button("Quick Demo Login (1-Click Judge Access)", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user_email = "judge.demo@segmapulse.in"
            st.rerun()

    st.stop()

# ================= MAIN ANALYTICS DASHBOARD =================
top_left, top_right = st.columns([4, 1])
with top_left:
    st.title("📊 SegmaPulse Analytics — Targeted Marketing System")
    st.caption(f"Signed in as **{st.session_state.user_email}** | K-Means (k=3) & Random Forest Engine")
with top_right:
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

# KPI Strip
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Customer Base", "1,000", "100% Standardized")
k2.metric("VIP Big Spenders (48.2%)", "482", "63.5% Response (3.6x Lift)")
k3.metric("Affluent Savers (26.7%)", "267", "43.4% Response Rate")
k4.metric("Budget Shoppers (25.1%)", "251", "17.5% Response Rate")

st.divider()

tab1, tab2, tab3 = st.tabs([
    "1. Segment Explorer",
    "2. Live Customer Predictor",
    "3. Campaign ROI Simulator"
])

# TAB 1: SEGMENT EXPLORER
with tab1:
    st.subheader("Behavioral Customer Clusters (K-Means, k = 3)")
    summary_df = pd.DataFrame({
        "Cluster": ["Cluster 0: VIP Big Spenders", "Cluster 1: Affluent Careful Savers", "Cluster 2: Budget Value Shoppers"],
        "Customers": [482, 267, 251],
        "Share (%)": ["48.2%", "26.7%", "25.1%"],
        "Avg Income": ["₹14.3 Lakhs", "₹14.2 Lakhs", "₹12.4 Lakhs"],
        "Spending Score": ["74 / 100", "28 / 100", "42 / 100"],
        "Response Rate": ["63.5%", "43.4%", "17.5%"],
        "Recommended Strategy": [
            "VIP Loyalty Tier, Early Launch Access & ₹1,500 Voucher",
            "High-Value Product Bundles, Extended Warranty & 0% EMI",
            "Festival Mega-Sales & Automated Cashback Coupons"
        ]
    })
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

# TAB 2: LIVE CUSTOMER PREDICTOR
with tab2:
    st.subheader("Real-Time Customer Scoring")
    c1, c2 = st.columns(2)
