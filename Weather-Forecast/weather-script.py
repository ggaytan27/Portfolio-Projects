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
from utils import weather_request, get_forecast, send_message


ciudad = 'Ciudad Juarez'
apiKey = API_KEY_WAPI
#Weather Response
weatherResponse = weather_request(ciudad, apiKey)
weatherMessage = get_forecast(weatherResponse)
message_id = send_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, TO_PHONE_NUMBER, weatherMessage)
print("Mensaje Enviado "+str(message_id))


