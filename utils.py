import os
import smtplib
import threading
import webbrowser
from email.message import EmailMessage
from urllib.parse import quote_plus
import requests

_speech_lock = threading.Lock()
def speak(text):
    # Create/use the SAPI engine on the worker thread, never the UI thread.
    with _speech_lock:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 185)
            engine.setProperty('volume', 1.0)
            engine.say(str(text)); engine.runAndWait(); engine.stop()
        except Exception as exc:
            print('Speech unavailable:', exc)

def request_json(url, **kwargs):
    response = requests.get(url, timeout=20, **kwargs)
    response.raise_for_status()
    return response.json()

def find_my_ip():
    return request_json('https://api64.ipify.org?format=json')['ip']
def search_on_google(query):
    webbrowser.open('https://www.google.com/search?q=' + quote_plus(query))
def youtube(query):
    webbrowser.open('https://www.youtube.com/results?search_query=' + quote_plus(query))
def search_on_wikipedia(query):
    import wikipedia
    return wikipedia.summary(query, sentences=2)
def get_news():
    key = os.getenv('NEWS_FETCH_API_KEY')
    if not key: raise ValueError('Set NEWS_FETCH_API_KEY in .env to use news.')
    data = request_json('https://newsapi.org/v2/top-headlines', params={'country': os.getenv('NEWS_COUNTRY','us'), 'apiKey':key})
    if data.get('status') != 'ok': raise ValueError(data.get('message','News service error'))
    return [a['title'] for a in data.get('articles',[])[:6]]
def weather_forecast(city):
    key = os.getenv('WEATHER_FORECAST_API_KEY')
    if not key: raise ValueError('Set WEATHER_FORECAST_API_KEY in .env to use weather.')
    data = request_json('https://api.openweathermap.org/data/2.5/weather', params={'q':city,'appid':key,'units':'metric'})
    return data['weather'][0]['description'], str(data['main']['temp'])+' C', str(data['main']['feels_like'])+' C'
def send_email(receiver_add, subject, message):
    sender = os.getenv('EMAIL'); password = os.getenv('PASSWORD')
    if not sender or not password: raise ValueError('Configure EMAIL and PASSWORD (an app password) in .env.')
    email = EmailMessage(); email['From']=sender; email['To']=receiver_add; email['Subject']=subject
    email.set_content(message)
    with smtplib.SMTP(os.getenv('SMTP_URL','smtp.gmail.com'), int(os.getenv('SMTP_PORT','587')), timeout=20) as server:
        server.starttls(); server.login(sender,password); server.send_message(email)
    return True
