import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("🍽️ Food Sharing Marketplace")

# ---------------- SESSION ----------------
if "food_data" not in st.session_state:
    st.session_state.food_data = pd.DataFrame(columns=[
        "Food", "Quantity", "Price", "Location"
    ])

if "requests" not in st.session_state:
    st.session_state.requests = []

# ---------------- ROLE SELECT ----------------
role = st.sidebar.selectbox("Select Role", ["Giver (Restaurant)", "Buyer (Needy)"])

# ---------------- GIVER PANEL ----------------
if role == "Giver (Restaurant)":

    st.header("🍽️ Add Leftover Food")

    with st.form("food_form"):
        food = st.text_input("Food Name")
        qty = st.number_input("Quantity (kg)", min_value=1)
        price = st.number_input("Price (₹)", min_value=1)
        location = st.text_input("Location")

        submit = st.form_submit_button("Add Food")

        if submit:
            new_data = {
                "Food": food,
                "Quantity": qty,
                "Price": price,
                "Location": location
            }

            st.session_state.food_data = pd.concat(
                [st.session_state.food_data, pd.DataFrame([new_data])],
                ignore_index=True
            )

            st.success("✅ Food Added!")

    st.subheader("📋 Available Food")
    st.dataframe(st.session_state.food_data)

# ---------------- BUYER PANEL ----------------
elif role == "Buyer (Needy)":

    st.header("🙋‍♂️ Available Food")

    df = st.session_state.food_data

    if df.empty:
        st.info("No food available")
    else:
        for i, row in df.iterrows():
            col1, col2, col3, col4 = st.columns(4)

            col1.write(f"🍛 {row['Food']}")
            col2.write(f"📦 {row['Quantity']} kg")
            col3.write(f"💰 ₹{row['Price']}")
            col4.write(f"📍 {row['Location']}")

            if st.button(f"Request {row['Food']}", key=i):
                st.session_state.requests.append(row.to_dict())
                st.success("✅ Request Sent!")

# ---------------- ADMIN PANEL ----------------
st.sidebar.subheader("📊 Requests")

if st.session_state.requests:
    st.sidebar.write(st.session_state.requests)
else:
    st.sidebar.write("No requests yet")
