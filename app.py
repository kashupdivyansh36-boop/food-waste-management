import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Food Waste Dashboard", layout="wide")

st.title("🍽️ Smart Food Waste Management Dashboard")

# ------------------ SESSION STATE ------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Day", "Restaurant", "Food_Item", "Waste", "Donated", "Compost"
    ])

df = st.session_state.data

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.header("⚙️ Filters")

day_filter = st.sidebar.selectbox(
    "Select Day",
    ["All", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
)

filtered_df = df if day_filter == "All" else df[df["Day"] == day_filter]

# ------------------ METRICS ------------------
col1, col2, col3 = st.columns(3)

col1.metric("♻️ Total Waste", int(filtered_df["Waste"].sum()))
col2.metric("🤝 Total Donated", int(filtered_df["Donated"].sum()))
col3.metric("🌱 Total Compost", int(filtered_df["Compost"].sum()))

# ------------------ CHART DATA (GROUPED) ------------------
chart_df = filtered_df.groupby("Day")[["Waste", "Donated", "Compost"]].sum().reset_index()

# ------------------ BAR CHART ------------------
st.subheader("📊 Waste Trend")

if not chart_df.empty:
    fig = px.bar(chart_df, x="Day", y=["Waste", "Donated", "Compost"], barmode="group")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available")

# ------------------ PIE CHART ------------------
st.subheader("🥧 Distribution")

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

# ------------------ FORM ------------------
st.subheader("📦 Add New Entry")

with st.form("form"):
    col1, col2 = st.columns(2)

    with col1:
        day = st.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        restaurant = st.text_input("Restaurant Name")

    with col2:
        food = st.text_input("Food Item")
        category = st.selectbox("Category", ["Waste", "Donated", "Compost"])

    quantity = st.number_input("Quantity (kg)", min_value=1)

    submit = st.form_submit_button("Add Data")

    if submit:
        new_data = {
            "Day": day,
            "Restaurant": restaurant,
            "Food_Item": food,
            "Waste": 0,
            "Donated": 0,
            "Compost": 0
        }

        new_data[category] = quantity

        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_data])],
            ignore_index=True
        )

        st.success("✅ Entry Added")
        st.rerun()

# ------------------ TABLE ------------------
st.subheader("📋 Data Table")
st.dataframe(st.session_state.data, use_container_width=True)

# ------------------ CLEAR BUTTON ------------------
if st.button("🗑️ Clear All Data"):
    st.session_state.data = pd.DataFrame(columns=df.columns)
    st.rerun()
