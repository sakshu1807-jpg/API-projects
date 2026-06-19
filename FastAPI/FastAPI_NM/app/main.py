from fastapi import FastAPI, Depends, Query, HTTPException
from schema import Customer
import utils
from utils import load_all, add_customer, modify_customer_record, modify_customer_balance, delete_customer
from typing import List, Dict

app = FastAPI(title="NM ENTERPRISES")

@app.post('/create_customer')
def create_customer(new_customer: Customer, 
        products: str = Query(...,
        title= "Products Purchased",
        description= "Enter the prodcuts ',' seperated"
        )
):
    customer_dict = new_customer.model_dump(mode='json')
    try:
        add_customer(customer_dict, products)
        return{
            f"Customer Details Added"
        }
    
    except ValueError as error:
        raise HTTPException(status_code= 404, detail= str(error))

@app.post('/update_customer_record')
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
        raise HTTPException(status_code=404,detail= str(error))

@app.post('/update_record_balance')   
def update_customer_balance(customer_name: str = Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    ),
    balance: int = Query(...,
        gt= 0,
        title= "Enter Amount Given",
        description= "Enter the amount given"
    )
):
    try:
        modify_customer_balance(customer_name, balance)
        return {
            f"Customer Balance with name {customer_name} has been updated"
        }
    
    except Exception as error:
        raise HTTPException(status_code=404, detail= str(error))

@app.get('/get_all')
def get_all_customers():
    return {
        "All Customer Data": utils.load_all()
    }

@app.get('/customer_total_balance')
def get_customer_total_balance(customer_name: str = Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    )
):
    try:
        for customer in utils.load_all():
            if customer.get('Name') == customer_name.strip().lower():
                if customer['Total_Balance'] < 0:
                    return {
                            "Customer Name": customer_name,
                            "Balance Details":f"This customer has a credit amount of {abs(customer['Total_Balance'])}"
                        }
        
                else:
                    return {
                            "Customer Name": customer_name,
                            "Balance Details":f"This customer has a total balance of {customer['Total_Balance']}"
                    }
    except:
        raise HTTPException(status_code= 404, detail= "Name not found")

@app.get('/customer_history')
def get_customer_history(customer_name: str = Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    )
):
    try:
        for customer in utils.load_all():
            if customer['Name'].lower() == customer_name.lower():
                history  = customer['Products_Purchased']
                time = customer['Purchased_At']
                return {
                    'Customer Name': customer['Name'],
                    'Customer Buying History': history,
                    'Customer Buying Time': time,
                    'Customer Total Balance': customer['Total_Balance']
                }
        raise HTTPException(status_code= 404, detail= "Name not found")
    except Exception as error:
        raise HTTPException(status_code=404, detail= str(error))
            
@app.delete("/customer")
def remove_customer(customer_name: str= Query(...,
    min_length=1,
    title= "Customer Name",
    description='Enter name of the customer'
    )
):
    try:
        customer_detail = delete_customer(customer_name)
        return f"Customer record deleted with details : {customer_detail}"
    
    except ValueError as error:
        raise HTTPException(status_code=404, detail= str(error))
    
    
