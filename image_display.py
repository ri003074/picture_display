import streamlit as st
import os
from PIL import Image


def image_display():
    st.set_page_config(
        page_title="Image Display",  # Page title
        layout="wide"  # Set layout to "wide"
    )

    # Initialize session state for directory paths and reload flag
    if "directory_path_1" not in st.session_state:
        st.session_state["directory_path_1"] = ""
    if "directory_path_2" not in st.session_state:
        st.session_state["directory_path_2"] = ""
    if "reload" not in st.session_state:
        st.session_state["reload"] = False

    # Sidebar instructions
    st.sidebar.write("Please specify two directories containing PNG files.")

    # Directory path input fields
    directory_path_1 = st.sidebar.text_input("Enter first directory path", key="directory_path_1")
    directory_path_2 = st.sidebar.text_input("Enter second directory path", key="directory_path_2")

    # Image width and number of columns settings
    image_width = st.sidebar.slider("Image width (px)", min_value=50, max_value=400, value=150, step=10)
    num_columns = st.sidebar.slider("Number of Columns", min_value=1, max_value=5, value=2, step=1)

    # Reload button to refresh the images
    if st.sidebar.button("Reload"):
        st.session_state["reload"] = not st.session_state["reload"]  # Toggle reload flag

    # Display images if valid directory paths are provided
    if directory_path_1 or directory_path_2:  # At least one directory should be specified
        # Check if both directories exist
        valid_dir_1 = os.path.isdir(directory_path_1)
        valid_dir_2 = os.path.isdir(directory_path_2)

        # Get PNG files from both directories if valid
        png_files_1 = [f for f in os.listdir(directory_path_1) if f.endswith('.png')] if valid_dir_1 else []
        png_files_2 = [f for f in os.listdir(directory_path_2) if f.endswith('.png')] if valid_dir_2 else []

        # Display PNG files if they exist in any directory
        if png_files_1 or png_files_2:
            st.title("PNG File Gallery")

            # If both directories are valid, display images in two columns (side-by-side)
            if valid_dir_1 and valid_dir_2:
                for i in range(0, max(len(png_files_1), len(png_files_2)), num_columns):
                    cols = st.columns(2)  # Create two columns for side-by-side display

                    # Display images from directory 1 in the left column
                    for j in range(min(num_columns, len(png_files_1) - i)):
                        file_name_1 = png_files_1[i + j]
                        file_path_1 = os.path.join(directory_path_1, file_name_1)
                        image_1 = Image.open(file_path_1)
                        with cols[0]:
                            # Center-align the image in the left column
                            st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                            st.image(image_1, caption=file_name_1, width=image_width)
                            st.markdown("</div>", unsafe_allow_html=True)

                    # Display images from directory 2 in the right column
                    for j in range(min(num_columns, len(png_files_2) - i)):
                        file_name_2 = png_files_2[i + j]
                        file_path_2 = os.path.join(directory_path_2, file_name_2)
                        image_2 = Image.open(file_path_2)
                        with cols[1]:
                            # Center-align the image in the right column
                            st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                            st.image(image_2, caption=file_name_2, width=image_width)
                            st.markdown("</div>", unsafe_allow_html=True)

            # If only one directory is valid, display its images in multiple columns
            elif valid_dir_1:
                st.write("Displaying images from Directory 1")
                for i in range(0, len(png_files_1), num_columns):
                    cols = st.columns(num_columns)  # Create specified number of columns
                    for j in range(num_columns):
                        if i + j < len(png_files_1):  # Check index range
                            file_name_1 = png_files_1[i + j]
                            file_path_1 = os.path.join(directory_path_1, file_name_1)
                            image_1 = Image.open(file_path_1)
                            with cols[j]:
                                # Center-align the image in each column
                                st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                                st.image(image_1, caption=file_name_1, width=image_width)
                                st.markdown("</div>", unsafe_allow_html=True)

            elif valid_dir_2:
                st.write("Displaying images from Directory 2")
                for i in range(0, len(png_files_2), num_columns):
                    cols = st.columns(num_columns)  # Create specified number of columns
                    for j in range(num_columns):
                        if i + j < len(png_files_2):  # Check index range
                            file_name_2 = png_files_2[i + j]
                            file_path_2 = os.path.join(directory_path_2, file_name_2)
                            image_2 = Image.open(file_path_2)
                            with cols[j]:
                                # Center-align the image in each column
                                st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                                st.image(image_2, caption=file_name_2, width=image_width)
                                st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.warning("No PNG files found in the specified directories.")

        # If no directories are valid
        if not valid_dir_1 and not valid_dir_2:
            st.error("Both directory paths are invalid.")
    else:
        st.info("Please specify at least one directory.")
