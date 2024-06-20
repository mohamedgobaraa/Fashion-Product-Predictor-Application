import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io

st.title("Fashion product predictor")
st.subheader("Upload the image to analyze it")

uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)

    analyser = st.button('Analyse Image')

    if analyser:
        # Load the model
        model = YOLO("best.pt")

        # Run the model on the uploaded image
        results = model(image)

        # Dictionary to store detected component names and their counts
        detected_counts = {}

        for result in results:
            # Plot the results
            annotated_image = result.plot()  # This returns a numpy array

            # Convert the numpy array to a PIL Image
            annotated_image = Image.fromarray(annotated_image)

            # Display the annotated image
            st.image(annotated_image, caption='Annotated Image', use_column_width=True)

            # Extract and display detected component names
            for box in result.boxes:
                class_id = box.cls  # Get the class ID of the detected object
                class_name = model.names[int(class_id)]  # Get the class name using the model's names attribute
                
                # Update the count of the detected class name
                if class_name in detected_counts:
                    detected_counts[class_name] += 1
                else:
                    detected_counts[class_name] = 1

        # Display the list of detected names and their counts
        if detected_counts:
            st.write("Detected components:")
            for name, count in detected_counts.items():
                st.write(f"{name} x{count}")
        else:
            st.write("No components detected.")
