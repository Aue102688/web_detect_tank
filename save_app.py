import streamlit as st
from PIL import Image
import concurrent.futures
from ultralytics import YOLO
import numpy as np

# Custom CSS
st.markdown("""
    <style>
        .image-container { display: flex; justify-content: center; margin-top: 20px; }
        .custom-buttons { text-align: center; margin-top: 10px; }
        .footer { text-align: center; margin-top: 20px; font-size: 0.9rem; color: gray; }
    </style>
""", unsafe_allow_html=True)

# Logo and Header
st.markdown("<div style='text-align: center;'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/7-eleven_logo.svg/791px-7-eleven_logo.svg.png' width='120'></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Water Preventive Maintenance Classification 💦</h1>", unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.title("Settings")
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
st.sidebar.write("Adjust the confidence level for object detection.")

# Input fields
employee_name = st.text_input("Employee Name:")
branch_code = st.text_input("Branch Code:")

# Upload Images
uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Load YOLOv8 Model only once
@st.cache_resource
def load_model():
    model_path = r'C:\selenium_web\web_detect_tank\best.pt'  # Path to your YOLOv8 model
    return YOLO(model_path)

try:
    st.sidebar.write("Loading YOLOv8 model...")
    model = load_model()
    st.sidebar.success("Model loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading model: {e}")
    st.stop()

# Process Uploaded Images
if uploaded_files:
    st.markdown("### Processing Results:")

    def process_image(uploaded_file):
        try:
            # Open the uploaded image
            original_image = Image.open(uploaded_file).convert("RGB")
            
            # Convert PIL Image to numpy array
            image_array = np.array(original_image)
            
            # Perform detection
            results = model.predict(image_array, conf=confidence_threshold)
            
            # Render the detected image
            rendered_image = results[0].plot()  # `plot()` renders the detections on the image
            
            # Convert rendered numpy array back to PIL Image
            detected_image = Image.fromarray(rendered_image)
            
            return detected_image
        except Exception as e:
            st.error(f"Error processing image {uploaded_file.name}: {e}")
            return None

    # Process images in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        detected_images = list(executor.map(process_image, uploaded_files))

    # Display Uploaded and Detected Images
    for idx, (uploaded_file, detected_image) in enumerate(zip(uploaded_files, detected_images)):
        if detected_image:
            # st.markdown(f"#### Uploaded Image: {uploaded_file.name}")
            # st.image(Image.open(uploaded_file), caption=f"Original: {uploaded_file.name}", use_container_width=True)
            st.markdown("#### Detected Image:")
            st.image(detected_image, caption=f"Processed: {uploaded_file.name}", use_container_width=True)

# Footer
st.markdown("<div class='footer'>Developed by Your Name | Contact: your.email@example.com</div>", unsafe_allow_html=True)
