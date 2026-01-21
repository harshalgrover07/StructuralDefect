import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# Configure the model 
gemini_api_key = os.getenv('GOOGLE_API_KEY1')
genai.configure(api_key=gemini_api_key)
model= genai.GenerativeModel('gemini-2.5-flash')

# Lets create sidebar for image upload
st.sidebar.title(''':red[Upload the Image's of Here:]''')
uploaded_image = st.sidebar.file_uploader('Image',type=['jpeg','jpg','png','jfif'],accept_multiple_files=True)

uploaded_image = [Image.open(img) for img in uploaded_image]

if uploaded_image:
    st.sidebar.success('Image has been loaded succesfully')
    st.sidebar.subheader(':blue[Uploaded Image]')
    st.sidebar.image(uploaded_image)

# Lets Create a Main page

st.title(':red[SafeFrame AI:-] :blue[Intelligent Structural Defect Detection Using AI]')
st.markdown('#### :green[This Application takes the images of the structural defect from the construction site and prepare the AI Assisted report.]')
title = st.text_input('Enter the Title of the report')
name = st.text_input('Enter the name of the person who has prepared the report')
desig = st. text_input('Enter the designation of the person who has created the report')
orgz = st.text_input('Enter the name of the organization')

if st.button('SUBMIT'):
    with st.spinner('Processing....'):
        prompt = f'''
            <Role> You are an Expert in Structural Engineer with 20+ experience.
            <Goal> You need to prepare a detailed report on structural defect. show the images provided by the user.
            <Context> The images by the user has been attached.
            <Format> Follow the steps to prepare the report
                * Add title at the top of the report. The title provided by the user is {title}.
                * next add name ,designation and organization of the person who has prepared the report. Also include the date.Following are the details 
                provided by the user
                    name : {name}
                    designation : {desig}
                    organisation : {orgz}
                    date : {dt.datetime.now().date()}
                * Identify and classify the defect for eg. crack, spalling,corossion,honey combining
                * There could be more than one defects in images. Identify all defects separately
                * For each defect highlighted or identified provide a short description of the defects and its potential imapact on the structure
                * For each defect measure the severity as low, medium, or high. Also Mention if the defect is inevitable or avoidable
                * Provide the short term and long term solution for the repair along with an estimated cost in INR along with the estimated time
                * What precautionary measure can be taken to avoid these measures in the future. 

            <Instructions>
            * Don not use any HTML formats like br .
            * The report generated should be in text form.
            * Use bullet points and tabular form where ever possible.
            * Make sure the report does not exceed 3 pages.
            * Make the report look attractive.
            '''
        
        response = model.generate_content([prompt,*uploaded_image],
                                          generation_config={'temperature':0.9})
        

        st.write(response.text)


    if st.download_button(
        label='Click To Download',
        data=response.text,
        file_name='structural_defect_report.txt',
        mime= 'text/plain'
        ):
        st.success('Your file is downloaded')