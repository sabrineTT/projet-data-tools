import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image

df = pd.read_csv("src/us_activities.csv",
                 on_bad_lines='skip')
st.set_page_config(layout='wide')

img = Image.open("src/images/usa_0.jpeg")
st.image(img, use_column_width='auto')

st.title('Activities for Rémy !')
st.write("""
            Hello Remy! What do you want to do today ?
         """)

# with st.form(key = "form1"):
my_form = st.form(key="form1")
option_city = my_form.selectbox('Where are you ?',
                                ('New York City', 'Las Vegas', 'Boston', 'San Francisco',
                                 'Washington', 'Chicago', 'Los Angeles', 'Miami', 'Atlanta',
                                 'Seattle', 'Tampa', 'Orlando', 'Fort Lauderdale', 'Houston',
                                 'Honolulu', 'Key West', 'Nouvelle Orleans', 'Philadelphie',
                                 'Pheonix', 'San Diego', 'San Antonio'))

col1, col2, col3 = my_form.columns(3)
price = col1.slider("Price", 0, 5000)
Rating = col2.slider("Rating", 0, 10)
Language = col3.multiselect("Language : ", ['Anglais', 'Français', 'Espagnol'])

submit = my_form.form_submit_button(label="Submit this form")

if submit:
    with st.spinner('We are looking for your best activities...'):
        time.sleep(3)
    st.balloons()

    st.map(df)
    df[df["Prices"] <= price]
    if st.checkbox("Carte"):
        st.map(df)
    elif st.checkbox("Liste"):
        df
    # afficher les activités de la ville choisie et prix max