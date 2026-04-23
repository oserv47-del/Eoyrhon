from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

class MainApp(MDApp):
    def build(self):
        # App ki theme set karein
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        screen = MDScreen()

        # Ek main vertical layout banaya
        main_layout = MDBoxLayout(orientation="vertical")

        # 1. Top App Bar (Jaise WhatsApp/Facebook me upar patti hoti hai)
        toolbar = MDTopAppBar(
            title="My Premium App",
            elevation=4,
            pos_hint={"top": 1}
        )
        main_layout.add_widget(toolbar)

        # 2. Content Layout (Center wali cheezon ke liye)
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint_y=None,
            height=dp(250)
        )

        # Swagat (Welcome) Label
        self.result_label = MDLabel(
            text="App me aapka swagat hai!",
            halign="center",
            font_style="H5"
        )
        content.add_widget(self.result_label)

        # Text Input (User se data lene ke liye)
        self.user_input = MDTextField(
            hint_text="Apna naam likhein (e.g., Raja Bhai)",
            mode="rectangle",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        content.add_widget(self.user_input)

        # Action Button
        btn = MDRaisedButton(
            text="Click Me",
            pos_hint={"center_x": 0.5},
            on_release=self.button_click # Button dabane par ye function chalega
        )
        content.add_widget(btn)

        # Content ko main layout me add kiya
        main_layout.add_widget(content)
        
        # Niche ki khali jagah ko manage karne ke liye ek blank box
        main_layout.add_widget(MDBoxLayout())

        screen.add_widget(main_layout)
        return screen

    # 3. Button Click Logic (Backend)
    def button_click(self, instance):
        name = self.user_input.text
        # Agar user ne kuch likha hai
        if name != "":
            self.result_label.text = f"Hello, {name}!"
        # Agar box khali hai
        else:
            self.result_label.text = "Bhai, pehle naam toh likho!"

if __name__ == "__main__":
    MainApp().run()
