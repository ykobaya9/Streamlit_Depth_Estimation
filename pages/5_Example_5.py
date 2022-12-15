import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
from streamlit_extras.switch_page_button import switch_page


Index = 4
st.markdown(f'### Example {Index+1}')


if 'session_code' not in st.session_state:
    session_code = st.write('Missing session code. Please return to instructions and enter it.')
else:
    _, row1_1, _, row1_2, _, row1_3, _, row1_4 = st.columns(
        (0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1)
    )
    with row1_1:

        st.markdown("<h5 style='text-align: center; color: black;'>Input Image</h1>", unsafe_allow_html=True)
        input_image = Image.open(os.path.join('Images',st.session_state['example_images'][Index]+'.png'))
        st.image(input_image)

    with row1_2:
        st.markdown("<h5 style='text-align: center; color: black;'>Predicted Depth</h1>", unsafe_allow_html=True)
        predicted_depth = Image.open(os.path.join('Predictions',st.session_state['example_images'][Index]+'.jpeg')).convert('RGB')
        st.image(predicted_depth)

    with row1_3:
        st.markdown("<h5 style='text-align: center; color: black;'>GT</h1>", unsafe_allow_html=True)
        gt_depth = Image.open(os.path.join('Depths',st.session_state['example_images'][Index]+'_disp.jpeg')).convert('RGB')
        st.image(gt_depth)

    with row1_4:
        st.markdown("<h5 style='text-align: center; color: black;'>Error</h1>", unsafe_allow_html=True)
        error = Image.open(os.path.join('errors',st.session_state['example_images'][Index]+'_disp_depth.jpg')).convert('RGB')
        st.image(error)

    if st.session_state['assigned_interpretable'] == '1':
        st.write('\n\n\n\n\n\n\n\n\n')
        st.markdown('###### Below are some filtered versions of the original input image you may find helpful.')
        _, row2_1, _, row2_2, _, row2_3, _, row2_4 = st.columns((0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1))
        with row2_1:
            st.markdown("<h5 style='text-align: center; color: black;'>Edges</h1>", unsafe_allow_html=True)
            edge_image = Image.open(os.path.join('canny',st.session_state['example_images'][Index]+'_canny.jpg'))
            st.image(edge_image)
        with row2_2:
            st.markdown("<h5 style='text-align: center; color: black;'>Contours</h1>", unsafe_allow_html=True)
            bin_image = Image.open(os.path.join('contour',st.session_state['example_images'][Index]+'_contour.jpg'))
            st.image(bin_image)
        with row2_3:
            st.markdown("<h5 style='text-align: center; color: black;'>Texture</h1>", unsafe_allow_html=True)
            hp_image = Image.open(os.path.join('HP',st.session_state['example_images'][Index]+'_highpass.jpg'))
            st.image(hp_image)
        with row2_4:
            st.markdown("<h5 style='text-align: center; color: black;'>Blurred</h1>", unsafe_allow_html=True)
            hp_image = Image.open(os.path.join('blur',st.session_state['example_images'][Index]+'_blur.jpg'))
            st.image(hp_image)


prev_name,next_name = f'example {Index+1-1}', f'question 1'

back, _, next = st.columns((.1,1,.1))

with back:
    last_page = st.button("Previous",key="prev",type="primary")
    if last_page:
        switch_page(prev_name)

with next:
    with next:
        next_page = st.button("Next Page",key="next",type="primary")
        if next_page:
            switch_page(next_name)
