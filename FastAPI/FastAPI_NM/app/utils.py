import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime, timezone
from pydantic import Field

data_file = Path('..\data\customer.json')

def load_all() -> List[Dict]:
    if not data_file.exists():
        return []
    
    with open(data_file, 'r') as f:
        return json.load(f)
    
customers = load_all()

def add_customer(customer_data: Dict, products: str):

    if any(customer_data['Name'] == customer['Name'] for customer in customers):
        raise ValueError(f"Customer with name {customer_data['Name']} is already present")
    
    with open(data_file, 'w'):
        products_list = products.split(',')
        customer_data['Products_Purchased'] = products_list
        customers.append(customer_data)
        return json.dump(customers, data_file, ensure_ascii= True, indent= 2)
    
def modify_customer_record(name: str, current_balance: int, products: str):
    products_list = products.split(',')
    time = datetime.now(timezone.utc).strftime("%d/%m/%y %H:%M:%S")
    is_present = False
    for customer in customers:
        if customer['Name'].lower() == name.lower():
            customer['Total_Balance'] = customer['Total_Balance'] + current_balance
            customer['Products_Purchased'].append(products_list)
            customer['Purchased_At'].append(time)
            is_present = True
            break

    if is_present:
        with open(data_file, 'w'):
            return json.dump(customers, data_file, ensure_ascii= True, indent= 2)
    else:
        raise ValueError("Customer Not Found")
    
def modify_customer_balance(name: str, balance: int):
    is_present = False
    for customer in customers:
        if customer['Name'].lower() == name.lower():
            customer['Total_Balance'] = customer['Total_Balance'] - balance
            is_present = True
        
    if is_present:
        with open(data_file, 'w'):
            return json.dump(customers, data_file, ensure_ascii= True, indent= 2)
    else:
        raise ValueError("Customer Not Found")
        
def delete_customer(name: str):
    for customer in customers:
        if customer['Name'].lower() == name.lower():
            index = customers.index(customer)
            break
    if index:
        with open(data_file, 'w'):
            json.dump(customers, data_file, ensure_ascii= True, indent= 2)
        return customers.pop(index)
    else:
        raise ValueError("Customer Not Found")



