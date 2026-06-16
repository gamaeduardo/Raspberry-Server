# source venv/bin/activate

from fastapi import FastAPI
import requests
import random
from deep_translator import GoogleTranslator

app = FastAPI()

# Teste
def fetchDataRick(endpoint, filters={}):
    url = f"https://rickandmortyapi.com/api/{endpoint}"
    response = requests.get(url, params=filters)

    return response.json() if response.status_code == 200 else None



# Tadução com o Google Translator
def translate(text):
    translated = GoogleTranslator(source='auto', target='en').translate(text)

    return translated


# Enviar Notificação
def sendNotification(message):
    envio = requests.post("https://ntfy.sh/gamma_morse_pico_w_8392x_receptor",data=message)
    return "Mensagem enviada" if envio.status_code == 200 else "Erro ao enviar"


# Dado
def randomNumber(min, max):
    numero = random.randint(min,max)

    return str(numero)



# GeckoCripto API
def criptocurrency(currency):
    API_KEY = "CG-wGn2iUDpcfF5wnCQZQnyyGtZ"
    url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=brl&symbols={currency}&x_cg_demo_api_key={API_KEY}"
    response = requests.get(url)
    valorMoeda = response.json()
    try:
        mensagem = f"{currency.upper()} = R${str(valorMoeda[currency]['brl'])}" if response.status_code == 200 else "Erro ao procurar moeda"
    except:
        mensagem = "Moeda não encontrada"

    return mensagem



# OpenWeatherMap API
def fetchDataCoordWeather(api, city):
    cityCord = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api}"
    response = requests.get(cityCord)
    result = response.json()
    lat = result[0]['lat']
    lon = result[0]['lon']
    return lat, lon

def fetchDataWeather(endpoint):
    API_KEY = "8c96901fbda8bc56c883962a822a1863"

    lat, lon = fetchDataCoordWeather(API_KEY, endpoint)
    
    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)

    return response.json() if response.status_code == 200 else None

def weather(city):
    weatherData = fetchDataWeather(city)

    pais = weatherData['sys']['country']

    temperatura = weatherData['main']['temp']
    tempMin = weatherData['main']['temp_min']
    tempMax = weatherData['main']['temp_max']
    sensacaoTerm = weatherData['main']['feels_like']
    umidade = weatherData['main']['humidity']

    return f"{city.capitalize()}- {pais}\n\n-Temperatura Atual: {temperatura}°C\n-Temperatura Min: {tempMin}°C\n-Temperatura Max: {tempMax}°C\n-Sensação Term: {sensacaoTerm}°C\n-Umidade: {umidade}%"


# message = fetch_data_rick("character", {'name': 'Rick'})

@app.get("/")
def receiveMessage(messagePico: str = ""):

    if not messagePico:
        return "Nenhum comando recebido"

    raspInput = messagePico.split()
    command = raspInput[0]
    message = ""

    match command.lower():
        case "clima":
            city = ""
            cont = 0
            for i in raspInput:
                if cont > 0:
                    city += f"{i} "
                cont += 1

            message = weather(city)

        case "traduzir":
            text = ""
            cont = 0
            for i in raspInput:
                if cont > 0:
                    text += f"{i} "
                cont += 1

            message = translate(text)

        case "msg":
            text = ""
            cont = 0
            for i in raspInput:
                if cont > 0:
                    text += f"{i} "
                cont += 1

            message = sendNotification(text)

        case "cripto":
            currency = raspInput[1]

            message = criptocurrency(currency)

        case "dado":
            min = int(raspInput[1])
            max = int(raspInput[2])

            message = randomNumber(min, max)

        case _:
            print("erro")

    return message