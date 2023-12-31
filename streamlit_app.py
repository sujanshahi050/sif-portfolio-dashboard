# streamlit_app.py

# Importing Libraries
import streamlit as st
import altair as alt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from st_files_connection import FilesConnection
from datetime import datetime

# ---------------------------------------------- Accessing Data -----------------------------

# Accessing the data stored in a Google Cloud Platform Bucket 
@st.cache_data
def get_data():
    conn = st.connection('gcs', type=FilesConnection)
    data = conn.read("stepscount_dashboard/stepcount_data_2023.csv", ttl=600)
    return data

# Assign the data to a dataframe
df = get_data()

# ------------------------------------------- Important Calculations ------------------------
total_steps = df['StepCount'].sum() # Total Steps Walked
total_hours = df['DurationHours'].sum() # Total Hours Walked
monthly_total_steps = df.groupby('Month')['StepCount'].sum().reset_index() # Monthly Total Steps
top_3_months = monthly_total_steps.nlargest(3, 'StepCount') # Top 3 months
# Convert numerical month to month name
month_name_mapping = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
top_3_months['MonthName'] = top_3_months['Month'].map(month_name_mapping)
# Calculate the number of days the goal was achieved
goal_achieved_days =df[df['StepCount'] >= 10000].shape[0]
total_days_in_year = 365

# ---------------------------------------------- Main Page Layout----------------------------------



# Dashboard Title with Style
st.markdown(
    """
    <div style="background-color: #cde8b5; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: #333; font-size: 36px; font-weight: bold; margin-bottom: 0;">Steps Tracker Dashboard 📊</h1>
        <p style="color: #555; font-size: 18px;">Visualizing Progress, Achieving Goals, and Embracing a Healthier Lifestyle</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Information Section
st.markdown(
    """
    <div style="background-color: #f8f8f8; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3>About This Dashboard</h3>
        <p>This dashboard visualizes step count data collected from the "Fitness Tracker" app on my iPhone 📱.</p>
        <p>The data was processed using Python 🐍, and the cleaned data is stored in a Google Cloud Bucket 🪣.</p>
        <p>Streamlit is used to host and present the data in an interactive and informative way.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------ROW 1: Contains three cards " Total Steps Walked", "Total Hours Walked", "Steps per Hour"
st.header('Overview')
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

# --------- ROW 2 --------------------------------
# Display month-by-month steps breakdown
st.header("Month-by-Month Steps Breakdown")

# Monthly Steps Bar Chart
fig_monthly_steps_breakdown = px.bar(df, x='Month', y='StepCount', color='Month',
                                      labels={'StepCount': 'Total Steps'},
                                      title='Month-by-Month Steps Breakdown')
st.plotly_chart(fig_monthly_steps_breakdown)

# Create a Sunburst chart for the top 3 months
fig_top_3_months_sunburst = px.sunburst(top_3_months, path=['MonthName'], values='StepCount',
                                        title='Top 3 Months with Highest Total Steps',
                                        hover_data=['StepCount'])
st.plotly_chart(fig_top_3_months_sunburst)

st.header("Goal Progress")

# Card to display Daily Goal Card
st.markdown(
    f'<div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center;">'
    f'<h3 style="margin-bottom: 0;">Daily Goal</h3>'
    f'<p style="font-size: 18px; color: #4CAF50;">10,000 steps</p>'
    f'</div>',
    unsafe_allow_html=True
)

# Gauge Meter 
fig_goal_progress = go.Figure(go.Indicator(
    mode="number+gauge",
    value=goal_achieved_days,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': f"Goal Achieved (Days) / {total_days_in_year}"},
    gauge={'axis': {'range': [None, total_days_in_year]},
           'bar': {'color': "green"},
           'steps': [{'range': [0, total_days_in_year], 'color': "lightgray"}],
           }))
st.plotly_chart(fig_goal_progress)


# Footnote
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px; font-style: italic; color: #777;">
        <p> Created By Sujan Shahi in 2023. </p>
    </div>
    """,
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













