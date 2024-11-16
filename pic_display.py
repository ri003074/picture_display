import streamlit as st
import os
from PIL import Image


def pic_display():
    st.set_page_config(
        page_title="Image Display",  # Page title
        layout="wide"  # Set layout to "wide"
    )

    # Initialize session state for directory path and reload flag
    if "directory_path" not in st.session_state:
        st.session_state["directory_path"] = ""
    if "reload" not in st.session_state:
        st.session_state["reload"] = False

    # Sidebar instructions
    st.sidebar.write("Please specify a directory containing PNG files.")

    # Directory path input field
    directory_path = st.sidebar.text_input("Enter directory path", key="directory_path")

    # Image width and number of columns settings
    image_width = st.sidebar.slider("Image width (px)", min_value=50, max_value=400, value=150, step=10)
    num_columns = st.sidebar.slider("Number of Columns", min_value=1, max_value=5, value=2, step=1)

    # Reload button to refresh the images
    if st.sidebar.button("Reload"):
        st.session_state["reload"] = not st.session_state["reload"]  # Toggle reload flag

    # Display images if a valid directory path is provided
    if directory_path:
        # Check if the directory exists
        if os.path.isdir(directory_path):
            # Get all PNG files in the directory
            png_files = [f for f in os.listdir(directory_path) if f.endswith('.png')]

            # Display PNG files if they exist
            if png_files:
                st.title("PNG File Gallery")

                # Display images in specified number of columns
                for i in range(0, len(png_files), num_columns):
                    cols = st.columns(num_columns)  # Create the specified number of columns
                    for j in range(num_columns):
                        if i + j < len(png_files):  # Check index range
                            file_name = png_files[i + j]
                            file_path = os.path.join(directory_path, file_name)
                            image = Image.open(file_path)

                            # Display image and caption in each column
                            with cols[j]:
                                st.image(image, caption=file_name, width=image_width)
            else:
                st.warning("No PNG files found in the specified directory.")
        else:
            st.error("Invalid directory path.")
    else:
        st.info("Please specify a directory.")
