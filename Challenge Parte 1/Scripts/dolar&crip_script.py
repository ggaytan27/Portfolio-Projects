#Librerias
import os
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_PHONE_NUMBER, TO_PHONE_NUMBER, APIBANX_TOKEN, FROM_PHONE_NUMBER_TEXT, TO_PHONE_NUMBER_TEXT
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

from utils import get_date, request_dolar, get_DolarForecast, message_Banx, request_cripto, get_CriptoForecast, create_dfCripto, message_Cripto, send_messagge, send_text_message

#Tipo de Cambio
#Variables
api_Banxico = APIBANX_TOKEN
datosBanx = []

#Funciones
inputDate = get_date()
responseBanxico = request_dolar(api_Banxico)
datosBanx = get_DolarForecast(responseBanxico)
messageBanx = message_Banx(datosBanx)


#Variables Criptomonedas
dataCripto = []

#Funciones
responseCripto = request_cripto()

for i in tqdm(range(len(responseCripto)), colour="green"):
    dataCripto.append(get_CriptoForecast(responseCripto, i))


dfCripto = create_dfCripto(dataCripto)
messageCripto = message_Cripto(dfCripto)


#Enviar Mensaje
message_id = send_text_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_PHONE_NUMBER_TEXT, TO_PHONE_NUMBER_TEXT, messageBanx, messageCripto)

print("Mensaje Enviado: " + str(message_id))