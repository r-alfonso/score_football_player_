## Librerias
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import csv
import time

## Criterios de la búsqueda:
url_home = 'http://www.futbol360.com.ar/'
football_player = 'lionel messi'
#### Si se encuentra más de un jugador con el mismo nombre se tomara el primer resultado de la busqueda.
#### Generalmente según las pruebas realizadas el primer resultado refiere al jugador más popular.
#### Si desea una búsqueda más precisa puede incluir otros criterios como el de país y/o equipo.

split_name = football_player.split(' ')
reverse_split_name = split_name[::-1]
football_player_2 = ' '.join(reverse_split_name)
no_match = ''.join('Mostrando 0 coincidencias para: '+football_player)
no_match_2 = ''.join('Mostrando 0 coincidencias para: '+football_player_2)
####Esta combinación de nombres se hace necesaria dada las limitaciones del buscador de la página seleccionada.

## Driver Web
driver = webdriver.Chrome('./chromedriver.exe')
#### El driver puedes descargarlo desde acá:
#### https://sites.google.com/a/chromium.org/chromedriver/downloads
#### Si no deseas modificar la linea de codigo anterior, debes guardar el ejecutable en la misma carperta del proyecto.

## Conexión con la web y busqueda de las estadísticas del jugador:
driver.get(url_home)
time.sleep(3)
driver.find_element_by_css_selector('#header > div > form > input.input').send_keys(football_player)
driver.find_element_by_css_selector('#header > div > form > input.button').click()
time.sleep(3)
match_search = driver.find_element_by_css_selector('#column522 > div > p')
match = match_search.text

if match != no_match:
    driver.find_element_by_css_selector('#column190 > ul > li:nth-child(4) > a').click()
    time.sleep(2)
    url_player = driver.find_element_by_css_selector('#column522 > div > div > h3 > a').click()
    url_table = driver.current_url
    table = pd.read_html(url_table, header = 0)[1]
    player_statistics = table.assign(Player = football_player)
    player_statistics.to_csv(''.join(football_player+'_statistics.csv'),index = False)
    driver.quit()
    print ('Listo el pollo')

else:
    driver.get(url_home)
    driver.find_element_by_css_selector('#header > div > form > input.input').send_keys(football_player_2)
    driver.find_element_by_css_selector('#header > div > form > input.button').click()
    time.sleep(3)
    match_search_2 = driver.find_element_by_css_selector('#column522 > div > p')
    match_2 = match_search_2.text
    if match_2 != no_match_2:
        driver.find_element_by_css_selector('#column190 > ul > li:nth-child(4) > a').click()
        time.sleep(2)
        url_player = driver.find_element_by_css_selector('#column522 > div > div > h3 > a').click()
        url_table = driver.current_url
        table = pd.read_html(url_table, header = 0)[1]
        player_statistics = table.assign(Player = football_player_2)
        player_statistics.to_csv(''.join(football_player_2+'_statistics.csv'),index = False)
        driver.quit()
        print ('Listo el pollo')
    else:
        print('No se encontraron resultados, intente con otro jugador')
