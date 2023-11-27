# streamlit_app.py

import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
from st_files_connection import FilesConnection


# Function to get data
@st.cache_data
def get_data():
    conn = st.connection('gcs', type=FilesConnection)
    data = conn.read("sif_bucket/sample_data_11_19_23.csv", ttl=600)
    data['DATE'] = pd.to_datetime(data['DATE'], format = "%Y%m%d")
    return data

df = get_data()

st.title("Website")

# Dropdown to select company
selected_company = st.selectbox("Select Company", df['SYMBOL'].unique())

# Filter data for the selected company
filtered_df = df[df['SYMBOL'] == selected_company]

# Create time series plot
fig1 = px.line(filtered_df, x='DATE', y='quoted_spread', title=f'{selected_company} Quoted Spread Time Series')
fig1.update_xaxes(title_text='Date')
fig1.update_yaxes(title_text='Quoted Spread')

fig2 = px.line(filtered_df, x='DATE', y='effective_spread', title=f'{selected_company} Effective Spread')
fig2.update_xaxes(title_text='Date')
fig2.update_yaxes(title_text='Effective Spread')

fig3 = px.line(filtered_df, x='DATE', y='volatility_trade', title=f'{selected_company} Volatility Trade')
fig3.update_xaxes(title_text='Date')
fig3.update_yaxes(title_text='Volatility Trade')



# Display the plot for quoted spread
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)


