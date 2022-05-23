"""try:
    coord_class = driver.find_element_by_xpath(
        "//div[@class='m-map js-map-new js-static-on-create loaded-map']")
    coord = coord_class.get_attribute("data-markers")
    coord_list.append(coord.text)
except NoSuchElementException:
    coord_list.append(-1)"""

#rajouter l'url de l'image d'entrée ?
import json

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:12:03 2022

@author: kju78
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

options = Options()
options.headless = True  # etre prive
options.add_argument("--window-size=1920,1080")  # dimension fenetre
options.add_argument("start-maximized")  # mise en plein ecran de la fenetre

driver = webdriver.Chrome("../chromedriver")  # adresse driver chrome

# =============================================================================
# Variables a definir :
# =============================================================================

debut = 1  # variable pour indentation nombre de page parcourues - a changer
fin = 5

page = debut  # a laisser

# =============================================================================
# Listes de stockage :
# =============================================================================

urls_list = []

prices_list = []
nb_visits_list = []

titles_list = []
nb_ratings_list = []
ratings_list = []
annulation_list = []
durations_list = []
languages_list = []
cities_list = []
coord_list = []

# =============================================================================
# Scraping :
# =============================================================================

def scrapping_url(debut, fin, page):
    try:
        while debut <= page <= fin:

            # url = 'https://www.civitatis.com/fr/new-york/?page=%d'%(page) #5
            url = 'https://www.civitatis.com/fr/las-vegas/?page=%d'%(page) #3
            # url = 'https://www.civitatis.com/fr/boston/?page=%d'%(page) #1
            # url = 'https://www.civitatis.com/fr/san-francisco/?page=%d'%(page) #2
            # url = 'https://www.civitatis.com/fr/washington/?page=%d'%(page) #1
            # url = 'https://www.civitatis.com/fr/chicago/?page=%d'%(page) #1
            # url = 'https://www.civitatis.com/fr/los-angeles/?page=%d'%(page) #2
            # url = 'https://www.civitatis.com/fr/miami/?page=%d'%(page) #3
            # url = 'https://www.civitatis.com/fr/atlanta/'  # 1

            driver.get(url)

            time.sleep(5)

            urls = driver.find_elements_by_xpath("//a[@class='ga-trackEvent-element _activity-link']")

            prices = driver.find_elements_by_xpath("//span[@class='comfort-card__price__text']")
            nb_visits = driver.find_elements_by_xpath("//span[@class='comfort-card__traveler-count _full']")

            page += 1

            for u in range(len(urls)):
                url = urls[u].get_attribute('href')
                urls_list.append(str(url))

            for p in range(len(prices)):
                price = prices[p]
                prices_list.append(price.text)

            for nb in range(len(nb_visits)):
                nb_visit = nb_visits[nb]
                nb_visits_list.append(nb_visit.text)



    except WebDriverException:
        pass

    return urls_list, prices_list, nb_visits_list


def scrapping(urls_list):
    compteur = 1
    print('itérations nécessaires : ', len(urls_list) + 1)

    for url in range(len(urls_list)):  # parcours de la liste des liens recoltes

        try:

            driver.get(urls_list[url])

            print('itération actuelle : ', compteur, '/', len(urls_list) + 1)

            time.sleep(5)
            try:
                title = driver.find_element_by_xpath("//h1[@class='a-title-activity']")
                titles_list.append(title.text)
            except NoSuchElementException:
                titles_list.append(-1)

            try:
                nb_rating = driver.find_element_by_xpath("//div[@class='a-text--rating-total']/a")
                nb_ratings_list.append(nb_rating.text)
            except NoSuchElementException:
                nb_ratings_list.append(-1)

            try:
                rating = driver.find_element_by_xpath(
                    "//div[@class='o-rating__title o-activity-header__rating__title']/a")
                ratings_list.append(rating.text)
            except NoSuchElementException:
                ratings_list.append(-1)

            try:
                annulation = driver.find_element_by_xpath("//div[@class='p']")
                annulation_list.append(annulation.text)
            except NoSuchElementException:
                annulation_list.append(-1)

            try:
                duration = driver.find_element_by_xpath(
                    "//li[@class='o-advantages--header__element  --important  o-advantages-icon-duration ']/a")
                durations_list.append(duration.text)
            except NoSuchElementException:
                durations_list.append(-1)

            try:
                language = driver.find_element_by_xpath(
                    "//span[@class='a-feature a-feature-lang o-advantages-icon-lang']")
                languages_list.append(language.text)
            except NoSuchElementException:
                languages_list.append(-1)

            city = urls_list[0].split("/")[4]
            cities_list.append(city)

            #recupération des coordonnées lat et long pour la carte de l'app
            try:
                coord_class = driver.find_element_by_id(
                    "meeting-point-map-container")
                coord = coord_class.get_attribute('data-markers')
                char_to_delete = ['[', ']', '{', '}', '"']
                for char in char_to_delete:
                    coord = coord.replace(char, '')
                coord = coord.split(",", 2)  #retourne une liste, par ex : ['lat:33.7633886', 'lng:-84.3952799']
                coord_list.append(coord[:2])
            except NoSuchElementException:
                if city == 'atlanta':
                    coord_list.append(['lat:33.7486826', 'lng:-84.3904340'])
                elif city == 'new-york':
                    coord_list.append(['lat:40.7129550', 'lng:-74.0013617'])
                elif city == 'las-vegas':
                    coord_list.append(['lat:36.2057143', 'lng:-115.1548737'])
                elif city == 'boston':
                    coord_list.append(['lat:42.3630547', 'lng:-71.0664598'])
                elif city == 'san-francisco':
                    coord_list.append(['lat:37.7786899', 'lng:-122.4281743'])
                elif city == 'washington':
                    coord_list.append(['lat:38.9439587', 'lng:-76.9606802'])
                elif city == 'chicago':
                    coord_list.append(['lat:41.9022766', 'lng:-87.6288040'])
                elif city == 'los-angeles':
                    coord_list.append(['lat:34.0531639', 'lng:-118.2524682'])
                elif city == 'miami':
                    coord_list.append(['lat:25.7616761', 'lng:-80.1940987'])

            compteur += 1

        except WebDriverException:
            pass

    return titles_list, nb_ratings_list, ratings_list, annulation_list, durations_list, languages_list, cities_list, coord_list
    # return titles_list, nb_ratings_list, prices_list, nb_visits_list, ratings_list


# =============================================================================
# Main :
# =============================================================================

def main():
    urls_list, prices_list, nb_visits_list = scrapping_url(debut, fin, page)
    titles_list, nb_ratings_list, ratings_list, annulation_list, durations_list, languages_list, cities_list, coord_list = scrapping(
        urls_list)

    # =============================================================================
    # Séparation des coordonnées Latitude et Longitude en 2 listes :
    # =============================================================================

    lat_list = []
    lon_list = []
    lat = ''
    lon = ''

    for coords in coord_list:
        #lat_list.append(coords[0])
        #lon_list.append(coords[1])
        for i in coords[0]:
            if i.isnumeric() == True or i == '.' or i == '-':
                lat+=i
        lat_list.append(float(lat))
        lat = ''
        for i in coords[1]:
            if i.isnumeric() == True or i == '.' or i == '-':
                lon+=i
        lon_list.append(float(lon))
        lon = ''

    # =============================================================================
    # Création du dataframe :
    # =============================================================================

    driver.close()  # fermeture de la fenetre de scraping

    df = pd.DataFrame(list(
        zip(titles_list, nb_ratings_list, prices_list, nb_visits_list, ratings_list, annulation_list, durations_list,
            languages_list, cities_list, lat_list, lon_list)),
                      columns=['Title', 'Nb rating', 'Prices', 'Nb visits', 'Rating', 'Annulation', 'Duration',
                               'Language', 'City', 'lat', 'lon'])  # creation d'une base de donnees
    # df = pd.DataFrame(list(zip(titles_list, nb_ratings_list, prices_list, nb_visits_list, ratings_list)),columns=['Title', 'Nb rating', 'Prices', 'Nb visits', 'Rating'])  #creation d'une base de donnees

    print(df)  # affichage de la base
    df.to_csv(r'vegas.csv', index=False)  # converti base pandas en fichier csv


main()