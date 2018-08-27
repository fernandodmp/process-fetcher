from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from celery import shared_task
import re
import os
import pandas as pd

@shared_task
def tribunal_crawler(url, process_num):
    """
    The selenium crawler responsible to access the tribunal interface and query about the entered process number and fetch it's data
    """

    #Telling pandas to not truncate the content of the dataframe
    pd.set_option('display.max_colwidth', -1)

    #Spliting the given process number to adjust it for the tribunal interface
    process_num_parts = process_num.split('.', )

    #Web-Driver Settings and Initialization
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)

    #Navigation on the web-page until the page gets ready for data extraction
    try:
        #Looking fot the form fields and entering the process number
        field_1 = driver.find_element_by_id('numeroDigitoAnoUnificado') 
        field_1.send_keys(process_num_parts[0] + process_num_parts[1])
        field_2 = driver.find_element_by_id('foroNumeroUnificado')
        field_2.send_keys(process_num_parts[4])
        #Submiting the form
        form_button = driver.find_element_by_id('pbEnviar')
        form_button.click()
        #Fully opening the hidden info
        all_parts = driver.find_element_by_id('linkpartes')
        all_parts.click()
        all_moves = driver.find_element_by_id('linkmovimentacoes')
        all_moves.click()

        #Creating the bs4 html parser as it's faster than selenium's
        page = BeautifulSoup(driver.page_source, 'html.parser')

        #Fetching the process information with selenium and adjusting it's format with pandas
        dados_processo = driver.find_element_by_xpath("/html/body/div/table[4]/tbody/tr/td/div[1]").get_attribute('innerHTML')
        dados_processo = pd.concat(pd.read_html(dados_processo))
        dados_processo.drop(2, axis = 1, inplace = True)
        dados_processo.dropna(inplace = True)

        #Fetching the interested parts section and transforming it to a pandas dataframe
        partes_interessadas = page.find('table', {"id": "tableTodasPartes"})
        partes_interessadas = pd.read_html(str(partes_interessadas))[0]

        #Fetching the process transactions section, transforming it to a pandas dataframe and adjusting
        movimentacoes = page.find("tbody", {'id': 'tabelaTodasMovimentacoes'}).parent
        movimentacoes = pd.read_html(str(movimentacoes))[0].drop("Unnamed: 1", axis = 1)

        #Returning the fetched data as html strings
        return [dados_processo.to_html(header = False, index = False), 
            partes_interessadas.to_html(header = False, index = False), 
            movimentacoes.to_html(index = False,  justify = 'left')]

    except:
        driver.quit()
        return None

    finally:
        driver.quit()