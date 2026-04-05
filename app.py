import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Food Waste Dashboard", layout="wide")

st.title("🍽️ Smart Food Waste Management Dashboard")

# ------------------ SESSION STATE (IMPORTANT) ------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Waste": [20, 35, 30, 25, 40],
        "Donated": [10, 20, 15, 18, 25],
        "Compost": [5, 10, 8, 7, 12]
    })

df = st.session_state.data

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Controls")
selected_day = st.sidebar.selectbox("Select Day", ["All"] + list(df["Day"].unique()))

filtered_df = df if selected_day == "All" else df[df["Day"] == selected_day]

# ------------------ METRICS ------------------
col1, col2, col3 = st.columns(3)

col1.metric("♻️ Total Waste (kg)", int(filtered_df["Waste"].sum()))
col2.metric("🤝 Donated (kg)", int(filtered_df["Donated"].sum()))
col3.metric("🌱 Compost (kg)", int(filtered_df["Compost"].sum()))

# ------------------ BAR CHART ------------------
st.subheader("📊 Waste Trend")

fig_bar = px.bar(
    filtered_df,
    x="Day",
    y=["Waste", "Donated", "Compost"],
    barmode="group"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ------------------ PIE CHART ------------------
st.subheader("🥧 Waste Distribution")

pie_data = pd.DataFrame({
    "Category": ["Waste", "Donated", "Compost"],
    "Value": [
        filtered_df["Waste"].sum(),
        filtered_df["Donated"].sum(),
        filtered_df["Compost"].sum()
    ]
})

fig_pie = px.pie(pie_data, names="Category", values="Value", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)

# ------------------ MAP ------------------
st.subheader("📍 Live Locations")

map_data = pd.DataFrame({
    "lat": [28.61, 28.70, 28.65],
    "lon": [77.20, 77.10, 77.25]
})

st.map(map_data)

# ------------------ FORM (UPDATED) ------------------
st.subheader("📦 Add Food Data")

with st.form("food_form"):
    day = st.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    quantity = st.number_input("Quantity (kg)", min_value=1)
    category = st.selectbox("Category", ["Waste", "Donated", "Compost"])
    submit = st.form_submit_button("Add Entry")

    if submit:
        new_row = {
            "Day": day,
            "Waste": 0,
            "Donated": 0,
            "Compost": 0
        }

        new_row[category] = quantity

        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_row])],
            ignore_index=True
        )

        st.success("✅ Data Added Successfully!")
        st.rerun()

# ------------------ TABLE ------------------
st.subheader("📋 Data Table")
st.dataframe(st.session_state.data, use_container_width=True)

# ------------------ FILE UPLOAD ------------------
st.subheader("📤 Upload CSV")

uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file:
    st.session_state.data = pd.read_csv(uploaded_file)
    st.success("✅ File Uploaded!")
    st.rerun()
