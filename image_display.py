import streamlit as st
import os
import pyautogui
import time
from datetime import datetime
from PIL import Image
from io import BytesIO


def take_screenshot(left, top, right, bottom):
    # Take a screenshot of the specified region
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = f"screenshot_{timestamp}.png"

    # Save the screenshot
    screenshot.save(save_path)

    # Convert the screenshot to binary format
    img_byte_arr = BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # Reset pointer to the beginning

    return img_byte_arr, save_path


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

    # Inject custom CSS to set the width of the sidebar
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 300px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True,
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
    directory_paths = []
    for i in range(0, 5):
        path = st.sidebar.text_input(f"Enter {i+1}st directory path", key=f"directory_path_{i+1}")
        directory_paths.append(path)

    # Image width and number of columns settings
    options = ["mode1", "mode2"]
    sort_option = st.sidebar.radio("Sorting Mode", options)
    selected_sort_option_index = options.index(sort_option)
    num_columns = st.sidebar.slider("Number of Columns", min_value=1, max_value=10, value=2, step=1)

    # Reload button to refresh the images
    if st.sidebar.button("Reload"):
        st.session_state["reload"] = not st.session_state["reload"]  # Toggle reload flag

    # Sidebar inputs for coordinates
    st.sidebar.header("Enter the coordinates of the area to capture")
    left = st.sidebar.number_input("Left X-coordinate", min_value=0, value=300)
    top = st.sidebar.number_input("Top Y-coordinate", min_value=0, value=200)
    right = st.sidebar.number_input("Right X-coordinate", min_value=left + 1, value=1800)
    bottom = st.sidebar.number_input("Bottom Y-coordinate", min_value=top + 1, value=1000)

    # Warning if right or bottom coordinates are smaller than left or top
    if right <= left or bottom <= top:
        st.sidebar.warning("The right and bottom coordinates must be greater than the left and top coordinates.")

    # Button to take the screenshot when clicked
    if st.sidebar.button("Capture Screenshot"):
        st.write("Preparing to capture the screenshot... Starting in 5 seconds...")

        # Wait for 5 seconds before capturing
        time.sleep(5)

        # Take the screenshot
        img_byte_arr, save_path = take_screenshot(left, top, right, bottom)

        # Display the captured screenshot
        st.image(img_byte_arr, caption=f"Saved image: {save_path}", use_container_width=True)

    # Display images if valid directory paths are provided
    if any(directory_paths):

        # Check if both directories exist
        valid_dirs = []
        for i in range(0, 5):
            valid_dir = os.path.isdir(directory_paths[i])
            valid_dirs.append(valid_dir)

        # Get PNG files from both directories if valid
        png_files = []
        for i in range(0, 5):
            png_file = [f for f in os.listdir(directory_paths[i]) if f.endswith('.png')] if valid_dirs[i] else []
            png_file.sort()
            png_files.append(png_file)

        total_images = 0
        for i in range(0, 5):
            total_images += len(png_files[i])
        progress_bar = st.progress(0)  # Initialize progress bar
        progress_count = RefNumber(0)  # Track the current progress

        # Display PNG files if they exist in any directory
        if any(png_files):
            st.title("PNG File Gallery")

            # If both directories are valid, display images in two columns (side-by-side)
            if all(valid_dirs[0:2]) and not any(valid_dirs[2:5]):
                for i in range(0, max(len(png_files[0]), len(png_files[1])), num_columns):
                    cols = st.columns(num_columns*2)  # Create two columns for side-by-side display
                    left, right = generate_series(max(len(png_files[0]), len(png_files[1])), num_columns, selected_sort_option_index)
                    put_image2(png_files[0], directory_paths[0], num_columns, i, cols, left, progress_count)
                    progress_bar.progress(progress_count.value/total_images)
                    put_image2(png_files[1], directory_paths[1], num_columns, i, cols, right, progress_count)
                    progress_bar.progress(progress_count.value/total_images)

            elif all(valid_dirs[0:3]) and not any(valid_dirs[3:5]):
                num_columns = 3
                for i in range(0, max(len(png_files[0]), len(png_files[1]), len(png_files[2])), num_columns):
                    cols = st.columns(num_columns)  # Create three columns
                    for k in range(num_columns):
                        put_image2(png_files[k], directory_paths[k], num_columns, i, cols, [k]*len(png_files[k])*num_columns, progress_count)
                        progress_bar.progress(progress_count.value/total_images)

            elif all(valid_dirs[0:4]) and not any(valid_dirs[4:6]):
                num_columns = 4
                for i in range(0, max(len(png_files[0]), len(png_files[1]), len(png_files[2]), len(png_files[3])), num_columns):
                    cols = st.columns(num_columns)  # Create three columns
                    for k in range(num_columns):
                        put_image2(png_files[k], directory_paths[k], num_columns, i, cols, [k]*len(png_files[k])*num_columns, progress_count)
                        progress_bar.progress(progress_count.value/total_images)

            elif all(valid_dirs):
                num_columns = 5
                for i in range(0, max(len(png_files[0]), len(png_files[1]), len(png_files[2]), len(png_files[3]), len(png_files[4])), num_columns):
                    cols = st.columns(num_columns)  # Create three columns
                    for k in range(num_columns):
                        put_image2(png_files[k], directory_paths[k], num_columns, i, cols, [k]*len(png_files[k])*num_columns, progress_count)
                        progress_bar.progress(progress_count.value/total_images)

            # If only one directory is valid, display its images in multiple columns
            else:
                for i, is_valid in enumerate(valid_dirs):
                    if is_valid:
                        put_image(i + 1, png_files[i], directory_paths[i], num_columns, progress_count)
                        progress_bar.progress(progress_count.value / total_images)
                        break

        else:
            st.warning("No PNG files found in the specified directories.")

        # If no directories are valid
        if not any(valid_dirs):
            st.error("All directory paths are invalid.")
    else:
        st.info("Please specify at least one directory.")


if __name__ == '__main__':
    image_display()
