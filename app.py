import streamlit as st
import pandas as pd
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
    df= pd.read_csv('bases_bicimad.csv', sep=";")
    return df



tab1, tab2= st.tabs(["Product", "Team"])

with tab1:

    st.title("🚲 BiciMad Predictor ")


    stations_data= load_data()
    stations_data.rename(columns={'Longitud':'longitude','Latitud':'latitude'},inplace=True)
    serie=stations_data['Direccion'].copy()
    serie.sort_values(axis=0, ascending=True, inplace=True)


    now = datetime.datetime.now()
    date=now.date()
    time=now.time()
    name_test='Puerta del Sol B'
    options=['--','Address','District','Neighborhood']


    url='https://image-bicimad-xk53jytsnq-ew.a.run.app/predict'
    #url = 'https://bicimad-xk53jytsnq-ew.a.run.app/predict'

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


    result=-1
    with col1:
        if st.button('Let\'s check it'):
            response = requests.get(url, params={'date': date_selected,'time':time_selected,'address':station_selected})
            # st.write(date_selected)
            # st.write(time_selected.hour)
            # st.write(station_selected)
            result=round(float(response.json()["number_bikes"]))
    if result ==0:
        st.subheader(f"❌ Unfortunately! Low probability of having a bike at {station_selected}")
    elif result >0:
        st.subheader(f"🎉 Great! {result} bikes available at {station_selected}")
            # st.write(number)
            # st.write(date_selected)
            # st.write(time_selected.hour)
            # st.write(station_selected)


with tab2:
    col1, col2,col3= st.columns(3)

    with col1:
        st.header("Giulia Baggio")
        st.subheader('Data Scientist')
        image3 = Image.open('IMG_7183.jpg')
        st.image(image3,width=280)
        st.caption('https://www.linkedin.com/in/giulia-baggio')

    with col2:
        st.header("Ines Morais")
        st.subheader('Data Scientist')
        image3 = Image.open('image.png')
        st.image(image3,width=293)
        st.caption('https://www.linkedin.com/in/ines-moreira-silva/')

    with col3:
        st.header("Juan Castro")
        st.subheader('Data Scientist')
        image3 = Image.open('IMG_2946.jpeg')
        st.image(image3,width=300)
        st.caption('https://www.linkedin.com/in/juan-castro-arias/?locale=en_US')
