
__version__ = "0.1.0"

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout

class JumpscareApp(App):

    def build(self):
        self.ambience = SoundLoader.load("Ambience.mp3")
        if self.ambience:
            self.ambience.volume = 0.8
            self.ambience.loop = True
            
        self.scare_sound = SoundLoader.load("dragon-studio-scary-scream-401725.mp3")
        if self.scare_sound:
            self.scare_sound.volume = 1
            self.scare_sound.loop = False
        #preload the sound so that it doesn't cause lag and check if it's available before the button press to dismiss crashes.
        
        self.layout = FloatLayout()
        slef.warning_label = Label(
            text="WARNING\n\nThis experience contains loud noises, flashing lights and images.\n\nViewer discretion is advised.",
            font_size="24sp",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        Clock.schedule_once(self.load_main_game, 3.5)
        
        return self.layout
        
    def load_main_game(self, dt):
        self.layout.clear_widgets()
        
        self.status_label = Label(
            text="Ready when you are!",
            font_size="24sp",
            size_hint_y=None,
            height=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.start_button = Button(
            text="Start",
            font_size="24sp",
            size_hint=(1, 0.1),
            pos_hint={'right': 0.95, 'y': 0.05}
        )

        self.start_button.bind(on_press=self.start_jumpscare)
        self.scare_image = Image(
            source='Polar Owl of Darknedd.jpeg', 
            size_hint=(1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.scare_image)
        self.scare_image.opacity = 0
        if self.ambience:
            self.ambience.play()
        
    def start_jumpscare(self, instance):
        self.status_label.text = "Loading..."
        self.start_button.disabled = True

        Clock.schedule_once(
            self.trigger_jumpscare, 10
        )

    def trigger_jumpscare(self, dt):
        if self.scare_sound:
            self.scare_sound.play()  # Remember the parenthesis()
        self.scare_image.opacity = 1
        self.status_label.text = "BOO!"
        Clock.schedule_once(
            self.restart, 3.5
        )
        
    def restart(self, dt):    
        self.scare_image.opacity = 0
        self.start_button.text = "Try again"
        self.start_button.disabled = False
        self.start_button.unbind(on_press=self.start_jumpscare)
        self.start_button.bind(on_press=self.trigger_jumpscare)
        self.status_label.text = "An error has occured. Please try again."


JumpscareApp().run()
