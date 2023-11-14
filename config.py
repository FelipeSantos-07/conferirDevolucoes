# CONFIG.PY -> MÓDULO COM O OBJETO
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

options = Options()
options.headless = True # Para visualizar o que está acontecendo (oculto ou não)

navegador = webdriver.Firefox(options=options)
sleep(3)

linkSite = "https://erp.tiny.com.br/login/"

navegador.get(url=linkSite)
sleep(1)