import importlib
import sys
from pathlib import Path
failed=[]
for module in ('kivy','PIL','dotenv','requests','speech_recognition','pyaudio','pyttsx3','wikipedia','imdb'):
    try:importlib.import_module(module);print('OK:',module)
    except Exception as exc:failed.append(module);print('FAILED:',module,exc)
for asset in ('jarvis.gif','circle.png','border.eps.png','mw.ttf','dusri.ttf','teesri.otf'):
    if not (Path(__file__).parent/'GUI'/'static'/asset).is_file():failed.append(asset)
print('Dependencies/assets:', 'FAILED' if failed else 'OK')
print('Microphone and internet services are checked only when used.')
sys.exit(bool(failed))
