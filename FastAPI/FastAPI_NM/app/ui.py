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

st.title("🛒 NM ENTERPRISES")
st.markdown("##### Minimalist Customer Management System")
st.markdown("---")

# Fetch all data for quick overview
try:
    response = requests.get(f"{BACKEND_URL}/get_all")
    if response.status_code == 200:
        all_customers = response.json().get("All Customer Data", [])
    else:
        all_customers = []
except Exception:
    all_customers = []
    st.error("Could not connect to the Backend API. Please check if the server is awake.")

# Tab Selection for Minimalist layout
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard & Lookup", "➕ Add Customer", "📝 Update Record", "❌ Remove"])

# --- TAB 1: DASHBOARD & LOOKUP ---
with tab1:
    st.subheader("Customer Directory")
    if all_customers:
        # Format data for a clean table view
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
                
                # History breakdown
                st.write("### Purchase History")
                history_df = pd.DataFrame({
                    "Date & Time": data["Customer Buying Time"],
                    "Products Bought": [", ".join(p) for p in data["Customer Buying History"]]
                })
                st.table(history_df)
            else:
                st.error("Customer not found.")

# --- TAB 2: ADD CUSTOMER ---
with tab2:
    st.subheader("Register New Customer")
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
                    st.rerun()
                else:
                    st.error(f"Error: {res.text}")
            else:
                st.warning("Please fill out all fields.")

# --- TAB 3: UPDATE RECORD (Add Purchase / Record Payment) ---
with tab3:
    st.subheader("Update Customer Financials")
    
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
                    st.rerun()
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
                    st.rerun()
                else:
                    st.error("Failed to record payment.")

# --- TAB 4: REMOVE CUSTOMER ---
with tab4:
    st.subheader("Danger Zone")
    del_name = st.text_input("Enter exact Customer Name to completely delete:")
    confirm = st.checkbox("I understand this action is permanent and cannot be undone.")
    
    if st.button("Delete Customer Permanently", type="secondary"):
        if del_name and confirm:
            res = requests.delete(f"{BACKEND_URL}/customer", params={"customer_name": del_name})
            if res.status_code == 200:
                st.success(f"Purged record for {del_name}")
                st.rerun()
            else:
                st.error("Customer not found.")
        else:
            st.warning("Please enter name and check the confirmation box.")