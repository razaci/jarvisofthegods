import threading
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from constants import ASSETS, USER
from commands import handle, HELP
from utils import speak, send_email

class Jarvis(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=16, spacing=10, **kwargs)
        self.busy=False
        self.add_widget(Label(text='JARVIS AI', font_size=28, size_hint_y=None, height=42))
        self.add_widget(Image(source=str(ASSETS/'jarvis.gif'), anim_delay=0.05, size_hint_y=.4))
        self.output=TextInput(text=f'Hello {USER}. Type help to see commands.', readonly=True, font_size=18)
        self.add_widget(self.output)
        self.input=TextInput(hint_text='Type a command or question...', multiline=False, size_hint_y=None,height=48)
        self.input.bind(on_text_validate=self.submit); self.add_widget(self.input)
        row=BoxLayout(size_hint_y=None,height=48,spacing=8)
        self.send=Button(text='Send'); self.send.bind(on_release=self.submit); row.add_widget(self.send)
        self.listen=Button(text='Listen'); self.listen.bind(on_release=self.start_recording); row.add_widget(self.listen)
        email=Button(text='Email');email.bind(on_release=self.email_dialog);row.add_widget(email)
        help_button=Button(text='Help');help_button.bind(on_release=lambda *_:setattr(self.output,'text',HELP));row.add_widget(help_button)
        self.add_widget(row)
        row=BoxLayout(size_hint_y=None,height=32)
        self.status=Label(text='Ready');row.add_widget(self.status)
        row.add_widget(Label(text='Speak responses',size_hint_x=.5))
        self.voice=Switch(active=False,size_hint_x=.3);row.add_widget(self.voice);self.add_widget(row)
    def set_busy(self,value,status):
        self.busy=value;self.send.disabled=value;self.listen.disabled=value;self.status.text=status
    def work(self, operation):
        if self.busy:return
        self.set_busy(True,'Working...')
        voice=self.voice.active
        def worker():
            try:
                result=operation()
                Clock.schedule_once(lambda dt: self.show(result))
                if voice:speak(result)
            except Exception as exc:
                message=f'Error: {exc}'
                Clock.schedule_once(lambda dt: self.show(message))
            finally:
                Clock.schedule_once(lambda dt:self.set_busy(False,'Ready'))
        threading.Thread(target=worker,daemon=True).start()
    def show(self,text):self.output.text=str(text)
    def submit(self,*_):
        query=self.input.text.strip()
        if not query:return
        self.work(lambda:handle(query))
    def start_recording(self,*_):
        def record():
            import speech_recognition as sr
            recognizer=sr.Recognizer();recognizer.operation_timeout=20
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source,duration=.4)
                audio=recognizer.listen(source,timeout=6,phrase_time_limit=12)
            query=recognizer.recognize_google(audio,language='en-US')
            Clock.schedule_once(lambda dt:setattr(self.input,'text',query))
            return handle(query)
        self.work(record)
    def email_dialog(self,*_):
        layout=BoxLayout(orientation='vertical',padding=12,spacing=8)
        recipient=TextInput(hint_text='Recipient email',multiline=False,size_hint_y=None,height=40)
        subject=TextInput(hint_text='Subject',multiline=False,size_hint_y=None,height=40)
        body=TextInput(hint_text='Message')
        for field in (recipient,subject,body):layout.add_widget(field)
        row=BoxLayout(size_hint_y=None,height=44,spacing=8)
        send=Button(text='Send reviewed email');cancel=Button(text='Cancel');row.add_widget(send);row.add_widget(cancel);layout.add_widget(row)
        popup=Popup(title='Review email before sending',content=layout,size_hint=(.9,.85))
        cancel.bind(on_release=popup.dismiss)
        def send_reviewed(*_):
            if self.busy:return
            to=recipient.text.strip();sub=subject.text;message=body.text
            if '@' not in to or not message.strip():popup.title='Enter a recipient and message';return
            popup.dismiss()
            def action():send_email(to,sub,message);return 'Email sent to '+to+'.'
            self.work(action)
        send.bind(on_release=send_reviewed);popup.open()
