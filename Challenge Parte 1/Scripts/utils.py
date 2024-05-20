#Librerias
import os
from twilio.rest import Client
import datetime
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime


#Tpo de Cambio
def get_date():
    today = datetime.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    fecha = year +'-'+month+'-'+day

    return fecha

def request_dolar(apiBanx):
    url_banxico = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43787,SF43784/datos/oportuno?token='+apiBanx

    try:
        responseBanx = requests.get(url_banxico).json()
    except Exception as e:
        print(e)
    
    return responseBanx

def get_DolarForecast(responseBanx):
    #Venta
    fechaVenta = responseBanx['bmx']['series'][0]['datos'][0]['fecha']
    precioVenta = responseBanx['bmx']['series'][0]['datos'][0]['dato']

    #Compra
    fechaCompra = responseBanx['bmx']['series'][1]['datos'][0]['fecha']
    precioCompra = responseBanx['bmx']['series'][1]['datos'][0]['dato']

    return fechaVenta, precioVenta, fechaCompra, precioCompra

def message_Banx(datos):
    mensaje = "\nInformacion sobre tipo de Cambio:\nFecha Venta: {}\nValor: ${}\nFecha Compra: {}\nValor: ${}".format(datos[0], datos[1], datos[2], datos[3])

    return mensaje


#Cripto Monedas
def request_cripto():
    urlCriptos = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'

    try:
        responseCripto = requests.get(urlCriptos).json()
    except Exception as e:
        print(e)
    
    return responseCripto

def get_CriptoForecast(responseCripto, i):
    nombreCripto = responseCripto[i]['name']
    precioCripto = round(responseCripto[i]['current_price'], 2)
    rankingCripto = responseCripto[i]['market_cap_rank']

    return nombreCripto, precioCripto, rankingCripto    


def create_dfCripto(data):
    col = ['Moneda', 'Precio (USD)', 'Ranking']
    dfCripto = pd.DataFrame(data, columns=col)

    dfCriptoFinal = dfCripto[dfCripto['Ranking']<=10]

    return dfCriptoFinal    
    

def message_Cripto(datos):
    mensajeCripto = "Resumen de las cripto:\n" + datos.to_string(index=False)

    return mensajeCripto


def send_messagge(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_PHONE_NUMBER, TO_PHONE_NUMBER, msgBanx, msgCripto):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    fromWhatsAppNumber = FROM_PHONE_NUMBER
    whatsappNumber = TO_PHONE_NUMBER

    error = ""

    try:
        message = client.messages.create(
                            from_=fromWhatsAppNumber,
                            body=msgBanx + "\n" + "\n"+ msgCripto,
                            to=whatsappNumber)   
    except Exception as e:
        print(e)
        error = e

    if error =="":
        response = message.sid
    else:
        response = "View Log"
 

    return response

def send_text_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_PHONE_NUMBER_TEXT, TO_PHONE_NUMBER, msgBanx, msgCripto):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    number = TO_PHONE_NUMBER
   
    error = ""

    try:    
        message = client.messages.create(
            body= msgBanx + "\n\n"+msgCripto,
            from_=FROM_PHONE_NUMBER_TEXT,
            to=number
        )

    except Exception as e:
        print(e)
        error = str(e)
    
    
    if error =="":
        response = message.sid
    else:
        response = "View Log"
 

    return response