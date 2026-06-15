from pydantic import (BaseModel, AnyUrl, field_validator, model_validator, computed_field, 
Field,  EmailStr, AnyHttpUrl)
from typing import List, Dict, Annotated, Literal, Optional
from uuid import UUID
import datetime
# BaseModel from pydantic is the parent class.

# CREATE PRODUCT

class Dimensions(BaseModel):
    length: Annotated[float, Field(
        gt= 0,
        description='Length of the product (in cm)'
        )
    ]
    width: Annotated[float, Field(
        gt= 0,
        description='Width of the product (in cm)'
        )
    ]
    height: Annotated[float, Field(
        gt= 0,
        description='Height of the product (in cm)'
        )
    ]

class Seller(BaseModel):
    seller_id: UUID
    name: Annotated[str, Field(
        min_length=2,
        max_length=50,
        description='Name of the Seller',
        examples=['Mi Store', 'Samsung India']
        )
    ]
    email: Annotated[EmailStr, Field(
        min_length= 6,
        max_length=50,
        description='email of the seller',
        examples=['support@1stop.in', 'support@samsung.in']
        )
    ]
    website: Annotated[AnyHttpUrl, Field(
        description='website of the product seller',
        )
    ]

    @field_validator('email', mode='after')
    @classmethod
    def email_domain_validate(cls,value : EmailStr):
        allowed_domains = ['samsungstore.in', 'mistore.in', 'applestore.in', 'lgstore.in', 'dellstore.in']
        domain = value.split('@')[-1]
        if domain not in allowed_domains:
            raise ValueError(f"The domain {domain} is not allowed.")
        return value

class Product(BaseModel): # child class
    id: UUID
    sku: Annotated[str, Field(
        min_length=10, 
        max_length=20, 
        title= 'SKU',
        description='STOCK KEEPING UNIT',
        examples=['XIAO-359GB-001', 'RQQL-135GB-002'],
        )
    ]
    name: Annotated[str, Field(
        min_length=5,
        max_length=20,
        title= 'Name',
        description='Name of the product',
    )]
    description: Annotated[str, Field(
        min_length=25,
        max_length=40,
        title= 'Description',
        description='Product Description',
    )]
    category: Annotated[str, Field(
        min_length=2,
        max_length=20,
        title= 'Category',
        description='Product Category like Electronics, Clothing etc.',
    )]
    brand: Annotated[str, Field(
        min_length=1,
        max_length=20,
        title= 'Brand',
        description='Product Brand Name',
    )]
    price: Annotated[float, Field(
        ge= 1,
        strict= True,
        title= 'Price',
        description='Price of the product between 1 to 10 Lakhs',
    )]
    currency: Literal['INR'] = 'INR'

    discount_percent: Annotated[int, Field(
        ge= 0,
        le= 90,
        title= 'Product Discount',
        description='Product Discount in Percentage (0 - 90)',
    )]
    stock: Annotated[int, Field(
        ge= 0,
        title= 'Stock Available',
        description='Write the stock availability of the product',
    )]
    is_active: Annotated[bool, Field(
        title= 'Product Availability',
        description='Whether the product is available or not',
    )]
    rating: Annotated[float, Field(
        ge= 0,
        le= 5,
        title= 'Product Rating',
        description='Product Rating b/w (0 - 5)',
    )]
    tags: Annotated[Optional[List[str]], Field(
        default=None,
        max_length=10, #Len of list 
        title= 'Tags for the product (if any)',
        description='Tags for the product upto 10 only',
    )]
    image_urls: Annotated[list[AnyUrl], Field(
        max_length=1,
        title= 'Image Url for the product',
        description='Provide atleast 1 Image Url for the product',
    )]

    dimesnions_cm: Dimensions

    seller: Seller

    created_at: datetime.datetime = Field(default_factory= lambda: datetime.now(datetime.timezone.utc))

    @field_validator('sku', mode='after') #Works on one field at a time 
    @classmethod
    def sku_validator(cls, value: str):
        if '-' not in value:
            raise ValueError("SKU must have '-' in it.")
        
        last = value.split('-')[-1]
        if len(last) != 3 or last.isdigit() == False:
            raise ValueError("The last part of sku must contain 3 digits after '-' like -> '345'")
        
        return value
    
    @model_validator(mode= 'after')
    @classmethod
    def validate_stock_and_active(cls, model : Product):
        if model.stock == 0 and model.is_active == True:
            raise ValueError("The product with zero stock can't be active")
        
        if model.stock != 0 and model.is_active == False:
            raise ValueError("The product with stock must be active")
        
        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Product with discount must have a rating > 0")
        
        return model

    @computed_field # creates a new field
    @property # This is used with computed_field and makes that attribute(new field) in read-mode only.
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount_percent/100), 2)
    
    @computed_field
    @property
    def product_volume(self) -> float:
        return round(self.dimesnions_cm.length * self.dimesnions_cm.width*self.dimesnions_cm.height,2)
    
#UPDATE PRODUCT

class DimensionsUpdate(BaseModel):
    length: Optional[float] = Field(gt= 0.0)
    
    width: Optional[float] = Field(gt = 0.0)
    
    height: Optional[float] = Field(gt = 0.0)

class SellerUpdate(BaseModel):
    seller_id: Optional[UUID]
    name: Optional[str] = Field(
        min_length=2,
        max_length=50,
        description='Name of the Seller',
        examples=['Mi Store', 'Samsung India']
        )
    
    email: Optional[EmailStr] = Field(
        min_length= 6,
        max_length=50,
        description='email of the seller',
        examples=['support@1stop.in', 'support@samsung.in']
        )
    
    website: Optional[AnyHttpUrl] = Field(
        description='Website of the product seller',
        )
    
    @field_validator('email', mode='after')
    @classmethod
    def email_domain_validate(cls,value : EmailStr):
        allowed_domains = ['samsungstore.in', 'mistore.in', 'applestore.in', 'lgstore.in', 'dellstore.in']
        domain = value.split('@')[-1]
        if domain not in allowed_domains:
            raise ValueError(f"The domain {domain} is not allowed.")
        return value

class ProductUpdate(BaseModel): 
    id: UUID
    sku: Optional[str] = Field(
        min_length=10, 
        max_length=20, 
        title= 'SKU',
        description='STOCK KEEPING UNIT',
        examples=['XIAO-359GB-001', 'RQQL-135GB-002'],
        )
    
    name: Optional[str] = Field(
        min_length=5,
        max_length=20,
        title= 'Name',
        description='Name of the product',
    )
    description: Optional[str] = Field(
        min_length=25,
        max_length=60,
        title= 'Description',
        description='Product Description',
    )
    category: Optional[str] = Field(
        min_length=2,
        max_length=20,
        title= 'Category',
        description='Product Category like Electronics, Clothing etc.',
    )
    brand: Optional[str] = Field(
        min_length=1,
        max_length=20,
        title= 'Brand',
        description='Product Brand Name',
    )
    price: Optional[float] = Field(
        ge= 1,
        strict= True,
        title= 'Price',
        description='Price of the product between 1 to 10 Lakhs',
    )
    currency: Literal['INR'] = 'INR'

    discount_percent: Optional[float] = Field(
        ge= 0,
        le= 90,
        title= 'Product Discount',
        description='Product Discount in Percentage (0 - 90)',
    )
    stock: Optional[int] = Field(
        ge= 0,
        title= 'Stock Available',
        description='Write the stock availability of the product',
    )
    is_active: Optional[bool] = Field(
        title= 'Product Availability',
        description='Whether the product is available or not',
    )
    rating: Optional[float] = Field(
        ge= 0,
        le= 5,
        title= 'Product Rating',
        description='Product Rating b/w (0 - 5)',
    )
    tags: Optional[Optional[List[str]]] = Field(
        default=None,
        max_length=10, #Len of list 
        title= 'Tags for the product (if any)',
        description='Tags for the product upto 10 only',
    )
    image_urls: Optional[list[AnyUrl]] = Field(
        min_length=1,
        max_length= 5,
        title= 'Image Url for the product',
        description='Provide atleast 1 Image Url for the product',
    )

    dimensions_cm: Optional[DimensionsUpdate] 

    seller: Optional[SellerUpdate] 
    created_at: datetime.datetime = Field(default_factory= lambda: datetime.now(datetime.timezone.utc))

    @field_validator('sku', mode='after') #Works on one field at a time 
    @classmethod
    def sku_validator(cls, value: str):
        if '-' not in value:
            raise ValueError("SKU must have '-' in it.")
        
        last = value.split('-')[-1]
        if len(last) != 3 or last.isdigit() == False:
            raise ValueError("The last part of sku must contain 3 digits after '-' like -> '345'")
        
        return value

    @model_validator(mode= 'after')
    @classmethod
    def validate_stock_and_active(cls, model : Product):
        if model.stock == 0 and model.is_active == True:
            raise ValueError("The product with zero stock can't be active")
        
        if model.stock != 0 and model.is_active == False:
            raise ValueError("The product with stock must be active")
        
        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Product with discount must have a rating > 0")
        
        return model

    @computed_field # creates a new field
    @property # This is used with computed_field and makes that attribute(new field) in read-mode only.
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount_percent/100), 2)
    
    @computed_field
    @property
    def product_volume(self) -> float:
        
        return round(self.dimensions_cm.length * self.dimensions_cm.width * self.dimensions_cm.height,2)