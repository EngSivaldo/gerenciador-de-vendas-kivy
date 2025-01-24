from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

class HomePage(Screen):
    pass

class AjustesPage(Screen):
    pass

# Carregar o arquivo KV
GUI = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return GUI
    
    def mudar_tela(self, id_tela):
        # Obter o gerenciador de telas usando o id
        gerenciador_telas = self.root.ids['screen_manager']
        # Alterar a tela atual para a tela com o id fornecido
        gerenciador_telas.current = id_tela

if __name__ == "__main__":
    MainApp().run()
