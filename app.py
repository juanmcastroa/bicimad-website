import streamlit as st
import pandas as pd
#from datetime import datetime
#from folium.plugins import HeatMap
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
#import flickrapi
import random
#from dotenv import load_dotenv
import os
import urllib
import plotly.express as px
import requests
import datetime
from PIL import Image
import numpy

#set page layout
st.set_page_config(
    page_title="BiciMad Predictor",
    page_icon="bike",
    layout="wide")

@st.cache
def load_data():
    """ Load the cleaned data with latitudes, longitudes & timestamps """
    df = pd.read_csv("station_1.csv")
    df['id']=pd.to_datetime(df['id'], format='%Y-%m-%d %H:%M:%S', errors='ignore',exact=True)
    #travel_log["date"] = pd.to_datetime(travel_log["ts"])
    return df



tab1, tab2= st.tabs(["Product", "Team"])

with tab1:

    st.title("🚲 BiciMad Predictor ")


    travel_data = load_data()


    stations_data= pd.read_csv('bases_bicimad.csv', sep=";")
    stations_data.rename(columns={'Longitud':'longitude','Latitud':'latitude'},inplace=True)
    serie=stations_data['Direccion'].copy()
    serie.sort_values(axis=0, ascending=True, inplace=True)

    # Calculate the timerange for the slider
    min_ts = travel_data["id"].min()
    max_ts = travel_data["id"].max()

    now = datetime.datetime.now()
    date=now.date()
    time=now.time()
    name_test='Puerta del Sol B'
    options=['--','Address','District','Neighborhood']


    #new_row need to be updated by information from the station
        #number, light, total_bases, longitude, latitude, weather,

    # new_row={'activate':1, 'name':name, 'reservations_count':0, 'light':0, 'total_bases':30,
    #     'free_bases':28, 'number':'1b', 'longitude':-3.701603, 'no_available':0, 'address':'Puerta del Sol nº 1',
    #     'latitude':-3.701603, 'dock_bikes':0, 'id':(str(date)+'T'+str(time)), 'time':time, 'date':date, 'holidays':holiday, 'datetime':datetime,
    #     'feels_like':17.44, 'weather_main':'Rain', 'weekday':weekday, 'year':year, 'month':month, 'hour_sin':hour_sin,
    #     'hour_cos':hour_cos, 'weekday_sin':weekday_sin, 'weekday_cos':weekday_cos, 'month_sin':month_sin, 'month_cos':month_cos}

    #date_selected= st.sidebar.date_input('When do you want to take your bike', datetime.datetime.today())
    #time_selected= st.sidebar.time_input('At what time will you take your bike', now)
    #day_selected =st.sidebar.selectbox('Select day', range(1,31))
    #month_selected =st.sidebar.selectbox('Select month', ['January','February','March','June','July','August','September','October','November','December'])

    #predict=st.sidebar.text_input('Prueba')


    url = 'https://bicimad-xk53jytsnq-ew.a.run.app/predict'

    col1, col2= st.columns(2)

    with col2:
        st.header("📍 Map")

    with col1:
        st.header("🔎 Prepare your trip")
        date_selected= st.date_input('📅 Date', datetime.datetime.today())
        time_selected= st.time_input('⏰ Time', now)
        search_by=st.selectbox('Search by',options)
        if search_by=='--':
            with col2:
                    st.map( stations_data)

        elif search_by=='Neighborhood':
            neighborhood_selected =st.selectbox('Select your neigborhood', numpy.sort(stations_data['Barrio'].unique()))
            station_selected=st.selectbox('Select your station', stations_data[stations_data['Barrio']==neighborhood_selected]['Direccion'])
            if st.checkbox('Locate'):
                with col2:
                    st.map(stations_data[stations_data['Direccion']==station_selected])
            else:
                with col2:
                    st.map( stations_data)

        elif search_by=='District':
            district_selected =st.selectbox('Select your district', numpy.sort(stations_data['Distrito'].unique()))
            neighborhood_selected=st.selectbox('Select your neigborhood', stations_data[stations_data['Distrito']==district_selected]['Barrio'].unique())
            station_selected =st.selectbox('Select your station', stations_data[stations_data['Barrio']==neighborhood_selected]['Direccion'])
            if st.checkbox('Locate'):
                with col2:
                    st.map(stations_data[stations_data['Direccion']==station_selected])
            else:
                with col2:
                    st.map( stations_data)
        elif search_by=='Address':
            station_selected =st.selectbox('Select your station', serie)
            if st.checkbox('Locate'):
                with col2:
                    st.map(stations_data[stations_data['Direccion']==station_selected])
            else:
                with col2:
                    st.map( stations_data)





    # selected_info=stations_data[stations_data['Direccion']==station_selected]
    # name=stations_data[stations_data['Direccion']==station_selected]

    # longitude=stations_data.loc[stations_data['Direccion']==station_selected]['longitude'].values[0]

    # latitude=stations_data.loc[stations_data['Direccion']==station_selected]['latitude'].values[0]

    # total_bases =stations_data.loc[stations_data['Direccion']==station_selected]['Número de Plazas'].values[0]

    # number=stations_data.loc[stations_data['Direccion']==station_selected]['Número'].values[0]
    # number=number.replace(" ", "")
    # while number=='0':
    #     number=number[1:]
    # number_test=number
    # address=stations_data[stations_data['Direccion']==station_selected]['Direccion']
    # list_stations=list(stations_data['Número'])
    result=-1
    with col1:
        if st.button('Predict'):
            response = requests.get(url, params={'date': date_selected,'time':time_selected,'name':station_selected})
            # st.write(date_selected)
            # st.write(time_selected.hour)
            # st.write(station_selected)
            result=round(float(response.json()["number_bikes"]))
    if result ==0:
        st.subheader(f"❌ Unfortunately! Low probability of having a bike at {station_selected}")
    elif result >0:
        st.subheader(f"🎉 Great! {result} bikes availableat {station_selected}")
            # st.write(number)
            # st.write(date_selected)
            # st.write(time_selected.hour)
            # st.write(station_selected)


with tab2:
    col1, col2,col3= st.columns(3)

    with col1:
        st.header("Giulia Baggio")

    with col2:
        st.header("Ines Morais")

    with col3:
        st.header("Juan Castro")
        st.subheader('Data Scientist')
        image3 = Image.open('IMG_2946.jpeg')
        st.image(image3,width=300)
        st.caption('https://www.linkedin.com/in/juan-castro-arias/?locale=en_US')
