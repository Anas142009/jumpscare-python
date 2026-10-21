
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

        self.glitch_sound = SoundLoader.load("glitch1.mp3")
        if self.glitch_sound:
            self.glitch_sound.volume = 1
            self.glitch_sound.loop = True
        #preload the sound so that it doesn't cause lag and check if it's available before the button press to dismiss crashes.
        
        self.layout = FloatLayout()
        self.lang_label= Label(
            text="Choose a language./اختر لغة.",
            font_size="24sp",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        
        self.En_button= Button(
            text="English",
            font_size="24sp",
            size_hint=(1, 0.06),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        
        self.En_button.bind(on_press=self.declare_warning)
        self.layout.add_widget(self.lang_label)
        self.layout.add_widget(self.En_button)

        return self.layout
    def declare_warning(self, instance):  
        self.layout.clear_widgets()
        
        self.warning_label = Label(
            text="WARNING\n\nThis experience contains loud noises, flashing lights and images.\n\nViewer discretion is advised.",
            font_size="24sp",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.layout.add_widget(self.warning_label)
        Clock.schedule_once(self.load_main_game, 3.5)
        
        
        
    def load_main_game(self, dt):
        self.layout.clear_widgets()

        self.version_label = Label(
            text="version 0.1.0",
            font_size="12sp",
            size_hint=(0.15, 0.15),
            pos_hint={'right': 0.95, 'top': 0.95}
        )
        self.status_label = Label(
            text="Press Start to continue.",
            font_size="24sp",
            size_hint_y=None,
            height=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.start_button = Button(
            text="Start",
            font_size="24sp",
            size_hint=(1, 0.04),
            pos_hint={'right': 0.95, 'y': 0.05}
        )

        self.start_button.bind(on_press=self.start_glitch)
        self.scare_image = Image(
            source='Polar Owl of Darknedd.jpeg', 
            size_hint=(1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )
        self.glitch_image = Image(
            source='glitch.png', 
            size_hint=(1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )
        self.layout.add_widget(self.version_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.glitch_image)
        self.glitch_image.opacity = 0
        self.layout.add_widget(self.scare_image)
        self.scare_image.opacity = 0
        if self.ambience:
            self.ambience.play()
    def start_glitch(self, instance):
        self.status_label.text = "Loading..."
        self.start_button.disabled = True
        Clock.schedule_once(self.trigger_glitch, 10)

    def trigger_glitch(self, dt):
        if self.glitch_sound:
            self.glitch_sound.play()
            self.ambience.stop()
        self.glitch_image.opacity = 1
        Clock.schedule_once(self.glitch_restart, 2.3)

    def glitch_restart(self, dt):
        self.glitch_sound.stop()
        self.ambience.play()
        self.glitch_image.opacity = 0
        self.start_button.disabled = False
        self.start_button.unbind(on_press=self.start_glitch)
        self.start_button.bind(on_press=self.start_jumpscare)
        self.status_label.text = "An error has occured.\n\nPlease try again."
        self.start_button.text = "Try again"
        
        

    def start_jumpscare(self, instance):
        self.status_label.text = "Loading..."
        self.start_button.disabled = True

        Clock.schedule_once(
            self.trigger_jumpscare, 10
        )

    def trigger_jumpscare(self, dt):
        if self.scare_sound:
            self.scare_sound.play()
            self.ambience.stop() # Remember the parenthesis()
        Clock.schedule_once(self.show_image, 0.25)
        
        Clock.schedule_once(
            self.restart, 3.2
        )
    def show_image(self, dt):
        self.scare_image.opacity = 1
        
    def restart(self, dt):    
        self.ambience.play()
        self.scare_image.opacity = 0
        self.start_button.text = "Reboot"
        self.start_button.disabled = False
        self.start_button.unbind(on_press=self.start_jumpscare)
        self.start_button.bind(on_press=self.start_glitch)
        self.status_label.text = "Did I get you?"


JumpscareApp().run()
