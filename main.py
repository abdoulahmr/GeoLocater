from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
import geocoder
from datetime import datetime
from kivy_garden.mapview import MapView, MapMarker
import xml.etree.ElementTree as ET

class LocationApp(App):
    def build(self):
        self.sm = ScreenManager()

        main_sc = Screen(name='main')
        self.mapview = MapView(zoom=13, lat=0, lon=0)
        self.marker = MapMarker()
        self.mapview.add_marker(self.marker)
        self.location_lab = Label(text="Your location..")
        history_btn = Button(
            text="History", 
            on_press=self.history,
        )
        label_button_layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            padding=(10, 10, 10, 10)
        )
        label_button_layout.add_widget(self.location_lab)
        label_button_layout.add_widget(history_btn)
        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=(10, 10, 10, 10)
        )
        layout.add_widget(self.mapview)
        layout.add_widget(label_button_layout)
        main_sc.add_widget(layout)

        history_sc = Screen(name='history')
        self.history_lab = Label(text="Location history : ")
        back_btn = Button(
            text="Back to home",
            on_press=self.home,
            size_hint=(None, None),
            size=(200, 70)
        )
        history_layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            padding=(50, 50, 50, 50)
        )
        history_layout.add_widget(self.history_lab)
        history_layout.add_widget(back_btn)
        history_sc.add_widget(history_layout)

        self.sm.add_widget(main_sc)
        self.sm.add_widget(history_sc)

        Clock.schedule_interval(self.getLocation, 60)
        Window.size = (700, 800)
        self.mapview.size_hint_y = None
        self.mapview.height = Window.height * 0.8

        return self.sm

    def getLocation(self, dt):
        location = geocoder.ip('me')
        lat, lon = location.latlng
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        location_info = f"""Latitude: {lat}\nLongitude: {lon}\nTime: {t}\n\n\n"""
        self.location_lab.text = f"Latitude: {lat}\nLongitude: {lon}"
        self.mapview.center_on(lat, lon)
        self.marker.lat = lat
        self.marker.lon = lon

        self.history_lab.text += location_info

        self.createXML(lat, lon, t)

    def createXML(self, lat, lon, t):
        file = 'location.xml'

        root = ET.Element('locations')
        location_element = ET.SubElement(root, 'location')
        ET.SubElement(location_element, 'latitude').text = str(lat)
        ET.SubElement(location_element, 'longitude').text = str(lon)
        ET.SubElement(location_element, 'time').text = t

        tree = ET.ElementTree(root)
        tree.write(file)

    def history(self, instance):
        self.sm.current = 'history'

    def home(self, instance):
        self.sm.current = 'main'

LocationApp().run()
