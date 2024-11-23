import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

class LabelMakerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10)
        
        # Input fields with dynamic animations
        self.project_name = TextInput(hint_text="Enter Project Name", size_hint=(1, None), height=40)
        self.project_location = TextInput(hint_text="Enter Project Location", size_hint=(1, None), height=40)
        self.project_date = TextInput(hint_text="Enter Project Date", size_hint=(1, None), height=40)

        # Add animated widgets to the layout
        self.layout.add_widget(self.project_name)
        self.layout.add_widget(self.project_location)
        self.layout.add_widget(self.project_date)
        
        # Upload CSV button with animation
        self.upload_button = Button(text="Upload CSV File", size_hint=(1, None), height=50)
        self.upload_button.bind(on_press=self.upload_csv)
        self.layout.add_widget(self.upload_button)

        # Generate labels button with animation
        self.generate_button = Button(text="Generate Labels", size_hint=(1, None), height=50)
        self.generate_button.bind(on_press=self.generate_labels)
        self.layout.add_widget(self.generate_button)

        return self.layout

    def upload_csv(self, instance):
        # Animation for the button press
        animation = Animation(color=(0, 1, 0, 1), duration=0.5)
        animation.start(instance)

        # File chooser for CSV file upload
        filechooser = FileChooserIconView()
        filechooser.bind(on_selection=lambda *x: self.load_csv(filechooser.selection))
        
        popup = Popup(title="Choose CSV File", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()

    def load_csv(self, selection):
        if selection:
            self.csv_file = selection[0]  # Choose first file
            print(f"CSV file selected: {self.csv_file}")
        else:
            print("No file selected")

    def generate_labels(self, instance):
        if not hasattr(self, 'csv_file'):
            print("CSV file not selected.")
            return
        
        # Load the CSV data
        data = pd.read_csv(self.csv_file)

        # Create labels as in your existing code
        self.create_pdf(data)
        
        print("Labels generated!")

    def create_pdf(self, data):
        # PDF creation with project info
        pages = []
        page = Image.new("RGB", (600, 800), "white")
        draw = ImageDraw.Draw(page)

        # Add project details at the top with large font size
        font = ImageFont.truetype("arial.ttf", 24)
        draw.text((10, 10), f"Project: {self.project_name.text}", fill="black", font=font)
        draw.text((10, 50), f"Location: {self.project_location.text}", fill="black", font=font)
        draw.text((10, 90), f"Date: {self.project_date.text}", fill="black", font=font)

        # Add labels from CSV data (you can customize this)
        # Save PDF
        current_date = datetime.now().strftime("%d_%m_%Y")
        output_pdf = f"/storage/emulated/0/Documents/Labels_{current_date}.pdf"
        pages[0].save(output_pdf, save_all=True, append_images=pages[1:])
        print(f"Labels saved to {output_pdf}")

if __name__ == "__main__":
    LabelMakerApp().run()
