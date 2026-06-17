from pydantic import BaseModel

class TumorResponse(BaseModel):
    filename: str
    prediction: str