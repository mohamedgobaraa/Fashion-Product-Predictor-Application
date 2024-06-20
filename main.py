import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io

st.title("Fashion product predictor")
st.subheader("Upload the image to analyze it")

uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.image(image, caption='Uploaded Image', use_column_width=True)

    analyser = st.button('Analyse Image')

    if analyser:
        model = YOLO("best.pt")

        results = model(image)

        detected_counts = {}

        for result in results:
            annotated_image = result.plot()

            annotated_image = Image.fromarray(annotated_image)

            st.image(annotated_image, caption='Annotated Image', use_column_width=True)

            for box in result.boxes:
                class_id = box.cls
                class_name = model.names[int(class_id)]
                
                if class_name in detected_counts:
                    detected_counts[class_name] += 1
                else:
                    detected_counts[class_name] = 1

        if detected_counts:
            st.write("Detected components:")
            for name, count in detected_counts.items():
                st.write(f"{name} x{count}")
        else:
            st.write("No components detected.")
