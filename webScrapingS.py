from selenium import webdriver
#seleccionar valores dentro de una lista despleglable
from selenium.webdriver.support.ui import Select
import pandas as pd
website = 'https://www.adamchoi.co.uk/teamgoals/detailed'
path = '/Users/rickybauch/Downloads/chromedriver'

# driver , abrir pagina automaticamente
driver = webdriver.Chrome(path)
driver.get(website)
print('hola')
# este metodo tiende a fallar
# all_matches_button = driver.find_element_by_xpath('//*[@id="page-wrapper"]/div/home-away-selector/div/div/div/div/label[2]')
# buscar xpath relativo (referencia al atributo name analytics-event / tag name en el *
# buscar nodo como nombre de tag = label y dentro de este nodo busca un atributo que tenga
# nombre analytics-event y como texto all matches

all_matches_button = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
all_matches_button.click()

dropdown = Select(driver.find_element_by_id('country'))
dropdown.select_by_visible_text('Spain')

# buscar filas por nombre de tag / extraigo una lista de elementos

matches = driver.find_elements_by_tag_name('tr')
print('hola2')
# extraemos los datos de la lista y guardamos los valores en una lista
partidos = []
for match in matches:
    partidos.append(match.text)

driver.quit()
print('hola3')
#creamos un data frame
df = pd.DataFrame({'partidos':partidos})
print(df)
# index = false para que no se pasen en el csv
# TENGO QUE TRABAJAR CON EXPRESIONES REGULARES PARA ARREGLAR EL CSV
df.to_csv('partidos.csv',index=False)
