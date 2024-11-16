import streamlit as st
import os
from PIL import Image


def pic_display():
    st.set_page_config(
        layout="wide"
    )

    # init session state
    if "directory_path" not in st.session_state:
        st.session_state["directory_path"] = ""

    st.sidebar.write("Specify Directory")

    directory_path = st.sidebar.text_input("Input Dir Path", key="directory_path")

    # auto reload
    image_width = st.sidebar.slider("Pic Width (px)", min_value=50, max_value=400, value=150, step=10)
    num_columns = st.sidebar.slider("Number of Columns", min_value=1, max_value=5, value=2, step=1)

    # display png files if directory_path is specified
    if directory_path:
        # directory check
        if os.path.isdir(directory_path):
            # get png files
            png_files = [f for f in os.listdir(directory_path) if f.endswith('.png')]

            # if png file exists, display
            if png_files:
                st.title("PNG Files Display")

                # 指定された数だけ横に並べて表示
                for i in range(0, len(png_files), num_columns):
                    cols = st.columns(num_columns)
                    for j in range(num_columns):
                        if i + j < len(png_files):
                            file_name = png_files[i + j]
                            file_path = os.path.join(directory_path, file_name)
                            image = Image.open(file_path)

                            with cols[j]:
                                st.image(image, caption=file_name, width=image_width)
            else:
                st.warning("No PNG files found in the specified directory.")
        else:
            st.error("Invalid directory path.")
    else:
        st.info("Please specify a directory")
