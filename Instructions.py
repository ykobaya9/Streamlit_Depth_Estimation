
import streamlit as st
import pandas as pd
import numpy as np
import random 
import glob
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import json
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	page_title=None,  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
)

st.markdown(f'# Study Instructions')
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



def rerun():
    pass

st.markdown("""


### Welcome
Hello! Thank you for volunteering to take part in our study. It will take about 10-15 minutes to complete, \
and it should be finished in one sitting—clearing your cache or refreshing midway through will result in lost answers. \

### Informed Consent

The following paragraphs contain important background and information about the study procedure. Your participation in this  \
study is fully voluntary. Feel free to withdraw from this study at any time. Withdrawing from this study will not affect the relationship 
you have, if any, with the researcher. If you choose to withdraw prior to completing the final submission page, none of \
your responses will be retained. If you choose to withdraw afterwards for any reason, feel free to contact us for any reason \
to request your responses be removed.

Please note: We are currently testing models that predict distance in endoscopic medical procedures. This means if you choose \
 to continue you will see close up medical images, though none should be particularly gory or disturbing. If \
this could be cause of concern for you please do not continue.

### Background
A monocular depth estimation model is a computer vision model that seeks to predict how far away objects \
are based solely on a single input image. These models have potential in a variety of use cases \
ranging from augmented reality experiences to autonomous vehicles. Our goal is see how interpretable these \
models are to humans and if we can add any measures to make them more interpretable. In particular, we are \
interested in seeing how well humans can detect when these models might make errors. 



### Procedure
Our experiment is split into three parts:

##### 1. Examples

First, you will be presented with a set of randomly selected example predictions. These consist of an input \
RGB image to the model, the predicted depth the model yielded for each part of the image, the ground truth depth,
and a map showing how large the error was for each region. For this section, you do not have any questions to answer: \
your goal is solely to see how well you can understand what might cause the model to make errors. 

##### 2. Questions
After going through a number of examples, you will reach a set of questions. For this portion of the experiment you \
will be presented with two images and their corresponding predictions. Each image will have a region highlighted: your \
goal is to guess as best as you can based on the information available to you which image will have the highest error \
within their respective highlighted region.

##### 3. Exit Survey
Our final part is a short survey for you to share your thoughts on the experiment. After this you will receive instructions \
on how to download and submit your responses.

#### Get Started:
""")


if not 'session_code' in st.session_state:
    user_id = st.text_input('Please enter your 5 digit identifier and hit enter to begin the study.', on_change=rerun)  
    if len(user_id) == 5 and user_id.isdigit():
        st.session_state['session_code'] = user_id 
   
        missing_state_vals = 'assigned_interpretable' not in st.session_state or \
            'example_images' not in st.session_state or 'question_images' not in st.session_state
        if missing_state_vals:
            found_user_cell = worksheet.find(st.session_state['session_code'])
            if found_user_cell is not None:
                found_user_row = worksheet.row_values(found_user_cell.row)
                # st.write(found_user_row)
                st.session_state['assigned_interpretable'] = found_user_row[1]
                st.session_state['example_images'] = json.loads(found_user_row[2])
                st.session_state['question_images'] = json.loads(found_user_row[3])

            else:
                st.session_state['assigned_interpretable'] = str(np.random.randint(2))

                possible_images = [path.split('/')[-1][:-4] for path in glob.glob('./Images/*.png')]
                random.shuffle(possible_images)
                example_images, question_images = possible_images[:5],possible_images[5:15]
                st.session_state['example_images'] = example_images
                st.session_state['question_images'] = question_images
                worksheet.append_row([st.session_state['session_code'], 
                    st.session_state['assigned_interpretable'],
                    json.dumps(example_images),
                    json.dumps(question_images)])
            switch_page('example 1')
    elif user_id:
        st.write("Uh oh. That doesn't appear to be a valid identifier.")
else:
    next_name =  'example 1'

    _, _, next = st.columns((.1,1,.1))
    with next:
        next_page = st.button("Next",key="next",type="primary")
        if next_page:
            switch_page(next_name)
