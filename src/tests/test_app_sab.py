import streamlit as st
import pandas as pd
import time
from PIL import Image
from streamlit_folium import st_folium
import folium

df = pd.read_csv("src/treated_us_activities.csv",
                 on_bad_lines='skip')
st.set_page_config(layout='wide')

img = Image.open("src/images/usa_0.jpeg")
st.image(img, use_column_width='auto')

st.title('Activities for Rémi !')
st.write("""
            Hello Remi! What do you want to do today ?
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
affichage_carte = col1.checkbox("Carte")
affichage_liste = col2.checkbox("Liste")

# --- Traitement des données des features ---
# La langue
for i in range(len(Language)):
    if Language[i] == 'Anglais':
        Language[i] = 1
    elif Language[i] == 'Français':
        Language[i] = 2
    elif Language[i] == 'Espagnol':
        Language[i] = 3

submit = my_form.form_submit_button(label="Submit this form")

# --- Affichage des résultats ---
if submit:
    with st.spinner('We are looking for your best activities...'):
        time.sleep(3)
    st.balloons()

    for j in Language:
        if affichage_carte:
            m = folium.Map(location=[40.7129550, -74.0013617], zoom_start=16)

            latitude = df[(df["Prices"] <= price) &
               (df['Rating'] >= Rating) &
               (df['Language'].str.contains(pat=str(j))) &
               (df['City'] == option_city)]['lat']
            longitude = df[(df["Prices"] <= price) &
               (df['Rating'] >= Rating) &
               (df['Language'].str.contains(pat=str(j))) &
               (df['City'] == option_city)]['lat']
            title = df[(df["Prices"] <= price) &
               (df['Rating'] >= Rating) &
               (df['Language'].str.contains(pat=str(j))) &
               (df['City'] == option_city)]['Title']

            for lat in latitude:
                for lon in longitude:
                    for name in title:
                        folium.Marker(
                            [lat, lon],
                            popup=name,
                            tooltip=name
                        ).add_to(m)

            st_data = st_folium(m, width=725)

        elif affichage_liste:
            df[(df["Prices"] <= price) &
               (df['Rating'] >= Rating) &
               (df['Language'].str.contains(pat = str(j))) &
               (df['City'] == option_city)]
