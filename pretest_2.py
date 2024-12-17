import streamlit as st
import torch
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import time

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

# Load YOLOv5 Model
model_path = r'C:\\selenium_web\\yolov5\\best_e100_b16_s.pt'

try:
    st.sidebar.write("Loading YOLOv5 model...")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    st.sidebar.success("Model loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading model: {e}")
    st.stop()

# Process Uploaded Images
if uploaded_files:
    st.markdown("### Processing Results:")
    results_data = []
    detected_images = []

    progress_bar = st.progress(0)
    total_files = len(uploaded_files)

    for idx, uploaded_file in enumerate(uploaded_files):
        try:
            original_image = Image.open(uploaded_file)
            results = model(original_image)

            # Collect statistics
            true_count = sum(result[-1] > confidence_threshold for result in results.pred[0])
            false_count = len(results.pred[0]) - true_count

            results_data.append({
                "Image Name": uploaded_file.name,
                "True": true_count,
                "False": false_count,
                "Confidence Avg": results.pred[0][:, -1].mean().item() if len(results.pred[0]) > 0 else 0
            })

            detected_images.append(Image.fromarray(results.render()[0]))

        except Exception as e:
            st.error(f"Error processing image {uploaded_file.name}: {e}")

        progress_bar.progress((idx + 1) / total_files)

    # Display DataFrame of results
    st.write("### Detection Summary:")
    df_results = pd.DataFrame(results_data)
    st.dataframe(df_results)

    # Pie Chart
    total_true = df_results['True'].sum()
    total_false = df_results['False'].sum()
    if total_true + total_false > 0:
        labels = ['True', 'False']
        # แปลงค่า total_true และ total_false ให้เป็น float หรือ list ก่อน
        sizes = [float(total_true), float(total_false)]
        colors = ['#90CAF9', '#1E88E5']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color': 'white'})
        ax.axis('equal')
        fig.patch.set_facecolor('black')
        st.pyplot(fig)

    # Image Navigation
    st.markdown("---")
    st.markdown("### Detected Images:")

    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    def next_image():
        if st.session_state.current_index < len(detected_images) - 1:
            st.session_state.current_index += 1

    def prev_image():
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1

    current_image = detected_images[st.session_state.current_index]
    # st.image(current_image, caption=f"Processed: {uploaded_files[st.session_state.current_index].name}", use_column_width=True)
    st.image(current_image, caption=f"Processed: {uploaded_files[st.session_state.current_index].name}", use_container_width=True)


    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("Previous", on_click=prev_image)
    with col3:
        st.button("Next", on_click=next_image)

# Footer
st.markdown("<div class='footer'>Developed by Your Name | Contact: your.email@example.com</div>", unsafe_allow_html=True)
