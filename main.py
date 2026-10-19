
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
            font_size="24sp"
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
            size_hint=(0.8, 0.8), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
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
        self.start_button.text = "Start again"
        self.start_button.disabled = False
        self.scare_image.opacity = 1



JumpscareApp().run()
