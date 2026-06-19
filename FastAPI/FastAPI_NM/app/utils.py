import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

data_file = Path('../data/customer.json')

def load_all() -> List[Dict]:
    if not data_file.exists():
        return []
    
    with open(data_file, 'r') as f:
        return json.load(f)
    
customers = load_all()

def add_customer(customer_data: Dict, products: str):

    customer_data['Name'] = customer_data['Name'].strip().lower()

    if any(customer_data['Name'] == customer['Name'] for customer in customers):
        raise ValueError(f"Customer with name {customer_data['Name']} is already present")
    
    raw_time_str = customer_data.get("Purchased_At")
    
    if raw_time_str:
        clean_iso = raw_time_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_iso)
        ist_dt = dt.astimezone(ZoneInfo("Asia/Kolkata"))
        customer_data["Purchased_At"] = [ist_dt.strftime("%d %B %Y, %I:%M %p")]
    
    products_list = [p.strip() for p in products.split(',')]
    customer_data['Products_Purchased'] = [products_list]
    customers.append(customer_data)
    with open(data_file, 'w') as f:
        return json.dump(customers, f, ensure_ascii= True, indent= 2)
    
def modify_customer_record(name: str, current_balance: int, products: str):
    products_list = [p.strip() for p in products.split(',')]
    ist_dt = datetime.now(ZoneInfo("Asia/Kolkata"))
    time = ist_dt.strftime("%d %B %Y, %I:%M %p")
    is_present = False
    for customer in customers:
        if customer['Name'] == name.strip().lower():
            customer['Total_Balance'] = customer['Total_Balance'] + current_balance
            customer['Products_Purchased'].append(products_list)
            customer['Purchased_At'].append(time)
            is_present = True
            break

    if is_present:
        with open(data_file, 'w') as f:
            return json.dump(customers, f, ensure_ascii= True, indent= 2)
    else:
        raise ValueError("Customer Not Found")
    
def modify_customer_balance(name: str, balance: int):
    is_present = False
    for customer in customers:
        if customer['Name'].strip().lower() == name.strip().lower():
            customer['Total_Balance'] = customer['Total_Balance'] - balance
            is_present = True
            break
        
    if is_present:
        with open(data_file, 'w')as f:
            return json.dump(customers, f, ensure_ascii= True, indent= 2)
    else:
        raise ValueError("Customer Not Found")
        
def delete_customer(name: str):
    is_present = False
    index = None
    for customer in customers:
        if customer.get('Name').strip().lower() == name.strip().lower():
            index = customers.index(customer)
            is_present = True
            break
    if isinstance(index, int) and is_present:
        removed_customer = customers.pop(index)
        with open(data_file, 'w') as f:
            json.dump(customers, f, ensure_ascii= True, indent= 2)
        return removed_customer
    else:
        raise ValueError("Customer Not Found")



