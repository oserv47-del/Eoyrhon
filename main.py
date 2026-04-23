from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.toast import toast
from kivy.utils import platform
import requests
import threading
import uuid

# UI Design (KV Language for cleaner, iOS-like look)
KV = '''
ScreenManager:
    HomeScreen:
    OrderScreen:
    PaymentScreen:

<HomeScreen>:
    name: "home"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.1, 0.1, 0.1, 1  # Dark iOS background
        
        MDTopAppBar:
            title: "Premium Store"
            specific_text_color: 1, 1, 1, 1
            md_bg_color: 0.1, 0.1, 0.1, 1
            elevation: 0

        ScrollView:
            MDGridLayout:
                id: product_grid
                cols: 1
                spacing: dp(20)
                padding: dp(20)
                size_hint_y: None
                height: self.minimum_height

<ItemCard@MDCard>:
    size_hint_y: None
    height: dp(200)
    radius: [dp(15)]
    elevation: 4
    md_bg_color: 0.15, 0.15, 0.15, 1
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(5)
    ripple_behavior: True
    
    image_source: ""
    item_title: ""
    item_price: ""
    
    FitImage:
        source: root.image_source
        size_hint_y: 0.7
        radius: [dp(10), dp(10), 0, 0]
        
    MDBoxLayout:
        size_hint_y: 0.3
        orientation: "horizontal"
        MDLabel:
            text: root.item_title
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "H6"
            bold: True
        MDLabel:
            text: root.item_price
            theme_text_color: "Custom"
            text_color: 0, 0.8, 0.2, 1
            font_style: "H6"
            halign: "right"

<OrderScreen>:
    name: "order"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.1, 0.1, 0.1, 1
        
        MDTopAppBar:
            title: "Enter Details"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            md_bg_color: 0.1, 0.1, 0.1, 1
            elevation: 0

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(30)
            spacing: dp(20)
            
            MDLabel:
                id: selected_item_label
                text: "Item: "
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                font_style: "H6"
                size_hint_y: None
                height: dp(40)
                
            MDTextField:
                id: game_id_input
                hint_text: "Enter BGMI Game ID"
                mode: "rectangle"
                text_color_normal: 1, 1, 1, 1
                hint_text_color_normal: 0.5, 0.5, 0.5, 1
                line_color_normal: 0.5, 0.5, 0.5, 1
                
            Widget: # Spacer
                
            MDRaisedButton:
                text: "Proceed to Payment"
                size_hint_x: 1
                md_bg_color: 0.2, 0.5, 1, 1 # iOS Blue
                on_release: app.go_to_payment()
                
            Widget:
                size_hint_y: 2

<PaymentScreen>:
    name: "payment"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.1, 0.1, 0.1, 1
        
        MDTopAppBar:
            title: "Payment"
            left_action_items: [["arrow-left", lambda x: app.go_back_to_order()]]
            md_bg_color: 0.1, 0.1, 0.1, 1
            elevation: 0
            
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(30)
            spacing: dp(30)
            
            MDLabel:
                text: "Total Amount to Pay:"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.7, 0.7, 0.7, 1
                
            MDLabel:
                id: amount_label
                text: "₹0"
                halign: "center"
                font_style: "H3"
                theme_text_color: "Custom"
                text_color: 0, 0.8, 0.2, 1
                bold: True
                
            MDRaisedButton:
                text: "Pay via UPI"
                size_hint_x: 1
                md_bg_color: 0.2, 0.8, 0.2, 1
                on_release: app.process_payment()
                
            Widget:
'''

class HomeScreen(Screen):
    pass

class OrderScreen(Screen):
    pass

class PaymentScreen(Screen):
    pass

class PopularityApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TELEGRAM BOT SETTINGS (Yahan apna Bot Token aur Chat ID dalein)
        self.BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
        self.CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
        self.UPI_ID = "8406962570@ybl"
        
        self.selected_item_name = ""
        self.selected_item_price = ""
        self.selected_game_id = ""

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.sm = Builder.load_string(KV)
        self.load_products()
        return self.sm

    def load_products(self):
        # YouTube Thumbnail jaise items (Internet se images load ho rahi hain test ke liye)
        products = [
            {"name": "Motorcycle (200 Pop)", "price": "₹20", "img": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=500"},
            {"name": "Sports Car (1000 Pop)", "price": "₹100", "img": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=500"},
            {"name": "Airplane (5000 Pop)", "price": "₹450", "img": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=500"}
        ]
        
        grid = self.sm.get_screen("home").ids.product_grid
        from kivy.factory import Factory
        for p in products:
            card = Factory.ItemCard()
            card.image_source = p["img"]
            card.item_title = p["name"]
            card.item_price = p["price"]
            # Bind click event
            card.bind(on_release=lambda instance, name=p["name"], price=p["price"]: self.open_order_page(name, price))
            grid.add_widget(card)

    def open_order_page(self, name, price):
        self.selected_item_name = name
        self.selected_item_price = price
        self.sm.get_screen("order").ids.selected_item_label.text = f"Selected: {name}"
        self.sm.transition.direction = "left"
        self.sm.current = "order"

    def go_back(self):
        self.sm.transition.direction = "right"
        self.sm.current = "home"
        
    def go_back_to_order(self):
        self.sm.transition.direction = "right"
        self.sm.current = "order"

    def go_to_payment(self):
        game_id = self.sm.get_screen("order").ids.game_id_input.text
        if len(game_id) < 5:
            toast("Sahi Game ID dalein!")
            return
            
        self.selected_game_id = game_id
        self.sm.get_screen("payment").ids.amount_label.text = self.selected_item_price
        self.sm.transition.direction = "left"
        self.sm.current = "payment"

    def process_payment(self):
        amount = self.selected_item_price.replace("₹", "")
        
        # 1. Telegram Message Bhejein (Background thread me taki app hang na ho)
        threading.Thread(target=self.send_telegram_msg, args=(amount,)).start()
        
        # 2. UPI App Open Karein (Android Only)
        if platform == 'android':
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                uri_string = f"upi://pay?pa={self.UPI_ID}&pn=Store&am={amount}&cu=INR"
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(uri_string))
                PythonActivity.mActivity.startActivity(intent)
            except Exception as e:
                toast("UPI App open nahi ho paya")
        else:
            toast("UPI is only supported on Android devices.")

    def send_telegram_msg(self, amount):
        # Device ID nikalna
        device_id = str(uuid.getnode()) 
        if platform == 'android':
            try:
                from jnius import autoclass
                SettingsSecure = autoclass('android.provider.Settings$Secure')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                device_id = SettingsSecure.getString(PythonActivity.mActivity.getContentResolver(), SettingsSecure.ANDROID_ID)
            except:
                pass

        msg = (f"🚀 *New Order Initiated*\n"
               f"Game ID: `{self.selected_game_id}`\n"
               f"Item: {self.selected_item_name}\n"
               f"Amount: ₹{amount}\n"
               f"Device ID: {device_id}")
               
        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
        payload = {"chat_id": self.CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print("Telegram send error:", e)

if __name__ == "__main__":
    PopularityApp().run()
