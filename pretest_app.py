import streamlit as st
import torch
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")  # จัด Layout ให้กึ่งกลาง

# Custom CSS for centering image
st.markdown(
    '''
    <style>
        .image-container { display: flex; justify-content: center; margin-top: 20px; }
    </style>
    ''', 
    unsafe_allow_html=True
)

# Logo และ Header
st.markdown(
    f'<div style="text-align: center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/7-eleven_logo.svg/791px-7-eleven_logo.svg.png" alt="7-ELEVEN Logo" width="120"></div>', 
    unsafe_allow_html=True
)
st.markdown(
    f'<div style="text-align: center; color: white;"><h1 style="font-size: 1.5rem;">Water Preventive Maintenance Classification for 7-ELEVEN 💦</h1></div>', 
    unsafe_allow_html=True
)

# Input
employee_name = st.text_input("Employee name:")
branch_code = st.text_input("Branch code:")

# Upload Images
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Load YOLOv5 Model
model_path = r'C:\\selenium_web\\yolov5\\best_e100_b16_s.pt'

try:
    st.write("Loading YOLOv5 model...")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Process Uploaded Images
if uploaded_files:
    results_count = {'True': 0, 'False': 0}
    detected_images = []

    for uploaded_file in uploaded_files:
        try:
            original_image = Image.open(uploaded_file)
            results = model(original_image)

            for result in results.pred[0]:
                if result[-1] > 0.5:
                    results_count['True'] += 1
                else:
                    results_count['False'] += 1

            detected_images.append(Image.fromarray(results.render()[0]))
        except Exception as e:
            st.error(f"Error processing image {uploaded_file.name}: {e}")

    # Display Pie Chart
    if results_count['True'] > 0 or results_count['False'] > 0:
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

        # ฟังก์ชันคำนวณ % สำหรับแต่ละส่วน
        def autopct_format(pct):
            return f"{pct:.1f}%" if pct > 0 else ""

        # Plot Pie Chart
        fig, ax = plt.subplots(figsize=(4, 4))
        fig.patch.set_facecolor('black')

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

    # Separate Pie Chart and Image with a blank line
    st.markdown("---")  # Add a horizontal line as a separator

    # Session State for Image Navigation
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    def next_image():
        if st.session_state.current_index < len(detected_images) - 1:
            st.session_state.current_index += 1

    def prev_image():
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1

    current_image = detected_images[st.session_state.current_index]

    # Display the Image in a New Row
    st.markdown("<div class='image-container'>", unsafe_allow_html=True)
    st.image(current_image, caption="Detected Objects", use_container_width=False, width=500)
    st.markdown("</div>", unsafe_allow_html=True)

    # Buttons for Navigation
    st.markdown("<div class='custom-buttons'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("Previous", on_click=prev_image)
    with col3:
        st.button("Next", on_click=next_image)
    st.markdown("</div>", unsafe_allow_html=True)
