
__version__ = "0.1.0"

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image


class JumpscareApp(App):

    def build(self):
        self.layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        self.status_label = Label(
            text="Ready when you are!",
            font_size="24sp",
            size_hint_y=None,
            height=50
        )

        self.start_button = Button(
            text="Start",
            font_size="24sp",
            size_hint_y=None,
            height=70
        )

        self.start_button.bind(
            on_press=self.start_jumpscare
        )
        self.scare_image = Image(
            source='Polar Owl of Darknedd.jpeg', 
            size_hint=(1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        self.layout.add_widget(self.scare_image)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.start_button)
        self.scare_image.opacity = 0

        return self.layout

    def start_jumpscare(self, instance):
        self.status_label.text = "Waiting..."
        self.start_button.disabled = True

        Clock.schedule_once(
            self.trigger_jumpscare, 5
        )

    def trigger_jumpscare(self, dt):
        self.status_label.text = "BOO!"
        self.scare_image.opacity = 1
        Clock.schedule_once(
            self.restart, 2.5
        )
    def restart(self, dt):    
        self.scare_image.opacity = 0
        self.start_button.text = "Start again"
        self.start_button.disabled = False
        self.status_label.text = "Wanna go again :)?"


JumpscareApp().run()
