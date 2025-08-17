import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Change this for Codespaces public URL when needed
API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Customer Due Tracker", layout="wide")
st.title("📒 Customer Due Tracking System")

menu = ["View Customers", "Add Customer", "Update Customer", "Delete Customer", "Delete All", "Sorted by Due"]
choice = st.sidebar.selectbox("Menu", menu)

# View all customers
if choice == "View Customers":
    res = requests.get(f"{API_URL}/customers").json()
    df = pd.DataFrame(res)
    st.dataframe(df)

    if not df.empty:
        fig, ax = plt.subplots()
        df.plot(kind="bar", x="name", y="due_amount", ax=ax)
        st.pyplot(fig)

# Add customer
elif choice == "Add Customer":
    with st.form("add_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_area("Address")
        due = st.number_input("Due Amount", min_value=0.0)
        submitted = st.form_submit_button("Add")
        if submitted:
            data = {"name": name, "phone": phone, "email": email, "address": address, "due_amount": due}
            res = requests.post(f"{API_URL}/customers", json=data)
            st.success(res.json()["message"])

# Update customer
elif choice == "Update Customer":
    customer_id = st.number_input("Enter Customer ID to Update", min_value=1, step=1)
    new_due = st.number_input("New Due Amount", min_value=0.0)
    if st.button("Update"):
        res = requests.put(f"{API_URL}/customers/{customer_id}", json={"due_amount": new_due})
        result = res.json()
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(result["message"])

# Delete customer
elif choice == "Delete Customer":
    customer_id = st.number_input("Enter Customer ID to Delete", min_value=1, step=1)
    if st.button("Delete"):
        res = requests.delete(f"{API_URL}/customers/{customer_id}")
        result = res.json()
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(result["message"])

# Delete all
elif choice == "Delete All":
    if st.button("Delete All Customers"):
        res = requests.delete(f"{API_URL}/customers")
        st.success(res.json()["message"])

# Sorted view
elif choice == "Sorted by Due":
    res = requests.get(f"{API_URL}/customers/sorted").json()
    df = pd.DataFrame(res)
    st.dataframe(df)
