import os
import subprocess
import webbrowser
from datetime import datetime
from urllib.parse import quote_plus
import requests
from constants import USER, GEMINI_API_KEY, GEMINI_MODEL
from utils import find_my_ip, youtube, search_on_google, search_on_wikipedia, get_news, weather_forecast

HELP = "Commands: time; date; open notepad; open command prompt; open camera; open discord; open gta; ip address; youtube <search>; search on google <search>; search on wikipedia <topic>; weather <city>; tell me news; movie <title>. Other text goes to Gemini when configured. Email uses the Email button."
def handle(query):
    query = query.strip(); low = query.lower()
    if not query: return 'Type a command or click Listen.'
    if low in ('help','commands'): return HELP
    if low in ('time','what time is it'): return datetime.now().strftime('It is %I:%M %p.')
    if low in ('date','what is the date'): return datetime.now().strftime('%A, %B %d, %Y')
    if 'how are you' in low: return f'I am ready to help, {USER}.'
    apps={'open notepad':['notepad.exe'], 'open command prompt':['cmd.exe']}
    if low in apps:
        if os.name != 'nt': return 'This command requires Windows.'
        subprocess.Popen(apps[low]); return 'Opened ' + low[5:] + '.'
    if low == 'open camera':
        if os.name != 'nt': return 'This command requires Windows.'
        os.startfile('microsoft.windows.camera:'); return 'Opened Camera.'
    if low in ('open discord','open gta'):
        key = 'DISCORD_PATH' if low.endswith('discord') else 'GTA_PATH'
        path = os.getenv(key,'')
        if not path or not os.path.isfile(path): return f'Set {key} in .env to the executable on your PC.'
        os.startfile(path); return 'Opened ' + low[5:] + '.'
    if 'ip address' in low: return 'Your public IP address is ' + find_my_ip()
    for prefix, action in [('search on google',search_on_google),('open google',search_on_google),('youtube',youtube),('open youtube',youtube),('search on wikipedia',search_on_wikipedia),('wikipedia',search_on_wikipedia)]:
        if low == prefix or low.startswith(prefix+' '):
            term=query[len(prefix):].strip()
            if not term: return f'Please type {prefix} followed by a search topic.'
            result=action(term); return result or 'Opened search results for ' + term + '.'
    if low == 'weather' or low.startswith('weather '):
        city=query[7:].strip()
        if not city: return 'Type weather followed by a city, for example weather Spokane.'
        desc,temp,feels=weather_forecast(city); return f'{city}: {desc}, {temp}; feels like {feels}.'
    if low in ('tell me news','give me news','news'): return '\n'.join(get_news()) or 'No headlines returned.'
    if low == 'movie' or low.startswith('movie '):
        title=query[6:].strip()
        if not title: return 'Type movie followed by a title.'
        import imdb
        matches=imdb.IMDb().search_movie(title)
        return '\n'.join(f"{m.get('title','Unknown')} ({m.get('year','year unknown')})" for m in matches[:5]) or 'No movies found.'
    if low in ('send an email','send email'): return 'Use the Email button to enter and review the recipient, subject, and message.'
    if low == 'subscribe':
        webbrowser.open('https://www.youtube.com/'); return 'Opened YouTube. Choose a channel there.'
    if not GEMINI_API_KEY: return 'Gemini is not configured. Local commands work now; add GEMINI_API_KEY to .env for AI chat. Type help for commands.'
    response=requests.post('https://generativelanguage.googleapis.com/v1beta/models/'+GEMINI_MODEL+':generateContent', headers={'x-goog-api-key':GEMINI_API_KEY}, json={'contents':[{'parts':[{'text':query}]}]}, timeout=45)
    if not response.ok: raise ValueError(f'Gemini returned HTTP {response.status_code}. Check the API key and GEMINI_MODEL in .env.')
    candidates=response.json().get('candidates',[])
    if not candidates: return 'Gemini returned no response.'
    return ''.join(part.get('text','') for part in candidates[0].get('content',{}).get('parts',[])) or 'Gemini returned no text.'
