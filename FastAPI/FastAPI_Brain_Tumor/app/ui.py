import streamlit as st
import requests
import io
from PIL import Image

# 1. Set up Page Configurations
st.set_page_config(
    page_title="Brain Tumor ImageClassifier",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Brain Tumor Classification Dashboard")
st.write("Upload a regular brain MRI image (.jpg, .png) or a medical DICOM file (.dcm) to analyze.")

# 2. Define Backend Target Endpoint
# (Ensure your FastAPI server is running on uvicorn app:main --reload)
FASTAPI_URL = "https://sakshammanchanda-brain-tumor-backend.hf.space"

# 3. Handle File Uploads via UI Widget
uploaded_file = st.file_uploader(
    "Choose an MRI Scan file...", 
    type=["jpg", "jpeg", "png", "dcm"]
)

if uploaded_file is not None:
    st.info(f"📂 File loaded: {uploaded_file.name}")
    
    # Visual UI handling depending on extension
    if not uploaded_file.name.lower().endswith('.dcm'):
        # Display preview for standard images
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded MRI Scan Preview", use_container_width=True)
    else:
        # Inform the user that DICOMs don't preview natively without extra steps
        st.warning("⚠️ DICOM file detected. Metadata and raw arrays will be processed natively by the backend.")

    # 4. Action Button to Trigger Prediction
    if st.button("🚀 Analyze Scan"):
        # We display the educational warning right above the spinner for transparency
        st.warning(
            "⏳ **Note for Doctors/Users:** If this is the first request in a while, "
            "our secure medical backend on HuggingFace may take up to 2-3 minutes to wake up "
            "and load the 1.6 GB neural network from Hugging Face. Please do not close this tab."
        )
        
        with st.spinner("Processing image through neural network..."):
            try:
                # Convert uploaded file data into the binary format FastAPI expects
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                # OPTIMIZED: Added timeout=180 (3 minutes) so the request doesn't instantly snap/fail
                response = requests.post(FASTAPI_URL, files=files, timeout=180)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis Complete!")
                    
                    # Highlight the prediction metrics inside clean UI cards
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Detected Classification", value=result["prediction"].upper().replace('_', ' '))
                    with col2:
                        st.metric(label="Target Source File", value=result["filename"])
                        
                else:
                    st.error(f"Backend Server Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("❌ The request timed out. The backend server took too long to wake up and process the file. Please try clicking 'Analyze Scan' again.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Failed! Please verify that your FastAPI application backend server is running and accessible.")
