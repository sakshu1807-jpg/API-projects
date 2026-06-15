from fastapi import FastAPI
from schema import Heart_Details, HeartPredictionResponse
from model_utils import preprocess_new_data, convert_dict_to_df, final_prediction

app = FastAPI(title= "Heart Disease Prediction API Model", version= "1.0")


@app.post('/', response_model= dict)
def heart_prediction(detail: Heart_Details):
    user_details = detail.model_dump()
    new_df = convert_dict_to_df(user_details)
    final_df = preprocess_new_data(new_df)
    prediction = final_prediction(final_df)
    if prediction == 0:
        message = "Low Risk : No significant signs of heart disease detected. Continue maintaining a healthy lifestyle"
    else:
        message = "High risk : The model indicates a high probability of heart disease. Please consult a doctor immediately."
    
    return {
        "prediction": prediction,
        "message": message 
    }


