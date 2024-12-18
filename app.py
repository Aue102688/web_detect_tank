import streamlit as st
import torch
from PIL import Image
import os
import datetime
import pandas as pd

st.markdown(
    '''
    <style>
        .stTextInput > div > div > input { color: white; }
        .stTextInput > div > div > input::placeholder { color: white; }
    </style>
    ''', 
    unsafe_allow_html=True
)

# Displaying the 7-ELEVEN logo and the header with white font
st.markdown(
    f'<div style="text-align: center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/7-eleven_logo.svg/791px-7-eleven_logo.svg.png" alt="your_alt_text" width="150"></div>', 
    unsafe_allow_html=True
)
st.markdown(
    f'<div style="text-align: center; color: white;"><h1>Water Preventive Maintenance classification for 7-ELEVEN 💦</h1></div>', 
    unsafe_allow_html=True
)

# Getting user input for employee details
employee_name = st.text_input("Employee name :")
branch_code = st.text_input("Branch code:")

# อัปโหลดไฟล์ภาพ
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# โหลดโมเดล
model_path = r'C:\selenium_web\yolov5\best_e100_b16_s.pt'

try:
    # พยายามโหลดโมเดล
    st.write("Loading YOLOv5 model...")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    st.success("Model loaded successfully!")
except Exception as e:
    # แสดงข้อความ error หากโหลดโมเดลไม่ได้
    st.error(f"Error loading model: {e}")
    st.stop()

# หากมีการอัปโหลดไฟล์
if uploaded_files:
    # กด Submit เพื่อทำการตรวจจับ
    submit = st.button("Submit", key="submit_button")  # ใช้ key เพื่อหลีกเลี่ยงปัญหาซ้ำของ ID

    if submit:
        # ทำการตรวจจับสำหรับแต่ละภาพ
        for uploaded_file in uploaded_files:
            try:
                # โหลดรูปภาพจากไฟล์ที่อัปโหลด
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)

                # รันการตรวจจับวัตถุ
                st.write("Running object detection...")
                results = model(image)

                # ดึงข้อมูลจากผลลัพธ์ที่ตรวจจับได้
                detections = results.pandas().xyxy[0]  # จะแสดงผลเป็น DataFrame
                for index, row in detections.iterrows():
                    class_name = row['name']
                    conf_score = row['confidence']
                    st.write(f"Detected: {class_name} with confidence {conf_score:.2f}")
                    print("------------------------------",conf_score, "------------------------------")
                    # หากพบการตรวจจับที่ตรงกับเงื่อนไข (เช่น class_name == "Complied")
                    if class_name == "Complied":
                        folder_name = "Complied_images"
                    else:
                        folder_name = "Incomplied_images"
                
                    # Ensure the folder exists or create it
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)

                    # Save the uploaded image to the designated folder and store its path
                    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    image_path = f"{folder_name}/image_{current_time}.png"
                    image.save(image_path)

                    upload_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # เพิ่มบรรทัดนี้

                    additional_text = "Your PM work image meets the standard."
                    if class_name == "Incomplied":
                        additional_text = "Your PM work image doesn't meet the standard.<br>"
                        additional_text += "Please check for cleanliness, there should be no residual water and no sediment."

                    st.markdown(
                        f'<div style="border: 2px solid black; padding: 10px; background-color: #f0f0f0; text-align: center;">'
                        f'<h2 style="color: black">{class_name}</h2>'
                        f'<h3 style="color: black">score: {int(conf_score * 1000) / 10}%</h3>'
                        f'<p style="color: black">{additional_text}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    # เพิ่มระยะห่างระหว่างผลลัพธ์และรูปภาพถัดไป
                    st.markdown("<br><br>", unsafe_allow_html=True)

            except Exception as e:
                # แสดงข้อความ error หากมีปัญหาในขั้นตอนการตรวจจับ
                st.error(f"Error during object detection: {e}")
