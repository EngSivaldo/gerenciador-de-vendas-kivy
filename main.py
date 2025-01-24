from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

GUI = Builder.load_file("main.kv")


class HomePage(Screen):
    pass



class MainApp(App):
    def build(self):
        return GUI
    
    def on_button_press(self):
        print("Botão pressionado!")

if __name__ == "__main__":
    MainApp().run()





