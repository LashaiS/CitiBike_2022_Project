import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 
st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Divvy currently faces")
####################### 
#Import data 
#########################################
df = pd.read_csv('citibike_2022_filtered.csv')
top20 = pd.read_csv('top20.csv')
###########################
# Bar Chart: Top 20 Start Stations
########################### 
fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
     title = 'Top 20 most popular bike stations in New York',
     xaxis_title = 'Start stations',
     yaxis_title ='Sum of trips',
     width = 900, height = 600)

st.plotly_chart(fig, use_container_width = True)
###########################
# Line Chart: 
########################### 
daily_rides = df.groupby('date').size().reset_index(name='bike_rides_daily')
daily_df = daily_rides.merge(
    df[['date', 'avgTemp']].drop_duplicates(),
    on='date',
    how='left'
)
fig_2 = make_subplots(specs = [[{"secondary_y": True}]])
fig_2.add_trace(
 go.Scatter(x = daily_df['date'], y = daily_df['bike_rides_daily'], name = 'Daily bike rides', 
 marker={'color': daily_df['bike_rides_daily'],'color': 'blue'}),
 secondary_y = False)
fig_2.add_trace(
 go.Scatter(x=daily_df['date'], y = daily_df['avgTemp'], name = 'Daily temperature', 
 marker={'color': df['avgTemp'],'color': 'red'}),
 secondary_y=True)

st.plotly_chart(fig_2, use_container_width=True)