import io
import pydicom
import tensorflow as tf
import numpy as np

def preprocess_any_image(image_bytes: bytes, filename: str) -> np.ndarray:
    """Preprocesses both standard images and medical DICOM (.dcm) files into 
    a normalized (224, 224, 1) grayscale tensor."""
    
    # 1. Handle DICOM files
    if filename.lower().endswith('.dcm'):
        # Read the raw DICOM bytes
        dicom_data = pydicom.dcmread(io.BytesIO(image_bytes))
        
        # Extract the raw pixel array
        img_array = dicom_data.pixel_array.astype(np.float32)
        
        # Rescale pixel values (Medical DICOMs often use 12 or 16-bit integers, not 0-255)
        # We normalize based on the maximum pixel value in this specific scan
        img_array = (img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array) + 1e-8)
        
        # Convert to a TensorFlow tensor and add the missing channel dimension -> (H, W, 1)
        tensor = tf.convert_to_tensor(img_array)
        tensor = tf.expand_dims(tensor, axis=-1)
        
        # Resize to your model's expected size
        tensor = tf.image.resize(tensor, [512,512])
        
    # 2. Handle standard web images (.jpg, .png, etc.)
    else:
        tensor = tf.io.decode_image(image_bytes, channels=1)
        tensor = tf.image.resize(tensor, [512,512])
        tensor = tensor / 255.0  # Standard normalization
        
    # 3. Add batch dimension -> (1, 224, 224, 1)
    tensor = tf.expand_dims(tensor, axis=0)
    
    return tensor.numpy()