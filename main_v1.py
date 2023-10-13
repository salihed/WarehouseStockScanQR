import os
import pandas as pd
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from pyzbar.pyzbar import decode
from PIL import Image as PILImage

# Masaüstündeki dosya yolu (Windows için)
EXCEL_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "mezanin.xlsx")


class MyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = pd.read_excel(EXCEL_PATH)  # Excel dosyasını oku

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Yalnızca .jpeg, .jpg ve .png dosyalarını gösteren bir filtre ekleyin
        self.file_chooser = FileChooserIconView(filters=['*.jpeg', '*.jpg', '*.png'])

        select_button = Button(text="Select and Decode")
        select_button.bind(on_press=self.decode_qr)

        # Ürün bilgisini gösterecek etiketi ekleyelim
        self.product_label = Label()

        layout.add_widget(self.file_chooser)
        layout.add_widget(select_button)
        layout.add_widget(self.product_label)
        return layout

    def decode_qr(self, instance):
        selected = self.file_chooser.selection
        if selected:
            img_path = selected[0]
            img = PILImage.open(img_path)
            decoded = decode(img)
            for d in decoded:
                data = d.data.decode('utf-8')

                # Eğer data "MZ" ile başlıyorsa, bu datayı atla
                if data.startswith("MZ"):
                    print(f"{data} MZ ile başladığı için arama yapılmayacak.")
                    continue

                print(data)

                # Eğer decode edilen data, "Taşıma birimi" sütununda varsa...
                matched_rows = self.df[self.df["Taşıma birimi"].astype(str) == data]
                if not matched_rows.empty:
                    product = matched_rows["Ürün"].iloc[0]
                    print(f"{data} için ürün: {product}")
                    self.product_label.text = f"Ürün: {product}"
                else:
                    print(f"{data} mezanin dosyasında bulunamadı!")
                    self.product_label.text = ""


if __name__ == '__main__':
    MyApp().run()
