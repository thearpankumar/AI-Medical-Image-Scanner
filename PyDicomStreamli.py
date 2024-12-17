import os
import pydicom
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Function to load .dcm files from the folder
def load_dicom_images(folder_path):
    # Ensure the folder exists
    if not os.path.isdir(folder_path):
        st.error(f"The folder at {folder_path} does not exist. Please check the path.")
        return [], []

    # Get all .dcm files in the directory
    dcm_files = [f for f in os.listdir(folder_path) if f.endswith('.dcm')]
    
    # If no .dcm files are found
    if not dcm_files:
        st.warning(f"No DICOM files found in the folder: {folder_path}")
        return [], []

    dcm_files.sort()  # Optional, sort files alphabetically
    dicom_images = [pydicom.dcmread(os.path.join(folder_path, f)) for f in dcm_files]
    images = [dcm.pixel_array for dcm in dicom_images]
    return images, dcm_files

# Streamlit Application
st.markdown("<h1 style='text-align: center;'>DICOM Image Viewer</h1>", unsafe_allow_html=True)

# Use Streamlit's column layout to center the folder path input box
col1, col2, col3 = st.columns([1, 2, 1])

# Folder path input inside the center column
with col2:
    folder_path = st.text_input("Enter the folder path containing DICOM files", "")

if folder_path:  # Only proceed if the user entered a folder path
    # Load images from the given folder path
    images, dcm_files = load_dicom_images(folder_path)

    if images:  # Only display images if loading was successful
        # Slider for selecting an image index (moving it to the center as well)
        image_index = st.slider('Select Image Index:', 0, len(images) - 1, 0)

        # Display the selected DICOM image
        selected_image = images[image_index]
        selected_file = dcm_files[image_index]

        # Display the image with Matplotlib in Streamlit
        fig, ax = plt.subplots()
        ax.imshow(selected_image, cmap="gray")
        ax.set_title(f"Image: {selected_file}")
        st.pyplot(fig)
