from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from schema import TumorResponse
from model_utils import preprocess_any_image
import numpy as np
import joblib
from huggingface_hub import hf_hub_download
import os
# Force TensorFlow to suppress all warning logs and skip GPU hardware probing
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    repo_id = "SakshamManchanda/Brain_TumorModel"
    filename = "brain_tumor_detection_model.joblib"
    
    print("LOG: Application starting up... Attempting to connect to HF Hub.")
    try:
        # OPTIMIZED: Removed the parameter entirely to avoid any typo or version bugs
        model_path = hf_hub_download(
            repo_id=repo_id, 
            filename=filename
        )
        print(f"LOG: Model downloaded to path: {model_path}. Loading with joblib...")
        model = joblib.load(model_path)
        print("LOG: Model loaded successfully into memory!")
    except Exception as error:
        print(f"LOG: Error loading model: {str(error)}")
    yield

app = FastAPI(title="BrainTumor Classification Task", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "Healthy", "message": "Brain Tumor API backend is operational!"}

# Essential CORS configuration for your Streamlit UI to connect safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classes = ['glioma', 'meningioma', 'no_tumor', 'pituitary']

@app.post('/', response_model= TumorResponse)
async def prediction(file: UploadFile = File(...)):
    image_bytes = await file.read()
    filename = file.filename
    
    preprocessed_image = preprocess_any_image(image_bytes, filename)
    predictions = model.predict(preprocessed_image)
    prediction_index = np.argmax(predictions[0])
    final_prediction = classes[prediction_index]

    return {
        'filename': filename,
        'prediction': final_prediction
    }
