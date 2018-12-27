import os

import urllib.request

from bs4 import BeautifulSoup


dirdocs="licores"
dirindex="Index"

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r

def numero_paginas(url):
    soupAux = BeautifulSoup(abrir_url(url),'html.parser')
    numeroPaginas = soupAux.find('ul',class_='pagination').find_all('li')[-2].text
    return int(numeroPaginas)

def extraer_texto_disevil():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    paginas = numero_paginas('https://www.disevil.com/tienda/es/80-licores-y-destilados/')
    categorias = [' AGUARDIENTE ',' ABSENTA ',' BRANDY ',' COGNAC ',' ARMAGNAC ',' WHYSKY ',' BOURBON ',' GINEBRA ',' RON ',' VODKA ',' TEQUILA']
    for i in range(1,paginas+1):
        soup=BeautifulSoup(abrir_url('https://www.disevil.com/tienda/es/80-licores-y-destilados/?p='+str(i)+"/"),'html.parser')
        
        for enlace in soup.find_all(class_='quick-view'):
            tupla = []
            url = enlace['href']

            soup2 = BeautifulSoup(abrir_url(url),'html.parser')
            
            producto = soup2.find(itemtype="http://schema.org/Product")
            
            titulo = " " + producto.find(itemprop="name").text + " "
            
            descripcion1 = producto.find(itemprop="description")
            if(descripcion1 !=None):
                descripcion1 = descripcion1.text
            else:
                descripcion1=""
            precio= producto.find(itemprop="price").text

            referencia= producto.find(itemprop="sku").text
            enlace=url
            
            urlImagen=producto.find(itemprop="image")['src']
            
            urlStock = producto.find(itemprop="availability")
            if urlStock != None:
                urlStock = urlStock['href']
                
            enStock = True
            
            if(urlStock != 'http://schema.org/InStock'):
                enStock= False
                
            categoria = None
            for cat in categorias:
                if cat in titulo:
                    categoria=cat
                    break
            if(categoria== None):
                if ' GIN ' in titulo:
                    categoria = ' GINEBRA '
                else:
                    categoria='OTROS LICORES'        
 
            descripcion2 = producto.find(class_='page-product-box').text
             
            if "Bot" in descripcion2:
                volumen =  descripcion2.split('Bot')[1]
                volumen = volumen.replace(" ","")
                volumen = volumen.replace(".","")
            
                volumen = volumen.upper()
        
                volumen = volumen.split("º")[0]
                volumen = volumen.replace("CL", "CLKKK")
                volumen = volumen.replace("1L","1LKKK")
                volumen = volumen.split("KKK")[0]
           
                if volumen.strip() == "0":
                    volumen = "70CL"
                    
            else:
                volumen = "70CL"
            volumen = volumen.replace(" ","")
            volumen = volumen.replace("070","70")
            
            if "Bot" in descripcion2:
                graduacion= descripcion2.split('Bot')[1]
                graduacion = graduacion.upper()
                graduacion = graduacion.replace("º","ºKKK")
                graduacion = graduacion.replace("CL","CL.")
                graduacion = graduacion.replace("CL..","CL.")
                graduacion = graduacion.replace(" ","")
                graduacion = graduacion.replace("L","L.")
                graduacion = graduacion.replace("L..","L.")
                graduacion = graduacion.split("KKK")[0]
                graduacion = graduacion.split("L")[1]
                graduacion = graduacion.split(".")[1]
                graduacion = graduacion.replace(" ","")
                if("º" not in graduacion):
                    graduacion = str(graduacion) +"º"
            
                graduacion = graduacion.replace(" ","")   
            else:
                graduacion = "Sin determinar"
            
            origen= descripcion2.splitlines()[1]
            if "Más" in origen:
                origen = descripcion2.splitlines()[2]
                origen = origen.split("Origen")[1]
                origen = origen.replace(":","")
            
            if origen == "":
                origen = "Sin determinar"
            
            origen = origen.replace(" ","")
            origen = origen.replace(".","")
            if len(origen) > 30:
                origen ="Sin determinar"
        
            descripcion = descripcion1 + descripcion2
            tupla = (referencia,titulo,descripcion,precio,origen,categoria,volumen,graduacion,url,enStock,urlImagen)
            print(tupla)
        
if __name__ == '__main__':
    
    extraer_texto_disevil()
    
    