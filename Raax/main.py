from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        screen = MDScreen()
        screen.add_widget(
            MDLabel(
                text="Python APK via GitHub Actions!",
                halign="center",
                font_style="H4"
            )
        )
        return screen

if __name__ == "__main__":
    MainApp().run()
