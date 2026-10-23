__version__ = "0.1.0"

import arabic_reshaper
from bidi.algorithm import get_display
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

class JumpscareApp(App):

    def format_arabic(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    def build(self):
        self.language = "en" # Default language
        self.arabic_font = os.path.join(os.path.dirname(__file__), "ARIAL.TTF") # Ensure this file is in your directory

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
        
        self.layout = FloatLayout()
        
        # Initial Language Screen
        self.lang_label = Label(
            text=f"Choose a language. / {self.format_arabic('اختر لغة.')}",
            font_size="24sp",
            halign="center",
            font_name=self.arabic_font,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        
        self.En_button = Button(
            text="English",
            font_size="24sp",
            size_hint=(1, 0.06),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        self.En_button.bind(on_press=self.set_english)

        self.Ar_button = Button(
            text=self.format_arabic("العربية"),
            font_size="24sp",
            font_name=self.arabic_font,
            size_hint=(1, 0.06),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        self.Ar_button.bind(on_press=self.set_arabic)

        self.layout.add_widget(self.lang_label)
        self.layout.add_widget(self.En_button)
        self.layout.add_widget(self.Ar_button)

        return self.layout

    def set_english(self, instance):
        self.language = "en"
        self.declare_warning()

    def set_arabic(self, instance):
        self.language = "ar"
        self.declare_warning()

    def declare_warning(self):  
        self.layout.clear_widgets()
        
        if self.language == "ar":
            warning_text = self.format_arabic("تحذير\n\nهذه التجربة تحتوي على أصوات\n عالية، أضواء وامضة، وصور مزعجة.\n\nينصح بإغلاق التطبيق إن كنت\nتعاني من نوبات صرع أو\nمشاكل صحية.")
            font = self.arabic_font
        else:
            warning_text = "WARNING\n\nThis experience contains loud noises, flashing lights and images.\n\nViewer discretion is advised."
            font = "Roboto" # Kivy's default

        self.warning_label = Label(
            text=warning_text,
            font_size="24sp",
            halign="center",
            font_name=font,
            text_size=(Window.width * 0.9, None), # Prevents text from stretching off screen
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.layout.add_widget(self.warning_label)
        Clock.schedule_once(self.load_main_game, 5)
        
    def load_main_game(self, dt):
        self.layout.clear_widgets()

        font = self.arabic_font if self.language == "ar" else "Roboto"

        self.version_label = Label(
            text="version 1.0",
            font_size="12sp",
            size_hint=(0.15, 0.15),
            pos_hint={'right': 0.95, 'top': 0.95}
        )
        
        status_text = self.format_arabic("اضغط على ابدأ للمتابعة.") if self.language == "ar" else "Press Start to continue."
        self.status_label = Label(
            text=status_text,
            font_size="24sp",
            font_name=font,
            size_hint_y=None,
            height=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        start_text = self.format_arabic("ابدأ") if self.language == "ar" else "Start"
        self.start_button = Button(
            text=start_text,
            font_size="24sp",
            font_name=font,
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
        loading_text = self.format_arabic("جاري التحميل...") if self.language == "ar" else "Loading..."
        self.status_label.text = loading_text
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
        
        error_text = self.format_arabic("حدث خطأ.\n\nيرجى المحاولة مرة أخرى.") if self.language == "ar" else "An error has occured.\n\nPlease try again."
        self.status_label.text = error_text
        
        retry_text = self.format_arabic("حاول مرة أخرى") if self.language == "ar" else "Try again"
        self.start_button.text = retry_text
        
    def start_jumpscare(self, instance):
        loading_text = self.format_arabic("جاري التحميل...") if self.language == "ar" else "Loading..."
        self.status_label.text = loading_text
        self.start_button.disabled = True

        Clock.schedule_once(self.trigger_jumpscare, 10)

    def trigger_jumpscare(self, dt):
        if self.scare_sound:
            self.scare_sound.play()
            self.ambience.stop()
        Clock.schedule_once(self.show_image, 0.25)
        Clock.schedule_once(self.restart, 3.2)
        
    def show_image(self, dt):
        self.scare_image.opacity = 1
        
    def restart(self, dt):    
        self.ambience.play()
        self.scare_image.opacity = 0
        
        exit_text = self.format_arabic("خروج") if self.language == "ar" else "Exit"
        self.start_button.text = exit_text
        self.start_button.disabled = False
        
        self.start_button.unbind(on_press=self.start_jumpscare)
        self.start_button.bind(on_press=self.close_app)
        
        gotcha_text = self.format_arabic("هل أخفتك؟") if self.language == "ar" else "Did I get you?"
        self.status_label.text = gotcha_text
        
    def close_app(self, instance):
        self.stop()
        

if __name__ == "__main__":
    JumpscareApp().run()
