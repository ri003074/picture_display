import streamlit as st
import os
from PIL import Image


class RefNumber:
    def __init__(self, value):
        self.value = value

    def add(self, amount):
        self.value += amount


def generate_series(n, col, mode=1):
    base_right = []
    base_left = []
    if mode == 0:
        for i in range(col):
            base_right.append(i)
            base_left.append(i+col)
        return base_right*2*n, base_left*2*n

    elif mode == 1:
        arr = [i for i in range(n*2)]
        for i, val in enumerate(arr):
            if i % 2:
                base_left.append(val)
            else:
                base_right.append(val)
        return base_right, base_left


def put_image(num, png_files, directory_path, num_columns, progress_count):
    st.write("Displaying images from Directory " + str(num))
    for i in range(0, len(png_files), num_columns):
        cols = st.columns(num_columns)  # Create specified number of columns
        for j in range(num_columns):
            if i + j < len(png_files):  # Check index range
                file_name = png_files[i + j]
                file_path = os.path.join(directory_path, file_name)
                image = Image.open(file_path)
                with cols[j]:
                    # Center-align the image in each column
                    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                    st.image(image, caption=file_name, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    progress_count.add(1)


def put_image2(png_files, directory_path, num_columns, index, cols, position, progress_count):
    for j in range(min(num_columns, len(png_files) - index)):
        file_name = png_files[index + j]
        file_path = os.path.join(directory_path, file_name)
        image = Image.open(file_path)
        with cols[position[j]]:
            st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
            st.image(image, caption=file_name, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            progress_count.add(1)


def image_display():
    st.set_page_config(
        page_title="Image Display",  # Page title
        layout="wide"  # Set layout to "wide"
    )

    # Initialize session state for directory paths and reload flag
    if "directory_path_1" not in st.session_state:
        st.session_state["directory_path_1"] = os.getcwd()
    if "directory_path_2" not in st.session_state:
        st.session_state["directory_path_2"] = ""
    if "directory_path_3" not in st.session_state:
        st.session_state["directory_path_3"] = ""
    if "directory_path_4" not in st.session_state:
        st.session_state["directory_path_4"] = ""
    if "directory_path_5" not in st.session_state:
        st.session_state["directory_path_5"] = ""
    if "reload" not in st.session_state:
        st.session_state["reload"] = False
    if "prev_image_width" not in st.session_state:
        st.session_state["prev_image_width"] = 150

    # Sidebar instructions
    st.sidebar.write("Please specify two directories containing PNG files.")

    # Directory path input fields
    directory_path_1 = st.sidebar.text_input("Enter 1st directory path", key="directory_path_1")
    directory_path_2 = st.sidebar.text_input("Enter 2nd directory path", key="directory_path_2")
    directory_path_3 = st.sidebar.text_input("Enter 3rd directory path", key="directory_path_3")
    directory_path_4 = st.sidebar.text_input("Enter 4th directory path", key="directory_path_4")
    directory_path_5 = st.sidebar.text_input("Enter 5th directory path", key="directory_path_5")

    # Image width and number of columns settings
    options = ["mode1", "mode2"]
    sort_option = st.sidebar.radio("Sorting Mode", options)
    selected_sort_option_index = options.index(sort_option)
    num_columns = st.sidebar.slider("Number of Columns", min_value=1, max_value=10, value=2, step=1)

    # Reload button to refresh the images
    if st.sidebar.button("Reload"):
        st.session_state["reload"] = not st.session_state["reload"]  # Toggle reload flag

    # Display images if valid directory paths are provided
    if directory_path_1 or directory_path_2 or directory_path_3 or directory_path_4 or directory_path_5:

        # Check if both directories exist
        valid_dir_1 = os.path.isdir(directory_path_1)
        valid_dir_2 = os.path.isdir(directory_path_2)
        valid_dir_3 = os.path.isdir(directory_path_3)
        valid_dir_4 = os.path.isdir(directory_path_4)
        valid_dir_5 = os.path.isdir(directory_path_5)

        # Get PNG files from both directories if valid
        png_files_1 = [f for f in os.listdir(directory_path_1) if f.endswith('.png')] if valid_dir_1 else []
        png_files_2 = [f for f in os.listdir(directory_path_2) if f.endswith('.png')] if valid_dir_2 else []
        png_files_3 = [f for f in os.listdir(directory_path_3) if f.endswith('.png')] if valid_dir_3 else []
        png_files_4 = [f for f in os.listdir(directory_path_4) if f.endswith('.png')] if valid_dir_4 else []
        png_files_5 = [f for f in os.listdir(directory_path_5) if f.endswith('.png')] if valid_dir_5 else []

        total_images = len(png_files_1) + len(png_files_2) + len(png_files_3) + len(png_files_4) + len(png_files_5)
        progress_bar = st.progress(0)  # Initialize progress bar
        progress_count = RefNumber(0)  # Track the current progress

        # Display PNG files if they exist in any directory
        if png_files_1 or png_files_2 or png_files_3 or png_files_4 or png_files_5:
            st.title("PNG File Gallery")

            # If both directories are valid, display images in two columns (side-by-side)
            if valid_dir_1 and valid_dir_2 and not valid_dir_3 and not valid_dir_4 and not valid_dir_5:
                for i in range(0, max(len(png_files_1), len(png_files_2)), num_columns):
                    cols = st.columns(num_columns*2)  # Create two columns for side-by-side display
                    left, right = generate_series(max(len(png_files_1), len(png_files_2)), num_columns, selected_sort_option_index)
                    put_image2(png_files_1, directory_path_1, num_columns, i, cols, left, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_2, directory_path_2, num_columns, i, cols, right, progress_count)
                    progress_bar.progress(progress_count.value/total_images)

            elif valid_dir_1 and valid_dir_2 and valid_dir_3 and not valid_dir_4 and not valid_dir_5:
                num_columns = 3
                for i in range(0, max(len(png_files_1), len(png_files_2), len(png_files_3)), num_columns):
                    cols = st.columns(num_columns)  # Create three columns
                    put_image2(png_files_1, directory_path_1, num_columns, i, cols, [0]*len(png_files_1)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_2, directory_path_2, num_columns, i, cols, [1]*len(png_files_2)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_3, directory_path_3, num_columns, i, cols, [2]*len(png_files_3)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)

            elif valid_dir_1 and valid_dir_2 and valid_dir_3 and valid_dir_4 and not valid_dir_5:
                num_columns = 4
                for i in range(0, max(len(png_files_1), len(png_files_2), len(png_files_3), len(png_files_4)), num_columns):
                    cols = st.columns(num_columns)  # Create three columns
                    put_image2(png_files_1, directory_path_1, num_columns, i, cols, [0]*len(png_files_1)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_2, directory_path_2, num_columns, i, cols, [1]*len(png_files_2)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_3, directory_path_3, num_columns, i, cols, [2]*len(png_files_3)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_4, directory_path_4, num_columns, i, cols, [3]*len(png_files_4)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)

            elif valid_dir_1 and valid_dir_2 and valid_dir_3 and valid_dir_4 and valid_dir_5:
                num_columns = 5
                for i in range(0, max(len(png_files_1), len(png_files_2), len(png_files_3), len(png_files_4), len(png_files_5)), num_columns):
                    cols = st.columns(num_columns)  # Create three columns
                    put_image2(png_files_1, directory_path_1, num_columns, i, cols, [0]*len(png_files_1)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_2, directory_path_2, num_columns, i, cols, [1]*len(png_files_2)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_3, directory_path_3, num_columns, i, cols, [2]*len(png_files_3)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_4, directory_path_4, num_columns, i, cols, [3]*len(png_files_4)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files_5, directory_path_5, num_columns, i, cols, [4]*len(png_files_4)*num_columns, progress_count)
                    progress_bar.progress(progress_count.value/total_images)

            # If only one directory is valid, display its images in multiple columns
            elif valid_dir_1:
                put_image(1, png_files_1, directory_path_1, num_columns, progress_count)
                progress_bar.progress(progress_count.value / total_images)
            elif valid_dir_2:
                put_image(2, png_files_2, directory_path_2, num_columns, progress_count)
                progress_bar.progress(progress_count.value / total_images)
            elif valid_dir_3:
                put_image(3, png_files_3, directory_path_3, num_columns, progress_count)
                progress_bar.progress(progress_count.value / total_images)
            elif valid_dir_4:
                put_image(4, png_files_4, directory_path_4, num_columns, progress_count)
                progress_bar.progress(progress_count.value / total_images)
            elif valid_dir_5:
                put_image(5, png_files_5, directory_path_5, num_columns, progress_count)
                progress_bar.progress(progress_count.value / total_images)

        else:
            st.warning("No PNG files found in the specified directories.")

        # If no directories are valid
        if not valid_dir_1 and not valid_dir_2 and not valid_dir_3 and not valid_dir_4 and not valid_dir_5:
            st.error("All directory paths are invalid.")
    else:
        st.info("Please specify at least one directory.")


if __name__ == '__main__':
    image_display()
