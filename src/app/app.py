import streamlit as st
import pandas as pd
import time
from PIL import Image
from streamlit_folium import folium_static
import folium

df = pd.read_csv("src/treated_us_activities.csv",
                 on_bad_lines='skip')

st.set_page_config(
    layout='wide',
    page_title = "Remi's activities planner App",
    page_icon = "🕺🏻",
)

audio = st.audio('src/app/audio/NY_sinatra.mp3', start_time=0)
img = Image.open("src/app/images/usa_0.jpeg")
st.image(img, use_column_width='auto')

st.title('Activities for Rémi ! 🕺🏻')
st.write("""
            Hello Rémi! What do you want to do today ?
         """)

# --- Choix des features ---
# Choix de la ville
my_form = st.form(key="form1")
option_city = my_form.selectbox('Where are you ?',
                                ('New York', 'Las Vegas', 'Boston', 'San Francisco',
                                 'Washington', 'Chicago', 'Los Angeles', 'Miami', 'Atlanta'))

# Choix des autres features
col1, col2, col3 = my_form.columns(3)
price = col1.slider("Price", 0, 5000)
Rating = col2.slider("Rating", 0, 10)
Language = col3.multiselect("Language : ", ['Anglais', 'Français', 'Espagnol'])
affichage = col1.radio("Which display would you like ?", ["Map", "List"])

submit = my_form.form_submit_button("Let's have fun !")

# --- Traitement des données des features selectionnées ---
# La langue - On change les données textes en chiffres
for i in range(len(Language)):
    if Language[i] == 'Anglais':
        Language[i] = 1
    elif Language[i] == 'Français':
        Language[i] = 2
    elif Language[i] == 'Espagnol':
        Language[i] = 3

# Si l'utilisateur ne spécifie pas de langue, on les prend toutes en compte
if len(Language) == 0:
    Language.append(1)
    Language.append(2)
    Language.append(3)
    Language.append(-1)

# --- Fonctions d'affichages---
def display_map(map):
    """
    Function that display the map with the activities available with the selected features

    :param map: the folium map created
    """
    for j in Language:
        latitudes = df[(df["Prices"] <= price) &
                      (df['Rating'] >= Rating) &
                      (df['Language'].str.contains(pat=str(j))) &
                      (df['City'] == option_city)]['lat']
        longitudes = df[(df["Prices"] <= price) &
                       (df['Rating'] >= Rating) &
                       (df['Language'].str.contains(pat=str(j))) &
                       (df['City'] == option_city)]['lon']
        titles = df[(df["Prices"] <= price) &
                   (df['Rating'] >= Rating) &
                   (df['Language'].str.contains(pat=str(j))) &
                   (df['City'] == option_city)]['Title']

    for lat, lon, title in zip(latitudes, longitudes, titles):
        folium.Marker(
            [lat, lon],
            popup=title,
            tooltip=title,
            icon=folium.Icon(icon="cloud")
        ).add_to(map)

    st_data = folium_static(map, width=1275)


@st.cache(suppress_st_warning=True)
def display_list():
    """
    Function that display the list of the activities available with the selected features
    """
    for j in Language:
        titles = df[(df["Prices"] <= price) &
           (df['Rating'] >= Rating) &
           (df['Language'].str.contains(pat=str(j))) &
           (df['City'] == option_city)]['Title']
        images = df[(df["Prices"] <= price) &
           (df['Rating'] >= Rating) &
           (df['Language'].str.contains(pat=str(j))) &
           (df['City'] == option_city)]['image']
        prices = df[(df["Prices"] <= price) &
           (df['Rating'] >= Rating) &
           (df['Language'].str.contains(pat=str(j))) &
           (df['City'] == option_city)]['Prices']
        ratings = df[(df["Prices"] <= price) &
           (df['Rating'] >= Rating) &
           (df['Language'].str.contains(pat=str(j))) &
           (df['City'] == option_city)]['Rating']
        durations = df[(df["Prices"] <= price) &
           (df['Rating'] >= Rating) &
           (df['Language'].str.contains(pat=str(j))) &
           (df['City'] == option_city)]['Duration']
        annulations = df[(df["Prices"] <= price) &
           (df['Rating'] >= Rating) &
           (df['Language'].str.contains(pat=str(j))) &
           (df['City'] == option_city)]['Annulation']

        for title, image, act_price, rating, duration, annulation in zip(titles, images, prices, ratings, durations, annulations):
            c = st.container()
            col_img, col_text = c.columns((2, 3))

            with col_img:
                st.image(image, width=400)
            with col_text:
                st.header(title)
                st.write("Price: ", str(act_price), "€")
                st.write("Rating: ", str(rating), "/10")
                st.write("Duration: ", duration)

# --- Affichage des résultats ---
if submit:
    with st.spinner('We are looking for your best activities...'):
        time.sleep(3)
    st.balloons()

    if affichage == 'Map':
        center_coord = []
        if option_city == 'New York':
            center_coord = [40.7129550, -74.0013617]
        elif option_city == 'Las Vegas':
            center_coord = [36.2057143, -115.1548737]
        elif option_city == 'Boston':
            center_coord = [42.3630547, -71.0664598]
        elif option_city == 'San Francisco':
            center_coord = [37.7786899, -122.4281743]
        elif option_city == 'Washington':
            center_coord = [38.9439587, -76.9606802]
        elif option_city == 'Chicago':
            center_coord = [41.9022766, -87.6288040]
        elif option_city == 'Los Angeles':
            center_coord = [34.0531639, -118.2524682]
        elif option_city == 'Miami':
            center_coord = [25.7616761, -80.1940987]
        elif option_city == 'Atlanta':
            center_coord = [33.7486826, -84.3904340]
        m = folium.Map(location=center_coord, zoom_start=12)
        display_map(m)

    elif affichage == 'List':
        display_list()

