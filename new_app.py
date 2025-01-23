import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from ultralytics import YOLO
import matplotlib.pyplot as plt
import subprocess
import os
import sys

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
st.sidebar.write("Adjust settings as needed.")

# Input fields
employee_name = st.text_input("Employee Name:")
branch_code = st.text_input("Branch Code:")

# Add Date Input Fields
st.sidebar.header("Input Date Information")
date = st.sidebar.number_input("Day (1-31):", min_value=1, max_value=31, value=1)
day_of_week = st.sidebar.selectbox(
    "Day of the Week:",
    options=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    format_func=lambda x: x,
    index=0
)
month = st.sidebar.number_input("Month (1-12):", min_value=1, max_value=12, value=1)
year = st.sidebar.number_input("Year:", min_value=1900, max_value=2100, value=2023)

# Convert day_of_week to numeric
week_day_mapping = {"Sunday": 1, "Monday": 2, "Tuesday": 3, "Wednesday": 4, "Thursday": 5, "Friday": 6, "Saturday": 7}
day_of_week_numeric = week_day_mapping[day_of_week]

# Upload Images
uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if "dataframe" not in st.session_state:
    st.session_state["dataframe"] = pd.DataFrame(columns=["Filename", "Class Predict", "Confidence"])


def get_dataframe():
    return st.session_state["dataframe"]

# Load YOLOv8 Model only once
@st.cache_resource
def load_model():
    model_path = r'C:\selenium_web\web_detect_tank\best_e100_b16_Beta.pt'  # Path to your YOLOv8 model
    return YOLO(model_path)

try:
    st.sidebar.write("Loading YOLOv8 model...")
    model = load_model()
    st.sidebar.success("Model loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading model: {e}")
    st.stop()


# Function to process an image
def process_image(uploaded_file):
    try:
        # Open the uploaded image
        original_image = Image.open(uploaded_file).convert("RGB")

        # Convert PIL Image to numpy array
        image_array = np.array(original_image)

        # Perform detection
        results = model.predict(image_array)  # Removed conf=confidence_threshold

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

        # Define final type based on conditions
        if "correct" in types_detected and "incorrect" in types_detected and "fail" in types_detected:
            # Check if any class has confidence less than 90%
            if any(conf < 90 for _, conf in detection_info):
                final_type = "check"
            else:
                final_type = main_type
        elif "correct" in types_detected and len(types_detected) > 1:
            final_type = "check"
        elif len(types_detected) > 1:
            final_type = main_type
        else:
            final_type = main_type if main_type else "check"

        # Update dataframe with filename, class prediction, and confidence
        dataframe = get_dataframe()
        dataframe.loc[len(dataframe)] = [uploaded_file.name, final_type, max_confidence]
        st.session_state["dataframe"] = dataframe

        return detected_image, detection_info
    except Exception as e:
        st.error(f"Error processing image {uploaded_file.name}: {e}")
        return None, None

# Automatically process uploaded images
if uploaded_files:
    for uploaded_file in uploaded_files:
        process_image(uploaded_file)

    # Sidebar toggle for viewing options
    view_option = st.sidebar.radio("View Option", ("Show DataFrame", "Show Images"))

    # Show DataFrame
    if view_option == "Show DataFrame":
        # Display the DataFrame with results
        st.write("### Detection Results")
        dataframe = get_dataframe()
        
        # Remove file extensions from filenames
        dataframe["Filename"] = dataframe["Filename"].str.replace(r"\.(jpg|jpeg|png)$", "", regex=True)

        st.dataframe(dataframe)

        # Add download button for CSV
        if not dataframe.empty:
            # แสดงแถบใส่ชื่อไฟล์
            file_name_input = st.text_input("Enter file name to save (without extension):")
            
            # ถ้าใส่ชื่อไฟล์แล้ว
            if file_name_input:
                csv = dataframe.to_csv(index=False, header=True).encode('utf-8')
                st.download_button(
                    label="Download Data as CSV",
                    data=csv,
                    file_name=f"{file_name_input}.csv",
                    mime="text/csv",
                )
            else:
                # ถ้าไม่ได้ใส่ชื่อไฟล์
                st.download_button(
                    label="Download Data as CSV",
                    data=b"",  # ส่งข้อมูลว่าง
                    disabled=True  # ทำให้ปุ่มไม่สามารถคลิกได้
                )
                st.error("Please enter a file name to save.")


        # Display Pie Chart
        if not dataframe.empty:
            st.write("### Classification Distribution")
            class_counts = dataframe["Class Predict"].value_counts()
            class_percentages = (class_counts / len(dataframe)) * 100

            fig, ax = plt.subplots()
            ax.pie(class_percentages, labels=class_counts.index, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
            ax.axis("equal")  # Equal aspect ratio ensures the pie chart is a circle
            st.pyplot(fig)

    # Show Images
    elif view_option == "Show Images":
        # Show all images toggle
        show_all = st.button("Show All")
        if 'show_all_state' not in st.session_state:
            st.session_state.show_all_state = False

        # Toggle between showing all images and just one
        if show_all:
            st.session_state.show_all_state = not st.session_state.show_all_state

        # Display all images or selected image based on the toggle
        if uploaded_files:
            if st.session_state.show_all_state:
                for uploaded_file in uploaded_files:
                    # Process the image
                    detected_image, detection_info = process_image(uploaded_file)

                    if detected_image:
                        st.markdown(f"#### Detected Image: {uploaded_file.name}")
                        st.image(uploaded_file, use_container_width=True)
                        # st.image(detected_image, use_container_width=True)

                        # Get classification and confidence from DataFrame
                        dataframe = get_dataframe()
                        file_data = dataframe[dataframe["Filename"] == uploaded_file.name]
                        if not file_data.empty:
                            final_type = file_data.iloc[0]["Class Predict"]
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
                                f'</div>'
                                f'<br>'
                                f'<br>',  # เพิ่มช่องว่างหลัง div
                                unsafe_allow_html=True
                            )

                        else:
                            st.write("No detections found in the DataFrame.")
            else:
                # Process and display the selected image
                selected_image_name = st.selectbox("Select an Image to View:", [file.name for file in uploaded_files])
                selected_file = next(file for file in uploaded_files if file.name == selected_image_name)
                
                # Process the selected image
                detected_image, detection_info = process_image(selected_file)

                if detected_image:
                    st.markdown(f"#### Detected Image: {selected_file.name}")
                    st.image(selected_file, use_container_width=True)

                    # Get classification and confidence from DataFrame
                    dataframe = get_dataframe()
                    file_data = dataframe[dataframe["Filename"] == selected_file.name]
                    if not file_data.empty:
                        final_type = file_data.iloc[0]["Class Predict"]
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


# RPA Button to trigger RPA process and load images
if st.button("RPA"):
    try:
        # แจ้งให้ผู้ใช้ทราบว่า RPA กำลังทำงาน
        st.sidebar.write("Running RPA script to fetch images...")

        # เรียกใช้ RPA script (รอจนกระทั่งเสร็จสิ้น)
        result = subprocess.run([
            "python", "test_rpa.py", str(date), str(day_of_week_numeric), str(month), str(year)
        ], capture_output=True, text=True)

        print(result)
        
        # ตรวจสอบผลลัพธ์จาก RPA script
        if result.returncode == 0:
            st.sidebar.success("RPA script completed successfully!")

            image_folder = "download_images"
            if not os.path.exists(image_folder):
                st.error(f"The folder '{image_folder}' does not exist.")
            else:
                # โหลดไฟล์ภาพจากโฟลเดอร์ที่ RPA script บันทึกไว้
                image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]

                st.session_state["dataframe"] = pd.DataFrame(columns=["Filename", "Class Predict", "Confidence"])

                if image_files:
                    results = []  # เก็บข้อมูล detection ทั้งหมด
                    for image_file in image_files:
                        image_path = os.path.join(image_folder, image_file)

                        # เปิดไฟล์ภาพและประมวลผล
                        with open(image_path, "rb") as img_file:
                            detected_image, detection_info = process_image(img_file)

                            if detected_image:
                                if isinstance(detection_info, list) and detection_info:  # ตรวจสอบว่ามีข้อมูล
                                    results.append({
                                        "Filename": image_file,
                                        "Detection Info": detection_info
                                    })

                                else:
                                    st.warning(f"Skipped invalid detection info for {image_file}: {detection_info}")

                    # สร้าง DataFrame จากผลลัพธ์ทั้งหมด
                    dataframe = get_dataframe()
                    st.write("### Detection Results")
                    st.dataframe(dataframe)

                    # เพิ่มปุ่มดาวน์โหลด
                    if not dataframe.empty:
                        file_name_input = st.text_input("Enter file name to save (without extension):")
                        if file_name_input:
                            csv = dataframe.to_csv(index=False, header=True).encode("utf-8")
                            st.download_button(
                                label="Download Data as CSV",
                                data=csv,
                                file_name=f"{file_name_input}.csv",
                                mime="text/csv",
                            )
                        else:
                            st.error("Please enter a file name to save.")

                    # แสดง Pie Chart
                    if not dataframe.empty:
                        st.write("### Classification Distribution")
                        class_counts = dataframe["Class Predict"].value_counts()
                        class_percentages = (class_counts / len(dataframe)) * 100

                        fig, ax = plt.subplots()
                        ax.pie(
                            class_percentages,
                            labels=class_counts.index,
                            autopct="%1.1f%%",
                            startangle=90,
                            colors=plt.cm.Paired.colors,
                        )
                        ax.axis("equal")  # ทำให้กราฟวงกลมเป็นวงกลมจริง ๆ
                        st.pyplot(fig)

                    # แสดงภาพที่ประมวลผลแล้ว
                    st.write("### Processed Images")
                    for result in results:
                        st.markdown(f"#### Detected Image: {result['Filename']}")
                        st.image(os.path.join(image_folder, result["Filename"]), use_container_width=True)

                        # แสดงข้อมูลเพิ่มเติม (เฉพาะชื่อคลาส)
                        detection_text = "<br>".join(
                            [f"{cls}" for cls, _ in result["Detection Info"]]
                        )
                        # Define additional text based on type
                        additional_text = "Your PM work image meets the standard."
                        if detection_text == "Incomplied":
                            additional_text = (
                                "Your PM work image doesn't meet the standard.<br>"
                                "Please check for cleanliness, there should be no residual water and no sediment."
                            )
                        elif detection_text == "check":
                            additional_text = (
                                "Your PM work image is under review. Multiple types detected."
                            )
                        elif detection_text == "undetected":
                            additional_text = (
                                "No detectable objects found in the image. Please recheck the image."
                            )
                        st.markdown(
                            f'<div style="border: 2px solid black; padding: 10px; background-color: #f0f0f0; text-align: center;">'
                            f'<h2 style="color: black">{detection_text}</h2>'
                            f'<p style="color: black">{additional_text}</p>'
                            f'</div>'
                            f'<br>'
                            f'<br>',
                            unsafe_allow_html=True
                        )
                else:
                    st.error(f"No images were downloaded by the RPA script in folder '{image_folder}'.")
        else:
            st.error(f"RPA script failed. Error: {result.stderr}")

    except subprocess.CalledProcessError as e:
        st.error(f"Error running RPA: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


# Footer
st.markdown("<div class='footer'>Developed by Your Name | Contact: satit102688@gmail.com</div>", unsafe_allow_html=True)
