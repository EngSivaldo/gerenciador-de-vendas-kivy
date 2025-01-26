from kivy.uix.filechooser import ScreenManager
from kivy.uix.screenmanager import Screen

class HomePage(Screen):
    pass

class AjustesPage(Screen):
    pass


class AdicionarVendasPage(Screen):
    pass

class ListarVendedoresPage(Screen):
    pass

class FotoPerfilPage(Screen):
    pass

class AdicionarVendedorPage(Screen):
    pass

class TodasVendasPage(Screen):
    pass



#passo 1 -> criar classes no telas
#passo 2 -> criar arquivo.kv na pasta kv
#passo 3 -> adicionar todos arquivos.kv no main.kv
#passo 4 adicionar todas as classes no ScreenManager no main.kv
#passo 5 na homepage e no ajustes incluir id da tela navegacao de no botao