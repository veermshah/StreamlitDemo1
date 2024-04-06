import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie # for animations
import plost

def countDays():
    count = seattle_weather['weather'].value_counts()
    
    counts_df = pd.DataFrame(count)
    
    counts_df.reset_index(inplace=True)
    
    counts_df.columns = ['Weather', 'Count']
    
    counts_df.to_csv('weather_counts.csv', index=False)
    
st.set_page_config(page_title='Weather Dashboard', page_icon=':rain_cloud:', layout='wide', initial_sidebar_state='expanded')

st.title(':rain_cloud: Weather Dashboard')

# SIDEBAR
st.sidebar.title('Settings')
st.sidebar.subheader('Heat map parameters')
choice = st.sidebar.selectbox('Select a paremeter', ('temp_min', 'temp_max'))
st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect('Select data to plot', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'] ) 
plot_height = st.sidebar.slider('Select the height of the plot', 200, 500, 250)

# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Row B
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
countDays()
weather_counts_csv = pd.read_csv('weather_counts.csv')

c1, c2 = st.columns((7, 3))
with c1:
    st.markdown('### Heatmap')
    plost.time_hist(
        data=seattle_weather,
        date='date',
        x_unit='week',
        y_unit='day',
        color=choice,
        aggregate='median',
        legend=None,
        height=360,
        use_container_width=True
    )

with c2:
    st.markdown('### Donut chart')
    plost.donut_chart(
        data=weather_counts_csv,
        theta='Count',
        color='Weather',
        legend='bottom',
        use_container_width=True
        
        
    )
    
# Row C
st.markdown('### Line Chart')
st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)

lottie_url = "https://lottie.host/4a8322b4-981b-4d72-8309-0adbb6305351/a4zyCyhizk.json"
st_lottie(lottie_url, width=200, height=200)
