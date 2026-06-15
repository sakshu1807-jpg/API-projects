from pydantic import BaseModel, Field
from typing import Dict, List, Annotated, Optional
from enum import Enum, IntEnum


class ChestPainTypeEnum(str, Enum):
    ATA = "ATA"
    TA = "TA"
    NAP = "NAP"
    ASY = "ASY"

class RestingECGEnum(str, Enum):
    NORMAL = "Normal"
    ST = "ST"
    LVH = "LVH"

class ExerciseAnginaEnum(str, Enum):
    YES = "Y"
    NO = "N"

class ST_SlopeEnum(str, Enum):
    UP = "Up"
    DOWN = "Down"
    FLAT = "Flat"

class Heart_Details(BaseModel):
    Age: Annotated[int, Field(...,
        ge= 1,
        title= "Age of the person"
    )]
    Sex: Annotated[str, Field(...,
        title= "Gender in (M/F)",
        description="Enter M for male and F for female"
    )]
    ChestPain: ChestPainTypeEnum = Field(...,
        title= 'Type of Chest Pain',
        description= 'Enter ATA / TA / NAP / ASY'
    )
    RestingBP: Annotated[int, Field(...,
        title= "Systolic Blood Pressure",
        description= "Resting systolic bp in (mm Hg) upon admission to hospital",
        ge = 50,
        le = 250
    )]
    Cholesterol: Annotated[int, Field(...,
        title= "Cholesterol level",
        description= "Serum Cholesterol level measured in mg/dL",
        ge= 80,
        le= 600
    )]
    FastingBS: Annotated[int, Field(...,
        title= "Fasting Blood Sugar",
        description="Fasting blood sugar > 120 mg/dL (True = 1, False = 0)",
        ge=0,
        le=1,
    )]
    RestingECG: RestingECGEnum = Field(...,
        title= "Resting Electro Cardiographic",
        description="Resting electrocardiographic results"
    )
    MaxHR: Annotated[int, Field(...,
        title= "Max Heart Rate",
        description="Maximum heart rate achieved during exercise stress testing",
        ge=60,
        le=220
    )]
    ExerciseAngina: ExerciseAnginaEnum = Field(...,
        title= "Exercise Angina",
        description="Exercise-induced angina (Y = Yes, N = No)"
    )
    Oldpeak: float = Field(...,
        title= "Oldpeak",
        description= "ST depression induced by exercise relative to rest",
        ge=-2.6,
        le=6.2,
    )
    ST_Slope: ST_SlopeEnum = Field(...,
        title= "ST SLOPE",
        description="The slope of the peak exercise ST segment (Up, Flat, Down)"
    )

class HeartResponseResult(IntEnum):
    HEALTHY = 0
    DISEASE = 1

class HeartPredictionResponse(BaseModel):
    HeartDisease: HeartResponseResult

