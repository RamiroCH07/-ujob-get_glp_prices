from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Paquete para reconocimiento de elemento "DROP DOWN"
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd

# FUNCION PARA HACER CLICK A UN BOTON 
url = 'https://www.facilito.gob.pe/facilito/pages/facilito/menuPrecios.jsp'
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
driver = webdriver.Chrome(options=option)
driver.maximize_window()
driver.get(url)
def click(xpath):
    while True:
        try:
            ### Instanciamos el boton
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                                By.XPATH, xpath)))
            
            ### Hacer click al boton
            button.click()
            sleep(3)
            print("Entramos al siguiente nivel de manera exitosa")
            break
        except:
            print("Error en recuperacion... volviendo a ingresar")
            print(xpath)
            sleep(20)
            pass
def select_dropdown(xpath,value):
    while True:
        try:
            ## IDENTIFICACIÓN DEL OBJETO DROPDOWN
            dropdown = Select(driver.find_element(By.XPATH,xpath))
            ## SELECCIOAMOS EL DEPARTAMENTO Y ACCEDEMOS AHI
            dropdown.select_by_visible_text(value)
            sleep(3)
            print("Entramos al siguiente nivel de manera exitosa")
            break
        except:
            print("Error en recuperacion... volviendo a ingresar")
            print(xpath)
            sleep(20)
            pass

def GET_DATA_FROM_PAGE(trs):
    df = pd.DataFrame(columns = ['Distrito','Marca','Establecimiento',
                                 'Direccion','Telefono','Precio_Venta'])
    for tr in trs:
        df.loc[df.shape[0]] = tr.get_text().strip().split('\n')
        
    return df


def exist_data(tr_text):
    if len(tr_text.strip().split('\n')) > 1 :
        return True 
    else :
        return False

### ESTA FUNCION PERMITE LLEGAR A LA PAGINA DONDE SE RECOPILARAN LOS DATOS    
def FIRST_TIME():
    ##
    #CLICK EN BOTON GLP ENVASADO
    click('//*[@id="icon-boxes"]/div/div/div[4]/div/h4/a')

    ###CLICK EN EL BOTON LOCALES DE VENTA
    click('//*[@id="services"]/div/div[2]/div[1]/div/h4/a')
            
    ### REALIZAMOS CAMBIO DE TAMAÑO DE LA PAGINSA
    driver.set_window_size(600, 600)
    select_dropdown('//*[@id="departmento"]', 'AMAZONAS')
    driver.maximize_window()
    ### SELECCIONARMOS 50 EN EL DROPDOWN
    

      
def GET_DATA_FROM_PROVINCE(dep,prov):
    #SELECCIONAMOS EL DEPORTAMENTO EN CUESTION
    select_dropdown('//*[@id="contact"]/div/div[1]/div/div[1]/select', dep)
    #SELECCIONAMOS LA PROVINCIA EN CUESTION
    select_dropdown('//*[@id="contact"]/div/div[1]/div/div[2]/select', prov)
    ### SELECCIONARMOS 50 EN EL DROPDOWN
    select_dropdown('//*[@id="tblPreciosAGranelGlp_length"]/label/select', '50')
    ### RECUPERAMOS EL ELEMENTO HTML
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    soup = bs(source,'html.parser')
    # Recuperamos el contenido de la etiqueta tabla
    table = soup.find('table',id = 'tblPreciosAGranelGlp')
    body = table.find('tbody')
    trs = body.find_all('tr')
    df = pd.DataFrame(columns = ['Distrito','Marca','Establecimiento',
                                 'Direccion','Telefono','Precio_Venta'])
    if exist_data(trs[0].get_text()):
        ### SE COMPRUEBA EL NUMERO DE FRAMES 
        frames = soup.find('div', id = 'tblPreciosAGranelGlp_paginate')
        num_frames = len(frames.find_all('a'))
        for i in range(1,num_frames+1):
            ### identificamos el elemento ui boton del 2
            xpath = f'//*[@id="tblPreciosAGranelGlp_paginate"]/span/a[{i}]'
            click(xpath) 
            body = driver.execute_script("return document.body")
            source = body.get_attribute('innerHTML')
            soup = bs(source,'html.parser')
            table = soup.find('table',id = 'tblPreciosAGranelGlp')
            body = table.find('tbody')
            trs = body.find_all('tr')
            df = pd.concat([df,GET_DATA_FROM_PAGE(trs)])
    return df
    

FIRST_TIME()
df = pd.DataFrame(columns = ['Distrito','Marca','Establecimiento',
                             'Direccion','Telefono','Precio_Venta'])
deps = {
    'CUSCO':[
        'ACOMAYO',
        'ANTA',
        'CALCA',
        'CANAS',
        'CANCHIS',
        'CHUMBIVILCAS',
        'CUSCO',
        'ESPINAR',
        'LA CONVENCION',
        'PARURO',
        'PAUCARTAMBO',
        'QUISPICANCHI',
        'URUBAMBA'
        ],
    'AREQUIPA':[
        'AREQUIPA',
        'CAMANA',
        'CARAVELI',
        'CASTILLA',
        'CAYLLOMA',
        'CONDESUYOS',
        'ISLAY',
        'LA UNION'
        ]}
for dep,provs in deps.items():
    for prov in provs:
        df = pd.concat([df,GET_DATA_FROM_PROVINCE(dep,prov)])






                  
                  
