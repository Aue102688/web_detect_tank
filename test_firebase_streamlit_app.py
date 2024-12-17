import streamlit as st
import torch
from PIL import Image
import firebase_admin
from firebase_admin import credentials, storage
import io

# ตั้งค่า Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # ใช้ไฟล์ JSON ที่ได้จาก Firebase
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-firebase-project-id.appspot.com'  # แทนที่ด้วย Firebase Project ID ของคุณ
})
bucket = storage.bucket()

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

# ฟังก์ชันอัปโหลดไฟล์ไปยัง Firebase Storage
def upload_to_firebase(image_file, filename):
    try:
        blob = bucket.blob(filename)
        blob.upload_from_file(image_file, content_type="image/jpeg")
        blob.make_public()  # ทำให้ไฟล์สามารถเข้าถึงได้สาธารณะ
        return blob.public_url
    except Exception as e:
        st.error(f"Error uploading to Firebase: {e}")
        return None

# หากมีการอัปโหลดไฟล์
if uploaded_files:
    # แสดงภาพที่อัปโหลดและอัปโหลดไปยัง Firebase
    firebase_urls = []
    for uploaded_file in uploaded_files:
        try:
            # แปลงไฟล์ภาพให้อยู่ในรูปแบบที่อ่านได้
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded: {uploaded_file.name}", use_container_width=True)

            # อัปโหลดไปยัง Firebase
            with io.BytesIO() as image_buffer:
                image.save(image_buffer, format="JPEG")
                image_buffer.seek(0)
                url = upload_to_firebase(image_buffer, uploaded_file.name)
                if url:
                    st.success(f"Uploaded to Firebase: {url}")
                    firebase_urls.append(url)
        except Exception as e:
            st.error(f"Error processing file {uploaded_file.name}: {e}")

    # เมื่อกด Submit ให้ทำการตรวจจับ
    submit = st.button("Submit")
    if submit and firebase_urls:
        for url in firebase_urls:
            try:
                # ดาวน์โหลดภาพจาก Firebase
                st.write(f"Processing image from: {url}")
                blob = bucket.blob(url.split("/")[-1])
                image_data = blob.download_as_bytes()
                image = Image.open(io.BytesIO(image_data))

                # แสดงภาพต้นฉบับ
                st.image(image, caption="Image from Firebase", use_container_width=True)

                # รันการตรวจจับวัตถุ
                st.write("Running object detection...")
                results = model(image)

                # แสดงผลลัพธ์การตรวจจับ
                st.image(results.render()[0], caption="Detected Objects", use_container_width=True)
            except Exception as e:
                st.error(f"Error during object detection for {url}: {e}")
