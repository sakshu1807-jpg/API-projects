from pydantic import BaseModel, Field
from typing import  Annotated
from datetime import datetime
from zoneinfo import ZoneInfo

# keywords :-
# Name, Purchased At, Total_Balance

class Customer(BaseModel):
    Name: Annotated[str, Field(
        min_length=2,
    )]
    Purchased_At: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )

    Total_Balance: Annotated[int, Field(
        title= "The Total Balance of the Customer"
    )]


