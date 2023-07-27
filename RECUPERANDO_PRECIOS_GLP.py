from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

url = 'https://www.facilito.gob.pe/facilito/pages/facilito/menuPrecios.jsp'
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
driver = webdriver.Chrome(options=option)
driver.maximize_window()
driver.get(url)


### HACER CLICK EN BOTON GLP ENVASADO
while True:
    try:
        xpath = '//*[@id="icon-boxes"]/div/div/div[4]/div/h4/a'
        
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
        pass


### HACER CLICK EN EL BOTON LOCALES DE VENTA
while True:
    try:
        ### Identificando el XPATH del boton locales de venta
        xpath = '//*[@id="services"]/div/div[2]/div[1]/div/h4/a'
        ### Instanciamos el boton
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                            By.XPATH, xpath)))
        ### Hacemos click al boton
        button.click()
        sleep(3)
        print("Entramos al siguiente nivel de manera exitosa")
        break
    except:
        print("Error en recuperacion... volviendo a ingresar")
        pass
        

driver.close()
#%%
