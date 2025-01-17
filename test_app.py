import streamlit as st
from PIL import Image
import concurrent.futures
from ultralytics import YOLO
import numpy as np
import pandas as pd

# Custom CSS for input styles
st.markdown(
    '''
    <style>
        .stTextInput > div > div > input { color: white; }
        .stTextInput > div > div > input::placeholder { color: white; }
    </style>
    ''', 
    unsafe_allow_html=True
)

# Logo and Header
st.markdown("<div style='text-align: center;'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/7-eleven_logo.svg/791px-7-eleven_logo.svg.png' width='120'></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Water Preventive Maintenance Classification 💦</h1>", unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.title("Settings")
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.2, 0.05)
st.sidebar.write("Adjust the confidence level for object detection.")

# Input fields
employee_name = st.text_input("Employee Name:")
branch_code = st.text_input("Branch Code:")

# Upload Images
uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Load YOLOv8 Model only once
@st.cache_resource
def load_model():
    model_path = r'C:\\selenium_web\\web_detect_tank\\best.pt'  # Path to your YOLOv8 model
    return YOLO(model_path)

try:
    st.sidebar.write("Loading YOLOv8 model...")
    model = load_model()
    st.sidebar.success("Model loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading model: {e}")
    st.stop()

# Initialize dataframe
columns = ["Filename", "Type", "Confidence"]
dataframe = pd.DataFrame(columns=columns)

# Function to process an image
def process_image(uploaded_file):
    try:
        # Open the uploaded image
        original_image = Image.open(uploaded_file).convert("RGB")

        # Convert PIL Image to numpy array
        image_array = np.array(original_image)

        # Perform detection
        results = model.predict(image_array, conf=confidence_threshold)

        # Extract detections and render image
        detections = results[0].boxes  # Get bounding boxes
        rendered_image = results[0].plot()  # Render detections on the image

        # Convert rendered numpy array back to PIL Image
        detected_image = Image.fromarray(rendered_image)

        # Prepare detection info
        detection_info = []
        types_detected = set()
        max_confidence = 0
        main_type = ""

        if detections is not None:
            for box in detections:
                class_name = results[0].names[int(box.cls)]  # Get class name
                confidence = box.conf.item() * 100  # Get confidence as percentage
                detection_info.append((class_name, confidence))
                types_detected.add(class_name)

                if confidence > max_confidence:
                    max_confidence = confidence
                    main_type = class_name

        # Determine final type based on detection rules
        if "correct" in types_detected and len(types_detected) > 1:
            final_type = "check"
        elif len(types_detected) > 1:
            final_type = main_type
        else:
            final_type = main_type if main_type else "undetected"

        # Update dataframe
        dataframe.loc[len(dataframe)] = [uploaded_file.name, final_type, max_confidence]

        return detected_image, detection_info
    except Exception as e:
        st.error(f"Error processing image {uploaded_file.name}: {e}")
        return None, None

# Dropdown menu for selecting an image
if uploaded_files:
    image_names = [file.name for file in uploaded_files]
    selected_image_name = st.selectbox("Select an Image to View:", image_names)

    # Process and display the selected image
    selected_file = next(file for file in uploaded_files if file.name == selected_image_name)
    
    # Process the selected image
    detected_image, detection_info = process_image(selected_file)

    if detected_image:
        st.markdown(f"#### Detected Image: {selected_file.name}")
        st.image(selected_file, use_container_width=True)

        # Get classification and confidence from DataFrame
        file_data = dataframe[dataframe["Filename"] == selected_file.name]
        if not file_data.empty:
            final_type = file_data.iloc[0]["Type"]
            max_confidence = file_data.iloc[0]["Confidence"]

            # Define additional text based on type
            additional_text = "Your PM work image meets the standard."
            if final_type == "Incomplied":
                additional_text = (
                    "Your PM work image doesn't meet the standard.<br>"
                    "Please check for cleanliness, there should be no residual water and no sediment."
                )
            elif final_type == "check":
                additional_text = (
                    "Your PM work image is under review. Multiple types detected."
                )
            elif final_type == "undetected":
                additional_text = (
                    "No detectable objects found in the image. Please recheck the image."
                )
            st.markdown(
                f'<div style="border: 2px solid black; padding: 10px; background-color: #f0f0f0; text-align: center;">'
                f'<h2 style="color: black">{final_type}</h2>'
                f'<p style="color: black">{additional_text}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.write("No detections found in the DataFrame.")
# Footer
st.markdown("<div class='footer'>Developed by Your Name | Contact: your.email@example.com</div>", unsafe_allow_html=True)
