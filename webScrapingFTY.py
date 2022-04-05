from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo  import MongoClient, UpdateOne
from datetime import datetime
import time

def insert_bulk(lista_crawler, collection):
    with MongoClient('127.0.0.1', 37017) as cliente:
        db = cliente.scraping_bb

        result = db[collection].bulk_write(lista_crawler)
        bulk_api_result = result.bulk_api_result
        print(f''
              f'Insert: {bulk_api_result["nUpserted"]} - '
              f'Matched:  {bulk_api_result["nMatched"]} - '
              f'Modified: {bulk_api_result["nModified"]}'
              )

path = '/Users/rickybauch/Downloads/chromedriver'
driver = webdriver.Chrome(path)
baseUrl = 'https://www.filmaffinity.com/es/countcat.php?id=apple_tv_plus'
'''driver.get(baseUrl)
print('PASO 1 CRAWLER ')
contenidos = driver.find_elements(By.CLASS_NAME, "top-movie")
now = datetime.now()
date = now.strftime("%Y-%m-%d")
lista_crawler = []
movieLinks= []
for contenido in contenidos:
    title = contenido.find_element(By.TAG_NAME, "h3")
    print(title.text)
    title2 = title.text
    url = title.find_element(By.TAG_NAME, "a").get_attribute('href')
    print(url)
    url2 = url.split('film')[2]
    regex = re.compile('[^0-9]')

    print(url2)



    item = {
        "PlatformCode": "fty",
        "Title": title2,
        "URL": url,
        "ContentId": url2,
        "CreatedAt": date
    }
    query = {
        "PlatformCode": "fty",
        "ContentId": url2,
        "CreatedAt": date
    }
    lista_crawler.append(
        UpdateOne(
            query,
            {
                "$set": item
            },
            upsert=True
        )
    )



print(len(lista_crawler))
insert_bulk(lista_crawler, 'Prueba2')
'''
listaScraping= []
print('PARTE 2 SCRAPING')
testlink ='https://www.filmaffinity.com/es/film480371.html'
driver.get(testlink)
titulo = driver.find_element(By.XPATH,"//*[@id='left-column']/dl[1]/dd[1]")
titulo2 = titulo.text
print(titulo.text)
pais =driver.find_element(By.XPATH,"//*[@id='left-column']/dl[1]/dd[4]")
pais2 =pais.text.strip()
print(pais2)
rating = driver.find_element(By.XPATH,"//*[@id='movie-count-rat']/span")
print(rating.text)
ratAvg = driver.find_element(By.ID,"movie-rat-avg")
print(ratAvg.text)
metaData = {
            "PlatformCode": "ybt",
            "Title": titulo2,
            "Country": pais2,
            "Rating": rating.text,
            "RatingAvg":ratAvg.text,

            }


#comentarios
botonCritic = driver.find_element(By.PARTIAL_LINK_TEXT, 'Críticas')
driver.execute_script("arguments[0].click();", botonCritic)
time.sleep(2)
paginas = driver.find_element(By.XPATH,"//*[@id='mt-content-cell']/div[5]/div[3]/div/a[6]")
print(paginas.text)
p = int(paginas.text)
listaComentario = []
for i in range(1,p):
    contents = driver.find_elements(By.CLASS_NAME,"fa-shadow.movie-review-wrapper.rw-item")
    for content in contents:
        tituloCritica = content.find_element(By.CLASS_NAME, "review-title")
        print(tituloCritica.text)
        user = content.find_elements(By.TAG_NAME, "a")
        print(user[0].text)
        print(user[1].text)
        location = content.find_element(By.XPATH,"//*[@id='mt-content-cell']/div[5]/div[4]/div[1]/div[1]/div[3]/div[2]/i")
        print(location.text)
        criticText = content.find_element(By.CLASS_NAME,"review-text1")
        print(criticText.text)
        comments ={
            "tituloCritica": tituloCritica,
            "user": user[1].text,
            "location":location,
            "criticText":criticText
            }
        listaComentario.append(comments)
    if i != p:
        botonNext = driver.find_element(By.PARTIAL_LINK_TEXT, '>>')
        driver.execute_script("arguments[0].click();", botonNext)
        time.sleep(2)

