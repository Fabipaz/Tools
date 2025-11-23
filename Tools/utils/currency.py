import requests
from bs4 import BeautifulSoup

def obtener_tasa_cambio(moneda_base, moneda_destino):
    url = f'https://www.google.com/finance/quote/{moneda_base}-{moneda_destino}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tasa_element = soup.find('div', class_='YMlKec fxKbKc')
            
            if tasa_element:
                tasa_cambio = float(tasa_element.text.replace(',', ''))
                return tasa_cambio
            else:
                return(f'No se pudo encontrar la tasa de cambio para {moneda_base}-{moneda_destino} en la página.')
                
    except requests.RequestException as e:
            return(f'Error al obtener la tasa de cambio para {moneda_base}-{moneda_destino}')
