# -*- coding: utf-8 -*-
"""
Created on Mon May 23 10:23:32 2022

@author: kju78
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


options = Options()
options.headless = True  #etre prive
options.add_argument("--window-size=1920,1080")  #dimension fenetre
options.add_argument("start-maximized")  #mise en plein ecran de la fenetre

driver = webdriver.Chrome("C:/Users/kju78/Documents/ESME Sudria/Ingé 2/ESME Sudria - Ingé 2/Projet - Machine Learning Immobilier/Scraping/chromedriver_win32/chromedriver")  # adresse driver chrome

# =============================================================================
# Variables :
# =============================================================================

villes = ["new-york","las-vegas","boston","san-francisco","washington","chicago","los-angeles","miami","atlanta"]

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
adresses_list = []


# =============================================================================
# Scraping :
# =============================================================================

def scrapping_url (villes) :
    try :
        
        for ville in villes :
                    
            url = 'https://www.civitatis.com/fr/%s/' %(ville)
            driver.get(url)
            
            time.sleep(5)
            
            
            urls = driver.find_elements_by_xpath("//a[@class='ga-trackEvent-element _activity-link']")
            prices = driver.find_elements_by_xpath("//span[@class='comfort-card__price__text']")
            nb_visits = driver.find_elements_by_xpath("//span[@class='comfort-card__traveler-count _full']")
            
            
            for u in range(len(urls)): 
                url = urls[u].get_attribute('href')
                urls_list.append(str(url))
                
            for p in range(len(prices)):
                price = prices[p]
                prices_list.append(price.text)
                
            for nb in range(len(nb_visits)):
                nb_visit = nb_visits[nb]
                nb_visits_list.append(nb_visit.text)
            
            
            adresses_list.append(ville)
                

    except WebDriverException:
        pass
    
    return urls_list, prices_list, nb_visits_list, adresses_list

def scrapping (urls_list) :
    
    compteur = 1
    print('itérations nécessaires : ', len(urls_list)+1)
    
                   
    for url in range(len(urls_list)) : #parcours de la liste des liens recoltes
                
        
        
        try : 
            
            driver.get(urls_list[url])
            
            print('itération actuelle : ', compteur,'/',len(urls_list)+1)
            
            time.sleep(5)
            try :        
                title = driver.find_element_by_xpath("//h1[@class='a-title-activity']")
                titles_list.append(title.text)
            except NoSuchElementException :
                titles_list.append(-1)
                
            try :     
                nb_rating = driver.find_element_by_xpath("//div[@class='a-text--rating-total']/a") 
                nb_ratings_list.append(nb_rating.text)
            except NoSuchElementException :
                nb_ratings_list.append(-1)
            
                
            try :
                rating = driver.find_element_by_xpath("//div[@class='o-rating__title o-activity-header__rating__title']/a")
                ratings_list.append(rating.text)
            except NoSuchElementException :
                ratings_list.append(-1)
                
            try :
                annulation = driver.find_element_by_xpath("//div[@class='p']") 
                annulation_list.append(annulation.text)
            except NoSuchElementException :
                annulation_list.append(-1)
                
            try :            
                duration = driver.find_element_by_xpath("//li[@class='o-advantages--header__element  --important  o-advantages-icon-duration ']/a")
                durations_list.append(duration.text)    
            except NoSuchElementException :
                durations_list.append(-1)
                
            try :
                language = driver.find_element_by_xpath("//span[@class='a-feature a-feature-lang o-advantages-icon-lang']")
                languages_list.append(language.text)
            except NoSuchElementException :
                languages_list.append(-1) 
            
            compteur += 1
        
        except WebDriverException : 
            pass 
    
    return titles_list, nb_ratings_list, ratings_list, annulation_list, durations_list, languages_list
    

# =============================================================================
# Main :
# =============================================================================


def main ():
    
    urls_list, prices_list, nb_visits_list, adresses_list = scrapping_url(villes)
    titles_list, nb_ratings_list, ratings_list, annulation_list, durations_list, languages_list = scrapping(urls_list)
   
    # =============================================================================
    # Création du dataframe :
    # =============================================================================
    
    driver.close()  #fermeture de la fenetre de scraping
    
    df = pd.DataFrame(list(zip(titles_list, nb_ratings_list, prices_list, nb_visits_list, ratings_list, annulation_list, durations_list, languages_list, adresses_list)),columns=['Title', 'Nb rating', 'Prices', 'Nb visits', 'Rating', 'Annulation', 'Duration', 'Language', 'Adress'])  #creation d'une base de donnees
    
    print(df)  #affichage de la base
    df.to_csv(r'C:\Users\kju78\Documents\ESME Sudria\Ingé 2\ESME Sudria - Ingé 2\Hands on Data Tools\dataToolsBDDTest.csv',index=False)  #converti base pandas en fichier csv



main()




