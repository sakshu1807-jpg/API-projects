from fastapi import FastAPI, responses, UploadFile, File
from schema import TumorResponse
from model_utils import preprocess_any_image
import numpy as np

app = FastAPI(title= "BrainTumor Classification Task")

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




