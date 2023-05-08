#Librerias
import os
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI, TO_PHONE_NUMBER
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime


def weather_request(c, ak):
    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+ak+'&q='+c+'&days=2&aqi=no&alerts=no'
    response = requests.get(url_clima).json()
    return response


def get_forecast(response):
    date = response['forecast']['forecastday'][0]['date']
    minTemp = response['forecast']['forecastday'][0]['day']['mintemp_c']
    maxTemp = response['forecast']['forecastday'][0]['day']['maxtemp_c']
    avgTemp = response['forecast']['forecastday'][0]['day']['avgtemp_c']
    chanceOfRain = response['forecast']['forecastday'][0]['day']['daily_chance_of_rain']     

    messageWeather = "Hola Admin, este es el pronostico del clima para el dia de hoy: {}\n * Temperatura Minima: {} °C\n * Temperatura Maxima: {} °C\n * Temperatura Promedio: {} °C \n * Posibilidad de Lluvia: {}%".format(date, minTemp, maxTemp, avgTemp, chanceOfRain)

    return messageWeather

def send_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, TO_PHONE_NUMBER, msg):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
   
    error = ""

    try:    
        message = client.messages.create(
            body= "\n"+msg,
            from_=PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )

    except Exception as e:
        print(e)
        error = str(e)
    
    
    if error =="":
        response = message.sid
    else:
        response = "View Log"
 

    return response
