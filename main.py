from kivy.app import App
from kivy.lang import Builder

GUI = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return GUI
    
    def on_button_press(self):
        print("Botão pressionado!")

if __name__ == "__main__":
    MainApp().run()





