import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="NM ENTERPRISES",
    page_icon="💼",
    layout="wide",
)

# Backend URL (Update this with your Render backend URL)
BACKEND_URL = st.sidebar.text_input("Backend API URL", value="https://customer-management-system-nm-enterprises.onrender.com")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📌 Menu")
page = st.sidebar.radio(
    "Select an Operation:",
    ["📊 Dashboard & Lookup", "➕ Add Customer", "📝 Update Record", "❌ Remove Customer"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: If the app feels slow on the first click, the backend is just waking up!")

# Fetch all data for the overview
try:
    response = requests.get(f"{BACKEND_URL}/get_all")
    if response.status_code == 200:
        all_customers = response.json().get("All Customer Data", [])
    else:
        all_customers = []
except Exception:
    all_customers = []

# --- PAGE 1: DASHBOARD & LOOKUP ---
if page == "📊 Dashboard & Lookup":
    st.title("📊 NM ENTERPRISES — Dashboard")
    st.markdown("##### View master directory and detailed customer history")
    st.markdown("---")
    
    st.subheader("Customer Directory")
    if all_customers:
        formatted_data = []
        for c in all_customers:
            formatted_data.append({
                "Name": c.get("Name", "").title(),
                "Total Balance (₹)": c.get("Total_Balance", 0),
                "Last Active": c.get("Purchased_At", ["N/A"])[-1] if c.get("Purchased_At") else "N/A"
            })
        df = pd.DataFrame(formatted_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No customer records found or backend is loading.")

    st.markdown("---")
    st.subheader("🔍 Quick Customer History Lookup")
    search_name = st.text_input("Enter Customer Name to look up history:")
    if st.button("Fetch History", type="primary"):
        if search_name:
            res = requests.get(f"{BACKEND_URL}/customer_history", params={"customer_name": search_name})
            if res.status_code == 200:
                data = res.json()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Balance", f"₹{data['Customer Total Balance']}")
                with col2:
                    st.write(f"**Name:** {data['Customer Name'].title()}")
                
                st.write("### Purchase History")
                history_df = pd.DataFrame({
                    "Date & Time": data["Customer Buying Time"],
                    "Products Bought": [", ".join(p) for p in data["Customer Buying History"]]
                })
                st.table(history_df)
            else:
                st.error("Customer not found.")

# --- PAGE 2: ADD CUSTOMER ---
elif page == "➕ Add Customer":
    st.title("➕ Register New Customer")
    st.markdown("##### Onboard a new customer profile into the system")
    st.markdown("---")
    
    with st.form("add_customer_form", clear_on_submit=True):
        new_name = st.text_input("Customer Name")
        initial_balance = st.number_input("Initial Balance / Due Amount", min_value=0, step=1)
        products = st.text_input("Products Purchased (Comma separated, e.g., Soap, Rice, Oil)")
        
        submit_btn = st.form_submit_button("Save Customer", type="primary")
        if submit_btn:
            if new_name and products:
                payload = {
                    "Name": new_name,
                    "Total_Balance": initial_balance
                }
                res = requests.post(f"{BACKEND_URL}/create_customer", json=payload, params={"products": products})
                if res.status_code == 200:
                    st.success(f"Successfully added {new_name}!")
                else:
                    st.error(f"Error: {res.text}")
            else:
                st.warning("Please fill out all fields.")

# --- PAGE 3: UPDATE RECORD ---
elif page == "📝 Update Record":
    st.title("📝 Update Customer Financials")
    st.markdown("##### Log a new purchase order or record an incoming cash payment")
    st.markdown("---")
    
    update_type = st.radio("Select Action", ["Record New Purchase (Increase Balance)", "Record Payment Received (Decrease Balance)"], horizontal=True)
    
    with st.form("update_form", clear_on_submit=True):
        up_name = st.text_input("Customer Name")
        
        if update_type == "Record New Purchase (Increase Balance)":
            up_balance = st.number_input("Amount to Add", min_value=0, step=1)
            up_products = st.text_input("New Products (Comma separated)")
            submitted = st.form_submit_button("Update Purchase Record", type="primary")
            
            if submitted and up_name:
                res = requests.post(f"{BACKEND_URL}/update_customer_record", params={
                    "customer_name": up_name, "products_bought": up_products, "balance": up_balance
                })
                if res.status_code == 200:
                    st.success("Record updated successfully!")
                else:
                    st.error("Failed to update.")
        
        else:
            pay_balance = st.number_input("Amount Paid by Customer", min_value=1, step=1)
            submitted = st.form_submit_button("Record Payment", type="primary")
            
            if submitted and up_name:
                res = requests.post(f"{BACKEND_URL}/update_record_balance", params={
                    "customer_name": up_name, "balance": pay_balance
                })
                if res.status_code == 200:
                    st.success("Payment recorded successfully!")
                else:
                    st.error("Failed to record payment.")

# --- PAGE 4: REMOVE CUSTOMER ---
elif page == "❌ Remove Customer":
    st.title("❌ Danger Zone")
    st.markdown("##### Completely purge a customer profile from the cloud files")
    st.markdown("---")
    
    del_name = st.text_input("Enter exact Customer Name to completely delete:")
    confirm = st.checkbox("I understand this action is permanent and cannot be undone.")
    
    if st.button("Delete Customer Permanently", type="secondary"):
        if del_name and confirm:
            res = requests.delete(f"{BACKEND_URL}/customer", params={"customer_name": del_name})
            if res.status_code == 200:
                st.success(f"Purged record for {del_name}")
            else:
                st.error("Customer not found.")
        else:
            st.warning("Please enter name and check the confirmation box.")