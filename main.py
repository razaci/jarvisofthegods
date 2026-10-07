from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '760')
Config.set('graphics', 'fullscreen', '0')
from kivy.app import App
from jarvis import Jarvis
class JarvisApp(App):
    title = 'Jarvis AI'
    def build(self): return Jarvis()
if __name__ == '__main__': JarvisApp().run()
