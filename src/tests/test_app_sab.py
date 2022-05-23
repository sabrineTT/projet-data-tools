import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv("src/USA_activities.csv", on_bad_lines='skip')

st.title('Activities for Rémy !')
st.write("""
            Hello *Remy!*
         """)
option = st.selectbox('Dans quelle ville souhaitez-vous vous amuser ?',
                      ('New York City', 'Las Vegas', 'Boston', 'San Francisco',
                       'Washington', 'Chicago', 'Los Angeles', 'Miami', 'Atlanta',
                       'Seattle', 'Tampa', 'Orlando', 'Fort Lauderdale', 'Houston',
                       'Honolulu', 'Key West', 'Nouvelle Orleans', 'Philadelphie',
                       'Pheonix', 'San Diego', 'San Antonio'))
st.write('You selected:', option)

price = st.slider("Price", 0, 5000)
if st.button("Search"):
    st.map(df)
    df[df["Prices"] <= price]
    if st.checkbox("Carte"):
        st.map(df)
    elif st.checkbox("Liste"):
        df
    #afficher les activités de la ville choisie et prix max
else:
    st.write('choose')