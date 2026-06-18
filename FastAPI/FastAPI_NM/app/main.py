from fastapi import FastAPI, Depends, Query, HTTPException
from schema import Customer
from utils import load_all, add_customer, modify_customer_record, modify_customer_balance, delete_customer
from typing import List, Dict

app = FastAPI(title="NM ENTERPRISES")

def load_all_customer() -> List[Dict]:
    return load_all

@app.post('/customers', response_model= Dict)
def create_customer(new_customer: Customer, products: str):
    customer_dict = new_customer.model_dump(mode='json')
    try:
        add_customer(customer_dict, products)
        return{
            f"Customer Details Added"
        }
    
    except Exception as error:
        return {
            f"An Error Occurred as {error}"
        }

@app.post('/customers', response_model= Dict)
def update_customer_record(customer_name: str = Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    ), 
    products_bought: str = Query(...,
        min_length=1,
        title= "Add Products",
        description= "Enter products with ',' seperated"
    ),
    balance: int = Query(...,
        ge=0,
        title= "Enter Current Balance",
        description= "Enter the total of current products"
    )
):
    try:
        modify_customer_record(customer_name, balance, products_bought)
        return {
            f"Details of Customer with name {customer_name} is updated"
        }
    
    except Exception as error:
        return {
            f"An Error Occurred as {error}"
        }

@app.post('/customers', response_model = Dict)   
def update_customer_balance(customer_name: str = Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    ),
    balance: int = Query(...,
        ge= 0,
        title= "Enter Amount Given",
        description= "Enter the amount given"
    )
):
    try:
        modify_customer_balance(customer_name, balance)
        return {
            f"Customer Details with name {customer_name} has been updated"
        }
    
    except Exception as error:
        return {
            HTTPException(status_code=404, detail= error)
        }

@app.get('/customers')
def get_all_customers(dep = Depends(load_all_customer)):
    return {
        "All Customer Data": dep
    }

@app.get('/customers', response_model= Dict)
def get_customer_total_balance(customer_name: str = Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    ), 
    dep = Depends(load_all_customer)
):
    customers = dep
    for customer in customers:
        if customer['Name'].lower() == customer_name.lower():
            if customer['Total_Balance'] < 0:
                return {
                        "Customer Name": customer['Name'],
                        "Balance Details":f"This customer has a credit amount of {customer['Total_Balance']}"
                    }
    
            else:
                return {
                        "Customer Name": customer['Name'],
                        "Balance Details":f"This customer has a total balance of {customer['Total Balance']}"
                }
    
    return {
        HTTPException(status_code= 404, detail="Customer Name Not Found")
    }

@app.get('/customers')
def get_customer_history(customer_name: str = Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    ), 
    dep = Depends(load_all_customer)
):
    customers = dep
    for customer in customers:
        if customer['Name'].lower() == customer_name.lower():
            history  = customer['Products_Purchased']
            time = customer['Purchased_At']
            return {
                'Customer Name': customer['Name'],
                'Customer Buying History': history,
                'Customer Buying Time': time,
                'Customer Total Balance': customer['Total_Balance']
            }

    return HTTPException(status_code= 404, detail="Customer Buying History Cannot Be Found")
            
@app.delete("/customers")
def remove_customer(customer_name: str= Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    )
):
    try:
        customer_detail = delete_customer(customer_name)
        return f"Customer record deleted with details : {customer_detail}"
    
    except Exception as error:
        return HTTPException(status_code=404, detail= error)
    
    
