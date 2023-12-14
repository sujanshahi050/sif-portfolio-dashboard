# streamlit_app.py

# Importing Libraries
import streamlit as st
import altair as alt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from st_files_connection import FilesConnection
from datetime import datetime

# Function to get data
@st.cache_data
def get_data():
    conn = st.connection('gcs', type=FilesConnection)
    data = conn.read("sif_bucket/sample_data_11_19_23.csv", ttl=600)
    data['DATE'] = pd.to_datetime(data['DATE'], format = '%Y%m%d').dt.strftime('%Y-%m-%d')
    return data

# Assign the data to a dataframe
df = get_data()

# Select variable for comparison
selected_variables = st.multiselect('Select Variable', df.columns[2:])

# Select ticker
selected_ticker = st.multiselect('Select Ticker', df['SYMBOL'].unique(), default=df['SYMBOL'].unique()[0])

# Filter dataframe based on selected ticker(s)
filtered_df = df[df['SYMBOL'].isin(selected_ticker)]

# Create line chart with range selector button
fig = px.line(filtered_df, x='DATE', y=selected_variables, color='SYMBOL',
              labels={'value': 'Value', 'variable': 'Metric'})

# Add date range slider within the chart layout
fig.update_layout(
    xaxis_rangeslider_visible=True,
    xaxis_title='Date Range',
    yaxis_tickformat=".6f",  # Adjust this format based on your preference
)

# Add range selector buttons and show gridlines
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1mo", step="month", stepmode="backward"),
                dict(count=6, label="6mo", step="month", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor='green',  # Background color of range selector
            font=dict(color='white')  # Font color of range selector
        ),
        rangeslider=dict(visible=True),
        type="date",
        tickfont=dict(color='black'),  # Font color of x-axis ticks
        showgrid=True,  # Show x-axis gridlines
        gridcolor='grey'  # Color of gridlines
    ),
    yaxis=dict(
        title=dict(text=", ".join(selected_variables), font=dict(color='white')),  # Join variables into a single string  # Font color of y-axis title
        tickfont=dict(color='black'),  # Font color of y-axis ticks
        showgrid=True,  # Show y-axis gridlines
        gridcolor='grey',  # Color of gridlines
        rangemode='tozero'  # Start y-axis from zero
    ),
    paper_bgcolor='white',  # Background color of the entire chart
    plot_bgcolor='white'  # Background color of the plot area
)


# Display the chart
st.plotly_chart(fig)
# Plot the data














