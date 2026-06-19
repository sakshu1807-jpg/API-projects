import os
from typing import List, Dict
from datetime import datetime
from zoneinfo import ZoneInfo
from pymongo import MongoClient

# 1. Connect to MongoDB using an Environment Variable
# When testing locally, you can paste your string here as a default fallback:
MONGO_URI = os.getenv("MONGO_URI", "PASTE_YOUR_MONGODB_CONNECTION_STRING_HERE")

client = MongoClient(MONGO_URI)
db = client["nm_enterprises_db"]      # Database name
collection = db["customers"]          # Collection (Table) name

def load_all() -> List[Dict]:
    """Fetches all customers directly from the cloud database."""
    customers = list(collection.find({}, {"_id": 0})) # Drops internal mongo IDs for clean JSON
    return customers

def add_customer(customer_data: Dict, products: str):
    customer_data['Name'] = customer_data['Name'].strip().lower()

    # Check if customer already exists in cloud
    if collection.find_one({"Name": customer_data['Name']}):
        raise ValueError(f"Customer with name {customer_data['Name']} is already present")
    
    raw_time_str = customer_data.get("Purchased_At")
    if raw_time_str:
        clean_iso = raw_time_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_iso)
        ist_dt = dt.astimezone(ZoneInfo("Asia/Kolkata"))
        customer_data["Purchased_At"] = [ist_dt.strftime("%d %B %Y, %I:%M %p")]
    
    products_list = [p.strip() for p in products.split(',')]
    customer_data['Products_Purchased'] = [products_list]
    
    # Save directly to Cloud
    collection.insert_one(customer_data)

def modify_customer_record(name: str, current_balance: int, products: str):
    products_list = [p.strip() for p in products.split(',')]
    ist_dt = datetime.now(ZoneInfo("Asia/Kolkata"))
    time_str = ist_dt.strftime("%d %B %Y, %I:%M %p")
    
    clean_name = name.strip().lower()
    
    # Update array elements and increment balance directly in Atlas
    result = collection.update_one(
        {"Name": clean_name},
        {
            "$inc": {"Total_Balance": current_balance},
            "$push": {
                "Products_Purchased": products_list,
                "Purchased_At": time_str
            }
        }
    )
    if result.matched_count == 0:
        raise ValueError("Customer Not Found")

def modify_customer_balance(name: str, balance: int):
    clean_name = name.strip().lower()
    
    # Decrement balance ($inc with a negative value subtracts)
    result = collection.update_one(
        {"Name": clean_name},
        {"$inc": {"Total_Balance": -balance}}
    )
    if result.matched_count == 0:
        raise ValueError("Customer Not Found")
        
def delete_customer(name: str):
    clean_name = name.strip().lower()
    
    # Find and delete
    customer = collection.find_one({"Name": clean_name}, {"_id": 0})
    if not customer:
        raise ValueError("Customer Not Found")
        
    collection.delete_one({"Name": clean_name})
    return customer