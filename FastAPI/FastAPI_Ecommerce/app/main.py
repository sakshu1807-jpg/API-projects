from fastapi import FastAPI, HTTPException, Query, Path, Depends, Request
from services.fetch_database import get_all_products, add_product, delete_product, update_product
from schema.products_rule import Product, ProductUpdate
from uuid import UUID, uuid4
from datetime import datetime
app = FastAPI()

@app.middleware('http')
async def Lifecycle(request: Request, call_next):
    print("Before response")
    response = await call_next(Request)
    print("After Response")
    return response 

def repeat_step():
    return "Hello CLIENT. How May I Help You?"

@app.get("/") # Static Route: Gives same info every time we run it.
def read(dep = Depends(repeat_step)):
    return {"Message": "Welcome to FastAPI", "Greeting Message": dep}


@app.get("/products")
def get_product_by_queries(
    name: str = Query(
    default=None,
    max_length=50,
    min_length=1,
    description='Enter name of product'
    ),
    sort_by_price: bool = Query(
        default=False,
        description="Sort products by price"
    ),
    order: str = Query(
        default= 'asc',
        description="Sort products in ascending or descending order (asc/desc)?"
    ),
    limit: int = Query(
        default= 7,
        ge= 1,
        le= 100,
        description='Number of items you want to see'
    )
):
    if not name:
        return HTTPException(status_code=404, detail='Name Not Found')
    
    name = name.lower().strip()
    products = get_all_products()
    final_products = [p for p in products if name in p.get('name', '').lower()]
    if not final_products:
        return HTTPException(status_code=404, detail=f'product with name: {name} not found')
    
    length = len(final_products)
    
    if sort_by_price:
        reverse = order == 'desc'
        final_products = sorted(final_products, key= lambda x : x.get('price', 0), reverse=reverse)

    if limit < len(final_products):
        final_products = final_products[0:limit]
    else:
        limit = length
    
    
    return {'Total Products': length, 'Products Shown': limit, 'Products': final_products}


@app.get("/products/{product_id}")
def get_product_id(
    product_id: str = Path(
        ...,
        max_length=36,
        min_length=36,
        description='ID of the Product',
        example='a0752aq9-a1c8-412c-98b2-7c4084ef4699'
        )
):
    products = get_all_products()
    for product in products:
        if product['id'] == product_id:
            return product
    return HTTPException(status_code=404, detail='Product Id Not Found')


@app.post('/products', status_code=201)
def create_new_product(product: Product):
    product_dict = product.model_dump(mode='json')
    product_dict['id'] = str(uuid4())
    try:
        add_product(product_dict)
    except Exception as error:
        raise HTTPException(status_code=400, detail= str(error))
    return product_dict


@app.delete('/products/{product_id}')
def remove_product(product_id: str = Path(..., description='Enter Id of the product to remove')):
    try:
        output = delete_product(product_id)
        return {'Message':'The following are the product details which are now removed', 'product removed': output}
    except:
        raise HTTPException(status_code=404, detail='Id Not Found')


@app.put('/products/{product_id}')
def change_product_details(payload: ProductUpdate = ..., 
                    product_id: str = Path(..., description='Enter the UUID of the product', example=uuid4())):
        output = update_product(product_id, payload.model_dump(mode = 'json', exclude_none= True))
        return {'Message': 'The following details of the product are updated.', 'Product Details': output}
    
