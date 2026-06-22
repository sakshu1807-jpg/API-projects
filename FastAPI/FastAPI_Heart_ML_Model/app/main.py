from fastapi import FastAPI
from schema import Heart_Details
from model_utils import preprocess_new_data, convert_dict_to_df, final_prediction
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pickle

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, scaler, oe
    try:
        model_path = 'rf_model.pkl'
        model = pickle.load(model_path)
        scaler_path = 'StandardScaler.pkl'
        scaler = pickle.load(scaler_path)
        oe_path = 'OrdinalEncoder.pkl'
        oe = pickle.load(oe_path)
        print("LOG: Model essentials loaded successfully.")
    except Exception as error:
        print(f"LOG: Error loading model essentials: {str(error)}.")

    yield

app = FastAPI(title= "Heart Disease Prediction API Model", version= "1.0", lifespan=lifespan)

@app.post('/')
def prediction(detail: Heart_Details):
    user_details = detail.model_dump()
    new_df = convert_dict_to_df(user_details)
    final_df = preprocess_new_data(new_df, oe, scaler)
    prediction = final_prediction(final_df, model)
    if prediction == 0:
        message = "Low Risk : No significant signs of heart disease detected. Continue maintaining a healthy lifestyle"
    else:
        message = "High risk : The model indicates a high probability of heart disease. Please consult a doctor immediately."
    
    return {
        "prediction": prediction,
        "message": message 
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)
