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
    results_count = {'True': 0, 'False': 0, 'Unknown': 0}  # เพิ่ม Unknown
    results_data = []
    detected_images = []

    progress_bar = st.progress(0)
    total_files = len(uploaded_files)

    for idx, uploaded_file in enumerate(uploaded_files):
        try:
            original_image = Image.open(uploaded_file)
            results = model(original_image)
            
            detections = results.pandas().xyxy[0]  # จะแสดงผลเป็น DataFrame
            for index, row in detections.iterrows():
                class_name = row['name']
                conf_score = row['confidence']
                st.write(f"Detected: {class_name} with confidence {conf_score:.2f}")
                print("------------------------------",conf_score, "------------------------------")
            
            # Collect statistics
            true_count = sum(result[-1] > confidence_threshold for result in results.pred[0])
            false_count = len(results.pred[0]) - true_count
            confidence_avg = results.pred[0][:, -1].mean().item() if len(results.pred[0]) > 0 else 0

            print("-------------------------",results)

        
            # Check for Unknown condition
            if confidence_avg == 0.5:
                results_count['Unknown'] += 1
            else:
                results_count['True'] += true_count
                results_count['False'] += false_count

            results_data.append({
                "Image Name": uploaded_file.name,
                "True": true_count,
                "False": false_count,
                "Confidence Avg": confidence_avg
            })

            detected_images.append(Image.fromarray(results.render()[0]))
        except Exception as e:
            st.error(f"Error processing image {uploaded_file.name}: {e}")

        progress_bar.progress((idx + 1) / total_files)

    # Display DataFrame of results
    st.write("### Detection Summary:")
    df_results = pd.DataFrame(results_data)
    st.dataframe(df_results)

    # Display Pie Chart
    if any(results_count.values()):
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

        # Pie Chart Data
        labels = []
        sizes = []
        colors = []

        if results_count['True'] > 0:
            labels.append('True')
            sizes.append(results_count['True'])
            colors.append('#90CAF9')  # สีฟ้าอ่อน

        if results_count['False'] > 0:
            labels.append('False')
            sizes.append(results_count['False'])
            colors.append('#1E88E5')  # สีน้ำเงินเข้ม

        if results_count['Unknown'] > 0:
            labels.append('Unknown')
            sizes.append(results_count['Unknown'])
            colors.append('#FFB300')  # สีเหลืองเข้ม

        # Convert sizes to List
        sizes = [s.item() if torch.is_tensor(s) else s for s in sizes]

        # Plot Pie Chart
        fig, ax = plt.subplots(figsize=(4, 4))
        fig.patch.set_facecolor('black')

        def autopct_format(pct):
            return f"{pct:.1f}%" if pct > 0 else ""

        if len(labels) > 1:
            # แสดงป้ายกำกับและเปอร์เซ็นต์หากมีหลายส่วน
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, autopct=autopct_format, startangle=90, colors=colors, 
                textprops={'color': 'white', 'fontsize': 12}
            )
            plt.setp(autotexts, size=12, weight="bold")
        else:
            # แสดงข้อความตรงกลางกรณีมีข้อมูลเดียว
            ax.pie(sizes, labels=None, startangle=90, colors=colors)
            center_label = labels[0]
            center_percent = f"{sizes[0] / sum(sizes) * 100:.1f}%"
            plt.text(0, 0, f"{center_percent}\n{center_label}", ha='center', va='center', fontsize=14, color='white')

        ax.axis('equal')  # ให้ Pie Chart เป็นวงกลม
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)


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
