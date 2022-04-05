from bs4 import BeautifulSoup
from pymongo  import MongoClient, UpdateOne
from datetime import datetime
import requests

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
lista_scraping = []
lista_crawler = []
baseUrl = 'https://yourbittorrent.com{}'
for x in "abcd":
    print(x)
    base = f'https://yourbittorrent.com/movies/{x}.html'
    base2 = f'https://yourbittorrent.com/television/{x}.html'
    r = requests.get(base2)
    soup = BeautifulSoup(r.content, 'lxml')
    movieList = soup.find_all('tr',class_ = 'table-default')
    print('PARTE1')

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    for item in movieList:

        try:

            title = item.a.text
            print(title)
            link = item.find('a')['href']
            print(link)
            url = baseUrl.format(link)
            print(url)

            item = {
                "PlatformCode": "ybt",
                "Title": title,
                "URL": url,
                "ContentId": link.split('/')[2],
                "CreatedAt": date
            }
            query = {
                "PlatformCode": "ybt",
                "ContentId": link.split('/')[2],
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
        except AttributeError:
            print(AttributeError)
            print('ACA ESTOY EN EXCEPCION')








print(len(lista_crawler))
print('PARTE 4')
insert_bulk(lista_crawler, 'Prueba')
print('PARTE 5')
print('--------------------------------------------------------------------------')
with MongoClient('127.0.0.1', 37017) as cliente:
    db = cliente.scraping_bb

    items = list(db['Prueba'].find(
        {
            "PlatformCode": "ybt",
            "CreatedAt": date,
            "Error": {"$exists": False}
        },
        {
            "_id": 0
        }
    ))

for i in items:
    print(i['URL'])

testLink = 'https://yourbittorrent.com/torrent/38101719/a-day-to-die-2022-1080p-webrip-5-1-yts-mx.html'
for item in items:
    query = {
        "PlatformCode": item['PlatformCode'],
        "ContentId": item['ContentId'],
        "CreatedAt": item['CreatedAt']
    }
    item['Timestamp'] = datetime.now()

    r = requests.get(item['URL'])
    print(item['URL'], r.status_code)
    if r.status_code == 200:

        soup = BeautifulSoup(r.content, 'lxml')
        name = soup.find('h3',class_='card-title').text.strip()
        category = soup.find('a',href='/movies.html').getText().strip()
        submiter = soup.find('a',class_='text-default').getText()
        seeder = soup.find('div',class_='col sd').getText()
        leechers = soup.find('div',class_='col pr').getText()
        columnas = soup.find_all('div',class_='col')
        torrent = soup.find_all('div',class_='col-md-4 text-center')
        trr = []
        '''    for t in torrent:
            trr.append(t.find('a')['href'])
            torrentURl = trr[1]'''


        arr = []
        for col in columnas:
            print(col)
            arr.append(col)
        content = arr[1].getText()
        print('AAAAAAAAAAAAAA')
        print(content)
        dateUpload =arr[2].getText()
        size = arr[6].getText()

        metaData = {
                            "PlatformCode": "ybt",
                            "name": name,
                            "category": category,
                            "dateUpload": dateUpload,
                            "seeder": seeder,
                            "leechers":leechers,
                            "size": size,

                    }
        lista_scraping.append(
                            UpdateOne(
                                query,
                                {
                                    "$set": metaData
                                },
                                upsert=True
                            )
                        )
insert_bulk(lista_scraping, 'Prueba2')

