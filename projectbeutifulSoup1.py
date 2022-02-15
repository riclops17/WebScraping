rom bs4 import BeautifulSoup
import requests
website = 'https://subslikescript.com/movie/Titanic-120338'
result = requests.get(website) #enviamos solicitud a la pagina , nos devuelve un response
#obtener el texto de un elemento en beutiful soup
content = result.text
#variable soup nos permite localizar elementos/ definimos el parser
soup = BeautifulSoup(content,'lxml')
#prettify desplega el html para visualizarlo mejor
# print(soup.prettify())
#buscar elementos
#elemento raiz = main article
box = soup.find('article',class_ = 'main-article')
#obtenemos el nombre de la pelicula dentro del elemento h1 y reemplazamos soup por box para excluir elementos
title =box.find('h1').get_text()
#print(title)
transcript = soup.find('div',class_ ='full-script').get_text(strip = True, separator= ' ')#borra espacios en blanco al inicio y al final
#print(transcript)
#crear un archivo en modo de escritura
#cadena f cadenas regulares que podemos escribir variables dentro de {}
with open(f'{title}.txt','w') as file:
    file.write(transcript)
