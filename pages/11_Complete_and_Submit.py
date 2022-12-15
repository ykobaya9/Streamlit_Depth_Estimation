import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import json
from streamlit_extras.switch_page_button import switch_page

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]


#creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(st.secrets['key_json']),scope)
#creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
)

client = gspread.authorize(creds)

worksheet = client.open("Interpretable_Depth_Estimation_Data").get_worksheet(0)


st.markdown(f'### Complete and Submit')

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:regular;padding-left:2px;}</style>', unsafe_allow_html=True)

if 'session_code' not in st.session_state:
    session_code = st.write('Missing session code. Please return to instructions and enter it.')
else:
    with st.form("Exit Survey"):
        usability = st.radio("2. Outside of the task, how would you rate the study's UI?",("Very difficult to use","Difficult to use","Average","Easy to use","Very easy to use"),index=2)
        model_confidence = st.radio("1. How confident would you be in the model's predictions?",("Very Unconfident","Unconfident","Average","Confident","Very Confident"),index=2)
        task_confidence = st.radio("3. How confident were you in your ability to complete the task?",("Very Unconfident","Unconfident","Average","Confident","Very Confident"),index=2)
        experience = st.radio("4. How experienced would you say you are with machine learning in general?",("No experience","Relatively experienced","Average","Very experienced","Expert"),index=2)
        
        submitted = st.form_submit_button("Submit and upload all study answers",type="primary",help="Clicking this button finalizes all answers and uploads them.")
        if submitted:
            found_user_cell = worksheet.find(st.session_state['session_code'])
            if found_user_cell is None:
                st.write("Write to google drive failed. Please contact us.")
            else:
                row = found_user_cell.row
                complete = True
                for question_index in range(5):
                    if f'Question_Answer_{question_index}' not in st.session_state:
                        st.write(f"Question {question_index+1} not completed. Please complete it and submit again.")
                        complete = False
                    else:
                        worksheet.update_cell(row,question_index+5,st.session_state[f'Question_Answer_{question_index}'])
                worksheet.update_cell(row,10,usability)
                worksheet.update_cell(row,11,model_confidence)
                worksheet.update_cell(row,12,task_confidence)
                worksheet.update_cell(row,13,experience)
                if complete:
                    st.write("Submission successful, thank you for your time!")

prev_name = f'question 5'

back, _, next = st.columns((.1,1,.1))

with back:
    last_page = st.button("Previous",key="prev",type="primary")
    if last_page:
        switch_page(prev_name)
