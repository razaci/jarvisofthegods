JARVIS AI — WINDOWS PACKAGE

1. Install Python 3.11 (64-bit) from https://www.python.org/downloads/windows/
   Keep the Python launcher selected during installation.
2. Extract this entire ZIP into a writable folder, such as Documents\Jarvis-AI.
3. Double-click Setup-Windows.cmd. Internet is needed to install dependencies.
4. Double-click Run-Jarvis.cmd. Type help, or click Listen for one voice command.
   Run-Console.cmd provides the same command engine without graphics.

No Conda, Git, FFmpeg, or API key is required to open the app.
This is a runnable Python project, not a bundled standalone .exe.

OPTIONAL SETTINGS
Open .env with Notepad. Add GEMINI_API_KEY for Gemini AI chat, then restart.
Get your key from https://aistudio.google.com/apikey . Usage may have limits/costs.
The model is configurable through GEMINI_MODEL; no ChatGPT account connection
or OpenAI API is implemented in the original repository or this package.
News and weather require their corresponding NewsAPI/OpenWeather keys.
Email requires SMTP settings and an app password where your provider requires it.
Set DISCORD_PATH/GTA_PATH to your actual executable paths if you use those commands.
Never share a populated .env file.

TRY THESE
help
open notepad
time
youtube relaxing music
search on google Windows microphone settings
search on wikipedia Spokane
weather Spokane
movie Alien

OFFLINE / ONLINE
Time/date, launching installed apps, and Windows speech output work locally.
Listen sends recorded speech to Google's speech recognition service and needs
internet. Gemini, public IP, movie lookup, Wikipedia, news/weather and browser
searches also need internet. Typing works without a microphone.
Responses are shown on screen; enable Speak responses for Windows speech output.
Email is composed and explicitly sent from the Email dialog.
YouTube opens search results so you choose the video.

TROUBLESHOOTING
If py is not found, repair Python 3.11 installation and enable its launcher.
If setup fails, read the terminal error and rerun Setup-Windows.cmd.
If Listen fails, enable Windows Settings > Privacy & security > Microphone >
Let desktop apps access your microphone, and select a working default input.
The app remains usable by typing if audio hardware is unavailable.
If the GUI cannot open, use Run-Console.cmd and check your graphics driver.
If Gemini rejects the request, check the key and choose an available model in .env.

SOURCE / FIXES
Repository: https://github.com/razaci/Jarvis-AI
Source main commit: 582b4a9d20b7f5c3f0a910bcfb5fe847ceb933a0
Actual upstream entry point: GUI/main.py (Kivy app).
Unmodified upstream source/assets are in original-source (bytecode excluded).
Working application remains in GUI, with original animation/assets retained.
Fixed launch paths, replaced oversized requirements with direct dependencies,
updated PyAudio for Python 3.11 wheels, removed automatic microphone startup,
bounded recording/network waits, prevented concurrent recognition, marshalled
UI updates onto Kivy's main thread, and replaced hardcoded personal app paths.
Replaced FFmpeg-dependent gTTS/pydub playback with local Windows pyttsx3 speech.
Replaced the legacy Gemini SDK/model with the REST API and a configurable model.
Added typed commands, a resizable GUI, optional settings and an email compose UI.
Removed the coordinate-based promotional subscribe automation; opens YouTube.
Console fallback previously imported missing const/online modules; now shares
the repaired command engine. No repository commit/push/change was performed.

VALIDATION
See VALIDATION.txt for checks performed. A real Windows microphone, speech,
graphics driver, credentials and live API responses require testing on your PC.
