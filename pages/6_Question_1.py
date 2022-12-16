import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import time
from streamlit_extras.switch_page_button import switch_page


Index = 0

st.markdown(f'### Question {Index + 1}')
st.markdown("Please look through the two sample images and select the one you think is most likely to have the higher error in the highlighted region.")
if 'session_code' not in st.session_state:
    session_code = st.write('Missing session code. Please return to instructions and enter it.')
else:
    if f'Question_Answer_{Index}' in st.session_state:
        st.markdown(f'#### Sample A')
        _, row1_1, _, row1_2, _ = st.columns((0.1, 1, 0.1, 1, 0.1))
        with row1_1:
            st.markdown("<h5 style='text-align: center; color: black;'>Sample A Input Image</h1>", unsafe_allow_html=True)
            input_image = Image.open(os.path.join('Superpixel_Input',st.session_state['question_images'][2*Index]+'_super.jpg'))
            st.image(input_image)
        with row1_2:
            st.markdown("<h5 style='text-align: center; color: black;'>Sample A Predicted Depth</h1>", unsafe_allow_html=True)
            predicted_depth = Image.open(os.path.join('Superpixel_Pred',st.session_state['question_images'][2*Index]+'_super.jpg')).convert('RGB')
            st.image(predicted_depth)
        if st.session_state['assigned_interpretable'] == '1':
            _, row1_2_1, row1_2_2, row1_2_3, row1_2_4, row1_2_5, _ = st.columns((0.1, 1, 1, 1, 1, 1, 1))
            with row1_2_1:
                st.markdown("<h5 style='text-align: center; color: black;'>Edges</h5>", unsafe_allow_html=True)
                edge_image = Image.open(os.path.join('canny',st.session_state['question_images'][2*Index]+'_canny.jpg'))
                st.image(edge_image)
            with row1_2_2:
                st.markdown("<h5 style='text-align: center; color: black;'>Contours</h5>", unsafe_allow_html=True)
                bin_image = Image.open(os.path.join('contour',st.session_state['question_images'][2*Index]+'_contour.jpg'))
                st.image(bin_image)
            with row1_2_3:
                st.markdown("<h5 style='text-align: center; color: black;'>Texture</h5>", unsafe_allow_html=True)
                hp_image = Image.open(os.path.join('HP',st.session_state['question_images'][2*Index]+'_highpass.jpg'))
                st.image(hp_image)
            with row1_2_4:
                st.markdown("<h5 style='text-align: center; color: black;'>Blurred</h5>", unsafe_allow_html=True)
                blur_image = Image.open(os.path.join('blur',st.session_state['question_images'][2*Index]+'_blur.jpg'))
                st.image(blur_image)
            with row1_2_5:
                st.markdown("<h5 style='text-align: center; color: black;'>Features Contributing to Error</h5>", unsafe_allow_html=True)
                shap = Image.open(os.path.join('SHAP',st.session_state['question_images'][2*Index]+'_shap.png'))
                st.image(shap)
            
      
        st.markdown("---")

        st.markdown(f'#### Sample B')
        _, row2_1, _, row2_2, _ = st.columns((0.1, 1, 0.1, 1, 0.1))
        with row2_1:
            st.markdown("<h5 style='text-align: center; color: black;'>Sample B Input Image</h1>", unsafe_allow_html=True)
            input_image = Image.open(os.path.join('Superpixel_Input',st.session_state['question_images'][(2*Index)+1]+'_super.jpg'))
            st.image(input_image)
        with row2_2:
            st.markdown("<h5 style='text-align: center; color: black;'>Sample B Predicted Depth</h1>", unsafe_allow_html=True)
            predicted_depth = Image.open(os.path.join('Superpixel_Pred',st.session_state['question_images'][(2*Index)+1]+'_super.jpg')).convert('RGB')
            st.image(predicted_depth)
        if st.session_state['assigned_interpretable'] == '1':
            _, row2_2_1, row2_2_2, row2_2_3, row2_2_4, row2_2_5, _ = st.columns((0.1, 1, 1, 1, 1, 1, 1))
            with row2_2_1:
                st.markdown("<h5 style='text-align: center; color: black;'>Edges</h5>", unsafe_allow_html=True)
                edge_image = Image.open(os.path.join('canny',st.session_state['question_images'][2*Index+1]+'_canny.jpg'))
                st.image(edge_image)
            with row2_2_2:
                st.markdown("<h5 style='text-align: center; color: black;'>Contours</h5>", unsafe_allow_html=True)
                bin_image = Image.open(os.path.join('contour',st.session_state['question_images'][2*Index+1]+'_contour.jpg'))
                st.image(bin_image)
            with row2_2_3:
                st.markdown("<h5 style='text-align: center; color: black;'>Texture</h5>", unsafe_allow_html=True)
                hp_image = Image.open(os.path.join('HP',st.session_state['question_images'][2*Index+1]+'_highpass.jpg'))
                st.image(hp_image)
            with row2_2_4:
                st.markdown("<h5 style='text-align: center; color: black;'>Blurred</h5>", unsafe_allow_html=True)
                blur_image = Image.open(os.path.join('blur',st.session_state['question_images'][2*Index+1]+'_blur.jpg'))
                st.image(blur_image)
            with row2_2_5:
                st.markdown("<h5 style='text-align: center; color: black;'>Features Contributing to Error</h5>", unsafe_allow_html=True)
                shap = Image.open(os.path.join('SHAP',st.session_state['question_images'][2*Index+1]+'_shap.png'))
                st.image(shap)
        st.markdown("Answer already submitted, thank you!")
    else:
        with st.form(key='highest_err'):
            st.markdown(f'#### Sample A')
            _, row1_1, _, row1_2, _ = st.columns((0.1, 1, 0.1, 1, 0.1))
            with row1_1:
                st.markdown("<h5 style='text-align: center; color: black;'>Sample A Input Image</h1>", unsafe_allow_html=True)
                input_image = Image.open(os.path.join('Superpixel_Input',st.session_state['question_images'][2*Index]+'_super.jpg'))
                st.image(input_image)
            with row1_2:
                st.markdown("<h5 style='text-align: center; color: black;'>Sample A Predicted Depth</h1>", unsafe_allow_html=True)
                predicted_depth = Image.open(os.path.join('Superpixel_Pred',st.session_state['question_images'][2*Index]+'_super.jpg')).convert('RGB')
                st.image(predicted_depth)
            if st.session_state['assigned_interpretable'] == '1':
                _, row1_2_1, row1_2_2, row1_2_3, row1_2_4, row1_2_5, _ = st.columns((0.1, 1, 1, 1, 1, 1, 1))
                with row1_2_1:
                    st.markdown("<h5 style='text-align: center; color: black;'>Edges</h5>", unsafe_allow_html=True)
                    edge_image = Image.open(os.path.join('canny',st.session_state['question_images'][2*Index]+'_canny.jpg'))
                    st.image(edge_image)
                with row1_2_2:
                    st.markdown("<h5 style='text-align: center; color: black;'>Contours</h5>", unsafe_allow_html=True)
                    bin_image = Image.open(os.path.join('contour',st.session_state['question_images'][2*Index]+'_contour.jpg'))
                    st.image(bin_image)
                with row1_2_3:
                    st.markdown("<h5 style='text-align: center; color: black;'>Texture</h5>", unsafe_allow_html=True)
                    hp_image = Image.open(os.path.join('HP',st.session_state['question_images'][2*Index]+'_highpass.jpg'))
                    st.image(hp_image)
                with row1_2_4:
                    st.markdown("<h5 style='text-align: center; color: black;'>Blurred</h5>", unsafe_allow_html=True)
                    blur_image = Image.open(os.path.join('blur',st.session_state['question_images'][2*Index]+'_blur.jpg'))
                    st.image(blur_image) 
                with row1_2_5:
                    st.markdown("<h5 style='text-align: center; color: black;'>Features Contributing to Error</h5>", unsafe_allow_html=True)
                    shap = Image.open(os.path.join('SHAP',st.session_state['question_images'][2*Index]+'_shap.png'))
                    st.image(shap)
            st.markdown("---")

            st.markdown(f'#### Sample B')
            _, row2_1, _, row2_2, _ = st.columns((0.1, 1, 0.1, 1, 0.1))
            with row2_1:
                st.markdown("<h5 style='text-align: center; color: black;'>Sample B Input Image</h1>", unsafe_allow_html=True)
                input_image = Image.open(os.path.join('Superpixel_Input',st.session_state['question_images'][(2*Index)+1]+'_super.jpg'))
                st.image(input_image)
            with row2_2:
                st.markdown("<h5 style='text-align: center; color: black;'>Sample B Predicted Depth</h1>", unsafe_allow_html=True)
                predicted_depth = Image.open(os.path.join('Superpixel_Pred',st.session_state['question_images'][(2*Index)+1]+'_super.jpg')).convert('RGB')
                st.image(predicted_depth)
            if st.session_state['assigned_interpretable'] == '1':
                _, row2_2_1, row2_2_2, row2_2_3, row2_2_4, row2_2_5, _ = st.columns((0.1, 1, 1, 1, 1, 1, 1))
                with row2_2_1:
                    st.markdown("<h5 style='text-align: center; color: black;'>Edges</h5>", unsafe_allow_html=True)
                    edge_image = Image.open(os.path.join('canny',st.session_state['question_images'][2*Index+1]+'_canny.jpg'))
                    st.image(edge_image)
                with row2_2_2:
                    st.markdown("<h5 style='text-align: center; color: black;'>Contours</h5>", unsafe_allow_html=True)
                    bin_image = Image.open(os.path.join('contour',st.session_state['question_images'][2*Index+1]+'_contour.jpg'))
                    st.image(bin_image)
                with row2_2_3:
                    st.markdown("<h5 style='text-align: center; color: black;'>Texture</h5>", unsafe_allow_html=True)
                    hp_image = Image.open(os.path.join('HP',st.session_state['question_images'][2*Index+1]+'_highpass.jpg'))
                    st.image(hp_image)
                with row2_2_4:
                    st.markdown("<h5 style='text-align: center; color: black;'>Blurred</h5>", unsafe_allow_html=True)
                    blur_image = Image.open(os.path.join('blur',st.session_state['question_images'][2*Index+1]+'_blur.jpg'))
                    st.image(blur_image)
                with row2_2_5:
                    st.markdown("<h5 style='text-align: center; color: black;'>Features Contributing to Error</h5>", unsafe_allow_html=True)
                    shap = Image.open(os.path.join('SHAP',st.session_state['question_images'][2*Index+1]+'_shap.png'))
                    st.image(shap)

            options = ["Sample A", "Sample B"]
            select_text = "Which sample do you think will have the highest error within the highlighted region?"
            
            
            
            highest_error_sample = st.selectbox(select_text,options=options)
            submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                st.session_state[f'Question_Answer_{Index}'] = highest_error_sample 
                switch_page(f'question {Index+1+1}')



prev_name,next_name = 'example 5', f'question {Index + 1 + 1}'

back, _, next = st.columns((.1,1,.1))

with back:
    last_page = st.button("Previous",key="prev",type="primary")
    if last_page:
        switch_page(prev_name)

if f'Question_Answer_{Index}' in st.session_state:
    with next:
        next_page = st.button("Next Page",key="next",type="primary")
        if next_page:
            switch_page(next_name)


   

