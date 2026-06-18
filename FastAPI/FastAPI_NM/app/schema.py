from pydantic import BaseModel, Field
from typing import List, Dict, Annotated
from datetime import datetime, timezone

# keywords :-
# Name, Purchased At, Total_Balance

class Customer(BaseModel):
    Name: Annotated[str, Field(
        min_length=2,
    )]

    Purchased_At: datetime = Field(default_factory= datetime.now(timezone.utc).strftime("%d/%m/%y %H:%M:%S"))

    Total_Balance: Annotated[int, Field(
        title= "The Total Balance of the Customer"
    )]


