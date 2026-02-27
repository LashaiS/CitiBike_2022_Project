import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go

########################### Initial settings for the dashboard ####################################################

st.set_page_config(page_title='Citi Bike Dashboard', layout='wide')

st.title('Citi Bike New York Dashboard (2022)')
st.markdown('This dashboard explores bike ride patterns and weather trends across New York City in 2022.')
page = st.sidebar.selectbox(
    "Select an aspect of the analysis",
    [
        "Introduction",
        "Top Stations",
        "Trip Trends",
        "User Type Breakdown",
        "Interactive Map View",
        "Insights & Recommendations"
    ]
)

########################## Import data ###########################################################################################
daily_df = pd.read_csv("daily_df.csv")
top_stations_20 = pd.read_csv("top20.csv")
df  = pd.read_csv("reduced_data_to_plot_7.csv")
####################### page function ###########################################################################################
    
if page == "Top Stations":
    st.header(" Most Popular Citi Bike Stations")
    
if page == "Trip Trends":
    st.header("Daily Trips vs Temperature")

if page == "User Type Breakdown":
    st.header("Member vs Casual Usage (2022)")
    
if page == "Interactive Map View":
    st.header("Trip Trends Over Time")
    
if page == "Insights & Recommendations":
    st.header("Insights")
    st.header("Recommendations")
    
### Intro page
if page == "Introduction":
    st.header("Welcome to the Citi Bike Dashboard (2022)")
    st.subheader("Overview")
    
    st.image("nyc_skyline.jpg", use_container_width=True)
    
    st.write(
        """
        This dashboard explores Citi Bike trip patterns in 2022 to understand when and where demand is highest. The goal is to surface trends, identify the most popular stations, and show geographic patterns that can inform station planning and rebalancing decisions.
        """
    )
    st.markdown("### What you'll find in this dashboard")
    st.markdown(
        """
        -**Top Stations:** Which stations have the highest activity
        
        -**Trip Trends:** How trips change over time due to seasonality and daily patterns
        
        -**User Type Breakdown: ** How usage differs between members and casual riders
        
        -**Interactive Map View:** Where trip concentrate geographically
        
        -**Insights & Recommendations:** Takeaways for improving bike availablity
        
        """
    )
    st.markdown("### Data")
    st.write(
        """
        Source: Citi Bike trip datat (2022) - https://s3.amazonaws.com/tripdata/index.html
        """
    )

    
    
### Top Station Page
if page == "Top Stations":
    st.header("Top Stations:")
    st.subheader(" Most Popular Citi Bike Stations")

st.image("top_station.jpg", use_container_width=True)

st.header("Top Stations:")
st.subheader(" Most Popular Citi Bike Stations")   

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

st.markdown('### Interpreation')
st.write("""
The chart highlights the 20 stations with the highest trip activity in 2022. The station with the highest volume are likely located in major transit hub, dense commercial areas, or popular destinations areas where the need for bikes is high. 
""")




### Trip Trends Page
if page == "Trip Trends":
    st.header("Trip Trends:")
    st.subheader("Daily Trips vs Temperature")

st.image("trip.jpg", use_container_width=True)

st.header("Trip Trends:")
st.subheader("Daily Trips vs Temperature")

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

st.markdown("### Interpretation")
st.write("""
The dual-axis chart compares daily trip volume with the average temperature during 2022. Trips generally increase as temperature increases. This is shown during late spring through early fall ,and then declines during the colder months. Short spikes may reflect weekend or holiday demands which can be monitored to trigger temporary rebalancing. There is a strong seasonality in Citi Bike usage.
""")

st.subheader("Monthly Citi Bike Demand vs Average Temperature")

daily_df['date'] = pd.to_datetime(daily_df["date"], errors="coerce")

month_df = daily_df.dropna(subset=['date', "bike_rides_daily", "avgTemp"]).copy()

month_df["month"] = month_df['date'].dt.month_name()

month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

month_df["month"] = pd.Categorical(month_df['date'].dt.month_name(), categories=month_order, ordered=True)

month_summary = month_df.groupby("month", as_index=False).agg(
    avg_daily_trips=("bike_rides_daily", "mean"),
    avg_temp=("avgTemp", "mean")
)

month_summary = month_summary.sort_values("month")

fig_month = go.Figure()

fig_month.add_trace(
    go.Scatter(
        x=month_summary["month"],
        y=month_summary["avg_daily_trips"],
        name="Average Daily Trips",
        yaxis="y1"
    )
)

fig_month.add_trace(
    go.Scatter(
         x=month_summary["month"],
        y=month_summary["avg_temp"],
        name="Average Temperature",
        yaxis="y2"
    )
)

fig_month.update_layout(
    title="Monthly Citi Bike Demand vs Average Temperature (2022)",
    template="plotly_white",
    xaxis=dict(title="Month"),
    yaxis=dict(title="Average Daily Trips"),
    yaxis2=dict(
        title="Average Temperature",
        overlaying='y',
        side='right'
    )
)
st.plotly_chart(fig_month, use_container_width=True)

st.markdown("### Interpretation")
st.write("""
This line chart shows the relationship of bike usage and avgerage temperature over a monthly scale in 2022.
Bike usage increase steadily as temperature rise, peaking in the summer months when weather conditions are most favorable. As temperature declines in the fall and winter, the volume of rides decreases. 
This indicates that temperature is a key driver of demand.
""")



### Trip Trends: Week Demands
st.subheader("Supply Analysis: Demand by Day of Week")
st.markdown("### Identifying peak usage days")

daily_df['date'] = pd.to_datetime(daily_df["date"], errors="coerce")
dow_df = daily_df.dropna(subset=["date", "bike_rides_daily"]).copy()

dow_df["day_of_week"] = dow_df['date'].dt.day_name()

dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_df["day_of_week"] = pd.Categorical(dow_df['day_of_week'], categories=dow_order, ordered=True)

dow_summary = (
    dow_df.groupby("day_of_week", as_index=False)["bike_rides_daily"]
    .mean()
    .rename(columns={"bike_rides_daily": "avg_daily_trips"})
)

fig_dow = px.bar(
    dow_summary,
    x="day_of_week",
    y="avg_daily_trips",
    title="Average Daily Trips by Day of Week",
    color="avg_daily_trips",
    color_continuous_scale=[
        [0, "#c6dbef"],
        [0.5, "#6baed6"],
        [1, "#08306b"]
    ]
)

fig_dow.update_layout(
    template="plotly_white",
    xaxis_title="Day of Week",
    yaxis_title="Average Daily Trips"
)
st.plotly_chart(fig_dow, use_container_width=True)

st.markdown('### Interpretation')
st.write("""
This chart highlights which days generate the highest bike demand. Wednesdays, Saturdays, and Fridays are the top three days in orders have the highest bike usage. From Wednesday to Saturday, Citi bike trends shows strong commuter demand and weekend usage suggest moe recreational rides.
""")


### User BreakDown
if page == "User Type Breakdown":
    st.header("User Type Breakdown:")
    st.subheader("Member vs Casual Usage (2022)")

st.image("daily.jpg", use_container_width=True)

st.header("User Type Breakdown:")
st.subheader("Member vs Casual Usage (2022)")


user_summary = df["member_casual"].value_counts().reset_index()
user_summary.columns = ["User Type", "Number of Trips"]

fig_user = px.bar(
    user_summary,
    x="User Type",
    y="Number of Trips",
    color="User Type",
    title="Citi Bike Usage by User Type (2022)",
    color_discrete_map={
        "member": "#08306b",
        "casual": "#6baed6"
    }
)

fig_user.update_layout(template="plotly_white")
st.plotly_chart(fig_user, use_container_width=True)

st.markdown('### Interpretation')
st.write("""
This chart highlights that Citi Bike usage is primarily driven by members, indicating strong demand from daily commuters.
Causal riders represent a smaller portion of trips, suggesting that routine transportation needs contribute most to overall bike usage. 
""")



### Interactive Map View Page
if page == "Interactive Map View":
    st.header("Interactive Map View")
    
st.image("busy.jpg", use_container_width=True)
st.header("Interactive Map View")

st.subheader("Citi Bike Trip Hotspots (2022)")

import streamlit.components.v1 as components


with open("citiBike_2022_map.html", "r", encoding="utf-8") as f:
    map_html = f.read()
components.html(map_html, height=600, scrolling=True)

st.markdown("### Interpretation")
st.write("""
This map shows where Citi Bike trips concentrate geographically in 2022. 
The yellow points represent Citi Bike stations, and the arcs show trips between stations. The thickness of each arc indicates how many trips occurred between those locations, with thicker lines representing more popular routes.
Trips cluster in the core service areas, and around high density and high traffic loactions. This pattern suggest demand is not evenly spread around New York City.
""")

### Insights & Recommendations
if page == "Insights & Recommendations":
    st.header("Insights & Recommendations")

st.image("nyc_citibikes.jpg", use_container_width=True)  

st.header("Insights & Recommendations")
st.subheader("Key Insights")

st.markdown("**1) Demand is Highest in Warmer Months**")
st.write("""
Bike usage steadily increases from winter into summer, peaking around July and August. The usage decline with the temperature in the fall and winter. This shows a strong relatioship between weather and rides.
""")

st.markdown("**2) Weekday Riders is Stronger Than Weekends**")
st.write("""
Wednesday - Saturday show the highest volume of rides. Wednesdays showing the most rides during the week.
This suggests that Citi Bike is heavily used for commuting rather than leisure.
""")

st.markdown("**3) Members Drive the Majority of Trips**")
st.write("""
The User Type Breakdown shows that members use Citi Bikes the most.
While casual riders represent a small portion, this confirms that Citi Bike is used by regular commuters.
""")

st.markdown("**4) High Activity is Concentrated in Specific Areas**")
st.write("""
The Top Stations and Map View reveal that demand is clustered around certain neighborhoods
and transit hubs, indicating that riders frequently start and end trips in high traffic areas.
""")


st.header("Recommendations")

st.markdown("**1) Increase Bike Availablity in the Spring & Summer**")
st.write("""
Since demand peaks in the warmer months , Citi Bike should add more bikes to the high demand stations
and increase rebalancing frequency during the summer to prevent empty stations.
""")
st.markdown("**2) Prioritize High Demand Stations**")
st.write("""
Stations with the highest activity should recieve more bikes, faster maintenance,
and restocking to ensure reliable service.
""")
st.markdown("**3) Focus on Commuter Routes**")
st.write("""
Due to the most users being memebers and weekday riders, Citi Bike should prioritizes stations near
busy streets, and transit hubs in the morning and evening rush hours.
""")
st.markdown("**4) Use Data to Predict Demands**")
st.write("""
The consistent patterns in weather, day of the week, and user type allow Citi Bike to 
forecast demand and plan resources effectively, improving efficiency and rider experience.
""")