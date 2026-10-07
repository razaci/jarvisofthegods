import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
sys.path.insert(0, str(Path(__file__).parent/'GUI'))
import commands
class CommandsTest(unittest.TestCase):
    def test_no_key(self):
        with patch.object(commands,'GEMINI_API_KEY',''):
            self.assertIn('not configured',commands.handle('hello'))
    def test_search(self):
        with patch.object(commands,'search_on_google') as search:
            commands.handle('search on google two words');search.assert_called_once_with('two words')
    def test_prompt(self):
        self.assertIn('followed by',commands.handle('weather'))
        self.assertIn('topic',commands.handle('youtube'))
    def test_windows_app(self):
        with patch.object(commands.os,'name','nt'),patch.object(commands.subprocess,'Popen') as launch:
            commands.handle('open notepad');launch.assert_called_once_with(['notepad.exe'])
    def test_missing_path(self):
        with patch.dict(os.environ,{'GTA_PATH':''}):self.assertIn('GTA_PATH',commands.handle('open gta'))
    def test_gemini(self):
        response=Mock(ok=True);response.json.return_value={'candidates':[{'content':{'parts':[{'text':'Hello'}]}}]}
        with patch.object(commands,'GEMINI_API_KEY','test'),patch.object(commands.requests,'post',return_value=response) as post:
            self.assertEqual(commands.handle('hello'),'Hello')
            self.assertEqual(post.call_args.kwargs['timeout'],45)
    def test_weather(self):
        with patch.object(commands,'weather_forecast',return_value=('clear','20 C','19 C')) as weather:
            self.assertIn('Spokane',commands.handle('weather Spokane'));weather.assert_called_once_with('Spokane')
    def test_email_route(self):self.assertIn('Email button',commands.handle('send an email'))
    def test_help(self):self.assertIn('open notepad',commands.handle('help'))
    def test_date(self):self.assertTrue(commands.handle('date'))
if __name__=='__main__':unittest.main()
