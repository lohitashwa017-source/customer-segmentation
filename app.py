
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.set_page_config(page_title="Customer Segmentation AI", layout="wide")

df = pd.read_csv('cleaned_data.csv')
bundle = joblib.load('models.pkl')
scaler, kmeans, rf_model = bundle['scaler'], bundle['kmeans'], bundle['rf_model']
segment_names, features = bundle['segment_names'], bundle['features']

recommendations = {
    "VIP Big Spenders": "Offer VIP loyalty tier, early access to new launches, and personal concierge rewards.",
    "Affluent Careful Savers": "Send high-value bundle discounts, extended warranties, and quality-focused emails.",
    "Young Impulse Buyers": "Target with flash-sale push notifications, limited-time coupons, and social media ads.",
    "Budget Value Shoppers": "Promote cashback offers, festival mega-sales, and essential combo packs."
}

st.title("🎯 Customer Segmentation & Targeted Marketing Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(df):,}")
col2.metric("Avg Annual Income", f"₹{df['Annual_Income_Lakhs'].mean():.1f} L")
col3.metric("Avg Spending Score", f"{df['Spending_Score'].mean():.1f} / 100")
col4.metric("Campaign Response Rate", f"{df['Campaign_Response'].mean()*100:.1f}%")

tab1, tab2, tab3 = st.tabs(["📊 Segments & Analytics", "📋 Profiles & Strategy", "🔮 Live Predictor"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.scatter(df, x="Annual_Income_Lakhs", y="Spending_Score", color="Segment_Name",
                          title="Customer Segments: Income vs. Spending Score")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        resp = df.groupby("Segment_Name")["Campaign_Response"].mean().reset_index()
        resp["Response_Pct"] = resp["Campaign_Response"] * 100
        fig2 = px.bar(resp, x="Segment_Name", y="Response_Pct", color="Segment_Name",
                      title="Campaign Response Rate by Segment (%)")
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    profile = df.groupby("Segment_Name").agg(
        Customers=("CustomerID", "count"),
        Avg_Age=("Age", "mean"),
        Avg_Income_Lakhs=("Annual_Income_Lakhs", "mean"),
        Avg_Spending=("Spending_Score", "mean"),
        Avg_Frequency=("Purchase_Frequency", "mean"),
        Response_Rate_Pct=("Campaign_Response", lambda x: x.mean() * 100)
    ).round(1).reset_index()
    profile["Recommended_Campaign"] = profile["Segment_Name"].map(
        lambda s: recommendations.get(s, "Send personalized seasonal discount coupon.")
    )
    st.dataframe(profile, use_container_width=True)

with tab3:
    p1, p2 = st.columns(2)
    with p1:
        age = st.slider("Age", 18, 70, 32)
        income = st.slider("Annual Income (₹ Lakhs)", 2.5, 25.0, 14.5)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with p2:
        spending = st.slider("Spending Score (1 - 100)", 1, 100, 75)
        freq = st.slider("Purchase Frequency (per year)", 1, 30, 15)

    if st.button("Analyze Customer", type="primary"):
        gender_code = 0 if gender == "Male" else 1
        input_df = pd.DataFrame([[age, income, spending, freq, gender_code]], columns=features)
        input_scaled = scaler.transform(input_df)
        seg_id = kmeans.predict(input_scaled)[0]
        seg_name = segment_names.get(seg_id, f"Segment {seg_id}")
        prob = rf_model.predict_proba(input_scaled)[0][1] * 100
        offer = recommendations.get(seg_name, "Send personalized seasonal discount coupon.")

        st.success(f"**Assigned Segment:** {seg_name}")
        st.info(f"**Campaign Response Likelihood:** {prob:.1f}%")
        st.warning(f"**Recommended Action:** {offer}")
