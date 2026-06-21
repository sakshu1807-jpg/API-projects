from fastapi import FastAPI, responses, UploadFile, File, HTTPException
from schema import TumorResponse
from model_utils import preprocess_any_image
import numpy as np
import joblib
from pathlib import Path
from huggingface_hub import hf_hub_download
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # What happens on startup:
    global model
    repo_id = "SakshamManchanda/Brain_TumorModel"
    filename = "brain_tumor_detection_model.joblib"
    try:
        model_path = hf_hub_download(repo_id=repo_id, filename=filename)
        model = joblib.load(model_path)
        print("Model loaded successfully into FastAPI memory!")
    except Exception as error:
        print(f"Error loading model: {str(error)}")
    
    yield  # API is running here

app = FastAPI(title="BrainTumor Classification Task", lifespan=lifespan)

classes = ['glioma', 'meningioma', 'no_tumor', 'pituitary']

@app.post('/', response_model= TumorResponse)
async def prediction(file: UploadFile = File(...)):
    image_bytes = await file.read()

    filename = file.filename
    
    preprocessed_image = preprocess_any_image(image_bytes, filename)

    predictions = model.predict(preprocessed_image) # returns a 2d array of probabilities of each class
    prediction_index = np.argmax(predictions[0]) # returns index of the highest probability
    final_prediction = classes[prediction_index] # the name of the brain tumor

    return {
        'filename': filename,
        'prediction': final_prediction
    }

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows the Streamlit cloud app to connect safely
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




