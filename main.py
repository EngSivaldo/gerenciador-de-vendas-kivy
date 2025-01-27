from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests   

# Carregar o arquivo KV
GUI = Builder.load_file("main.kv")

class MainApp(App):
    id_usuario = 1
    #constroe parte visual
    def build(self):
        return GUI

    #executa assim que ele inicia
    def on_start(self):
        #pegar info dos usuarios============================
        requisicao = requests.get(f"https://apilactivovendashash-default-rtdb.firebaseio.com/{self.id_usuario}.json")
        requisicao_dic = requisicao.json()
        # print(requisicao.json())
        #preencher foto de perfil ==========================
        avatar = requisicao_dic['avatar']
        # print(avatar) 
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f'icones/fotos_perfil/{avatar}'
        # print(requisicao_dic)

        #preencher lista de vendas==========================
        try:
            vendas = requisicao_dic['vendas'][1:]
            for venda in vendas:
                print(venda)   
                venda['cliente']
                venda['data']
        except:
            pass


    
    def mudar_tela(self, id_tela):
        # Obter o gerenciador de telas usando o id
        gerenciador_telas = self.root.ids['screen_manager']
        # Alterar a tela atual para a tela com o id fornecido
        gerenciador_telas.current = id_tela

if __name__ == "__main__":
    MainApp().run()


#get - pegar info do bd
#post -> enviar para o bd
#patch -> atualizar