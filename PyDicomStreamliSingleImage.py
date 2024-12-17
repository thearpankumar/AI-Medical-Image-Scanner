import streamlit as st
import pydicom
import numpy as np

def main():
    st.title("CT Scan Viewer")

    # Upload the DICOM file
    uploaded_file = st.file_uploader("Upload a DICOM file", type=["dcm"])

    if uploaded_file is not None:
        # Read the DICOM file
        ds = pydicom.dcmread(uploaded_file)

        # Extract the pixel data
        pixel_array = ds.pixel_array

        # Apply windowing to bring pixel values within the 0-255 range
        window_center = ds.WindowCenter[0]  # Assuming single window center
        window_width = ds.WindowWidth[0]  # Assuming single window width
        pixel_array = (pixel_array - window_center) / window_width
        pixel_array = pixel_array.clip(0, 1)  # Clip values to 0-1 range
        pixel_array = (pixel_array * 255).astype(np.uint8)  # Scale to 0-255 range

        # Display the image
        st.image(pixel_array, caption='CT Scan Image')

if __name__ == '__main__':
    main()