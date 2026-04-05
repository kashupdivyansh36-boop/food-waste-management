import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Food Waste Dashboard", layout="wide")

# ------------------ TITLE ------------------
st.title("🍽️ Smart Food Waste Management Dashboard")

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Controls")

# Sample Data
data = {
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Waste": [20, 35, 30, 25, 40, 50, 45],
    "Donated": [10, 20, 15, 18, 25, 30, 28],
    "Compost": [5, 10, 8, 7, 12, 15, 14]
}
df = pd.DataFrame(data)

# Filter
selected_day = st.sidebar.selectbox("Select Day", ["All"] + list(df["Day"]))

if selected_day != "All":
    df = df[df["Day"] == selected_day]

# ------------------ METRICS ------------------
total_waste = df["Waste"].sum()
total_donated = df["Donated"].sum()
total_compost = df["Compost"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("♻️ Total Waste (kg)", total_waste)
col2.metric("🤝 Donated (kg)", total_donated)
col3.metric("🌱 Compost (kg)", total_compost)

# ------------------ BAR CHART ------------------
st.subheader("📊 Waste Trend")

fig_bar = px.bar(
    df,
    x="Day",
    y=["Waste", "Donated", "Compost"],
    barmode="group",
    title="Daily Food Data"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ------------------ PIE CHART ------------------
st.subheader("🥧 Waste Distribution")

pie_data = pd.DataFrame({
    "Category": ["Waste", "Donated", "Compost"],
    "Value": [total_waste, total_donated, total_compost]
})

fig_pie = px.pie(
    pie_data,
    names="Category",
    values="Value",
    hole=0.4
)

st.plotly_chart(fig_pie, use_container_width=True)

# ------------------ MAP ------------------
st.subheader("📍 Live Locations")

map_data = pd.DataFrame({
    "lat": [28.61, 28.70, 28.65],
    "lon": [77.20, 77.10, 77.25]
})

st.map(map_data)

# ------------------ FORM ------------------
st.subheader("📦 Add Food Data")

with st.form("food_form"):
    food_type = st.text_input("Food Type")
    quantity = st.number_input("Quantity (kg)", min_value=0)
    category = st.selectbox("Category", ["Waste", "Donated", "Compost"])
    submit = st.form_submit_button("Add Entry")

    if submit:
        st.success(f"{food_type} ({quantity} kg) added as {category}")

# ------------------ TABLE ------------------
st.subheader("📋 Data Table")
st.dataframe(df, use_container_width=True)

# ------------------ FILE UPLOAD ------------------
st.subheader("📤 Upload Your Data")

uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file:
    new_df = pd.read_csv(uploaded_file)
    st.write(new_df)