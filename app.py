import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="The Bear Dashboard", layout="wide")
st.title("🐻 The Bear: Fine-Dining 'Stress Test' Dashboard")
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv("The_Bear__Data.csv")

df = load_data()

st.sidebar.header("📊 Interactive Controls")
pricing_choice = st.sidebar.multiselect("Select Pricing Type:", options=df["Pricing_Type"].unique(), default=df["Pricing_Type"].unique())
payment_choice = st.sidebar.multiselect("Select Payment Method:", options=df["Payment_Type"].unique(), default=df["Payment_Type"].unique())
age_range = st.sidebar.slider("Select Guest Age Range:", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))

filtered_df = df[(df["Pricing_Type"].isin(pricing_choice)) & (df["Payment_Type"].isin(payment_choice)) & (df["Age"].between(age_range[0], age_range[1]))]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Filtered Revenue", f"${filtered_df['Check_Total'].sum():,.2f}")
with col2:
    st.metric("Total Tickets", len(filtered_df))
with col3:
    st.metric("Covers Served", int(filtered_df['Covers'].sum()))
with col4:
    st.metric("Avg Per Cover", f"${filtered_df['Check_Total'].sum() / filtered_df['Covers'].sum():,.2f}" if filtered_df['Covers'].sum() > 0 else "$0.00")

st.markdown("---")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🛢️ Standard vs. Discount Check Value")
    st.plotly_chart(px.box(filtered_df, x="Pricing_Type", y="Check_Total", color="Pricing_Type", points="all"), use_container_width=True)

with col_right:
    st.subheader("♨️ Age vs. Net Check Total")
    st.plotly_chart(px.scatter(filtered_df, x="Age", y="Check_Total", color="Pricing_Type", size="Covers"), use_container_width=True)

st.markdown("---")
st.subheader("🥩 Revenue Engine Breakdown")
st.plotly_chart(px.bar(filtered_df.groupby("Payment_Type")["Check_Total"].sum().reset_index(), x="Payment_Type", y="Check_Total", color="Payment_Type"), use_container_width=True)

if st.checkbox("Show Raw Data Table"):
    st.dataframe(filtered_df)
