import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='Citi Bike Dashboard', layout='wide')

st.title('Citi Bike New York Dashboard (2022)')
st.markdown('This dashboard explores bike ride patterns and weather trends across New York City in 2022.')
#load data
daily_df = pd.read_csv("daily_df.csv")
top_stations_20 = pd.read_csv("top20.csv")

st.header(" Most Popular Citi Bike Stations")

import plotly.express as px

fig_bar_20 = px.bar(
    top_stations_20,
    x="Number of Trips",
    y="Station Name",
    orientation='h',
    title=" Top 20 Most Popular Citi Bike Station in New York - 2022",
     color="Number of Trips",
    color_continuous_scale='Blues'
)

fig_bar_20.update_layout(
    template='plotly_white',
    height=600
)
st.plotly_chart(fig_bar_20, use_container_width=True)

st.header("Daily Trips vs Temperature")

fig = go.Figure()

#Temperature
fig.add_trace(
    go.Scatter(
        x=daily_df['date'],
        y=daily_df['avgTemp'],
        name="Average Temperature",
        yaxis='y1',
        line=dict(color='red')
    )
)
#Trips
fig.add_trace(
    go.Scatter(
        x=daily_df['date'],
        y=daily_df['bike_rides_daily'],
        name="Number of Trips",
        yaxis='y2',
        line=dict(color='blue')
    )
)
fig.update_layout(
    title="Daily Trips vs Temperature - 2022",
    xaxis=dict(title="Date"),
    yaxis=dict(
        title="Number of Trips",
    ),
    yaxis2=dict(
        title="Average Temperature",
        overlaying='y',
        side='right'
    ),
    template='plotly_white',
    height=600
)
st.plotly_chart(fig, use_container_width=True)

import streamlit.components.v1 as components

st.header("Citi Bike Trip Map")

with open("citiBike_2022_map.html", "r", encoding="utf-8") as f:
    map_html = f.read()
components.html(map_html, height=600, scrolling=True)