import streamlit as st
import pydicom
import matplotlib.pyplot as plt
import numpy as np
from glob import glob

# Function to load DICOM files
def load_dicom_images(folder_path):
    dicom_files = glob(f"{folder_path}/*.dcm")
    dicom_images = []
    for file in dicom_files:
        ds = pydicom.dcmread(file)
        dicom_images.append(ds.pixel_array)
    return dicom_images

# Streamlit UI
st.title("DICOM Image Viewer")

# Upload folder path
folder_path = st.text_input("Enter the folder path containing .dcm files:")

if folder_path:
    try:
        dicom_images = load_dicom_images(folder_path)

        # Display images as layers
        st.sidebar.title("Layer Selector")
        num_layers = len(dicom_images)
        selected_layer = st.sidebar.slider("Select Layer", 0, num_layers - 1, 0)

        # Plot the selected layer
        fig, ax = plt.subplots()
        ax.imshow(dicom_images[selected_layer], cmap="gray")
        ax.axis("off")
        st.pyplot(fig)

        # Optionally, display all layers as thumbnails
        st.sidebar.title("All Layers")
        cols = st.sidebar.columns(5)  # Adjust for more/less thumbnails per row
        for i, img in enumerate(dicom_images):
            with cols[i % 5]:  # Adjust thumbnail grid
                st.image(img, use_column_width=True, caption=f"Layer {i}")

    except Exception as e:
        st.error(f"Error loading DICOM files: {e}")
else:
    st.info("Please enter a valid folder path to view DICOM images.")
