# streamlit_app.py

# Importing Libraries
import streamlit as st
import altair as alt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from st_files_connection import FilesConnection
from datetime import datetime

# ----------------------- Accessing Data -------------------------

# Accessing the data stored in a Google Cloud Platform Bucket 
@st.cache_data
def get_data():
    conn = st.connection('gcs', type=FilesConnection)
    data = conn.read("stepscount_dashboard/stepcount_data_2023.csv", ttl=600)
    return data

# Assign the data to a dataframe
df = get_data()

# ----------------------- Main Page ----------------------------

# Row 1 - Contains metrics such as  "Total Steps Walked", "Total Hours Walked", "Steps to Hours Ratio"
total_steps = df['StepCount'].sum() # Total Steps Walked
total_hours = df['DurationHours'].sum() # Total Hours Walked
st.markdown('### Year 2023 in glance')
col1, col2, col3 = st.columns(3)

# Card for Total Steps Walked
col1.markdown( 
    f'<div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center;">'
    f'<h3 style="margin-bottom: 0;">Total Steps Walked 👣</h3>'
    f'<p style="font-size: 24px; font-weight: bold; color: #4CAF50;">{round(total_steps):,.0f} steps</p>'
    f'</div>',
    unsafe_allow_html=True
    )

# Card for Total Hours Walked
col2.markdown(
    f'<div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center;">'
    f'<h3 style="margin-bottom: 0;">Total Hours Walked ⌛</h3>'
    f'<p style="font-size: 24px; font-weight: bold; color: #01796F;">{round(total_hours):,.0f} hrs</p>'
    f'</div>',
    unsafe_allow_html=True
)

# Card for Steps Walked per Hour
col3.markdown(
    f'<div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center;">'
    f'<h3 style="margin-bottom: 0;"> Steps Walked per Hour </h3>'
    f'<p style="font-size: 24px; font-weight: bold; color: #8A9A5B;">{round(total_steps/total_hours):,.0f} steps/hr</p>'
    f'</div>',
    unsafe_allow_html=True
)







# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)













