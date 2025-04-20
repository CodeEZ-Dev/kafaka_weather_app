import pandas as pd
import streamlit as st
# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('weather_data.csv')
# Display Data
st.title("🌦️ Real-Time Weather Dashboard")
data = load_data()
st.subheader("Latest 10 Weather Updates")
st.write(data.tail(10))
st.subheader("🌡️ Temperature Trends")
st.line_chart(data.set_index('timestamp')['temperature'])
st.subheader("💧 Humidity Trends")
st.line_chart(data.set_index('timestamp')['humidity'])