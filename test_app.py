import streamlit as st
import torch
from PIL import Image
import os
import datetime
import pandas as pd

# st.write("Current maxUploadSize:", st.get_option("server.maxUploadSize"))

# ตั้งค่าหน้าเว็บให้แสดงผลแบบ Wide layout
st.set_page_config(layout="wide")

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
# CSS สำหรับจัด layout และปรับขนาด box
st.markdown(
    """
    <style>
    .image-box {
        border: 2px solid black;
        padding: 10px;
        margin: 10px;
        background-color: #f0f0f0;
        width: 400px;  /* กำหนดความกว้าง */
        height: 400px; /* กำหนดความสูง */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .image-box img {
        max-width: 100%; /* ปรับขนาดรูปภาพให้พอดีกับ box */
        max-height: 300px; /* จำกัดความสูงของรูปภาพ */
        object-fit: contain; /* จัดการให้รูปภาพไม่ผิดสัดส่วน */
    }
    .image-box h2, .image-box h3, .image-box p {
        margin: 5px 0; /* กำหนดระยะห่างระหว่างข้อความ */
        color: black;
    }
    </style>
    """,
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
    st.write("Loading YOLOv5 model...")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# หากมีการอัปโหลดไฟล์
if uploaded_files:
    submit = st.button("Submit", key="submit_button")

    if submit:
        cols = st.columns(3)  # สร้าง 3 คอลัมน์สำหรับ layout

        for idx, uploaded_file in enumerate(uploaded_files):
            try:
                # เปิดรูปภาพ
                image = Image.open(uploaded_file)

                # สมมติว่า model ผลลัพธ์จากการตรวจจับวัตถุ (ทดแทนด้วยข้อมูลตัวอย่าง)
                class_name = "Complied"  # ตัวอย่าง
                conf_score = 0.85  # ตัวอย่างความแม่นยำ
                additional_text = (
                    "Your PM work image meets the standard."
                    if class_name == "Complied" else
                    "Your PM work image doesn't meet the standard.<br>"
                    "Please check for cleanliness, there should be no residual water and no sediment."
                )

                # จัดเก็บภาพในโฟลเดอร์ที่เหมาะสม
                folder_name = "Complied_images" if class_name == "Complied" else "Incomplied_images"
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                image_path = f"{folder_name}/image_{current_time}.png"
                image.save(image_path)

                # แสดงผลใน layout box
                col = cols[idx % 3]  # วนใช้คอลัมน์ที่มีอยู่ (3 คอลัมน์)
                with col:
                    st.markdown(
                        f"""
                        <div class="image-box">
                            <img src="data:image/png;base64,{st.image(image, use_container_width=True)}" alt="Uploaded Image">
                            <h2>{class_name}</h2>
                            <h3>Score: {int(conf_score * 1000) / 10}%</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.error(f"Error during object detection: {e}")