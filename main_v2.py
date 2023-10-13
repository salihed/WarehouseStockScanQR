import os
import pandas as pd
import cv2
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from pyzbar.pyzbar import decode

EXCEL_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "mezanin.xlsx")
TARGET_PRODUCT = "100285300"


class MyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Dosyayı oku ve Ürün ve Taşıma birimi sütunlarını metin olarak oku
        self.df = pd.read_excel(EXCEL_PATH, dtype={'Ürün': str, 'Taşıma birimi': str})
        self.target_units = self.df[self.df["Ürün"] == TARGET_PRODUCT]["Taşıma birimi"].tolist()

    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserIconView(filters=['*.jpeg', '*.jpg', '*.png'])
        select_button = Button(text="Select and Highlight")
        select_button.bind(on_press=self.highlight_qr)

        layout.add_widget(self.file_chooser)
        layout.add_widget(select_button)
        return layout

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def highlight_qr(self, instance):
        found_match = False
        selected = self.file_chooser.selection
        if selected:
            img_path = selected[0]
            image = cv2.imread(img_path)
            decoded = decode(image)

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2
            font_thickness = 3

            for d in decoded:
                data = d.data.decode('utf-8')

                # Okunan QR kodu, target_units listesi içerisinde mi kontrol et
                if data in self.target_units:
                    x, y, w, h = d.rect
                    cv2.putText(image, "OK", (x, y + h + 30), font, font_scale, (0, 0, 255), font_thickness)
                    found_match = True

            cv2.imshow("Highlighted Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if found_match:
                self.show_popup("Bilgi", "Eşleşme bulundu!")
            else:
                self.show_popup("Bilgi", "Eşleşme bulunamadı.")


if __name__ == '__main__':
    MyApp().run()
