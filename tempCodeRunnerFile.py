# main.py
from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
from banner_venda import BannerVenda
import requests   

# Carregar o arquivo KV
GUI = Builder.load_file("main.kv")

class MainApp(App):
    id_usuario = 1
    # Constroe parte visual
    def build(self):
        return GUI

    # Executa assim que ele inicia
    def on_start(self):
        # Pegar info dos usuarios
        requisicao = requests.get(f"https://apilactivovendashash-default-rtdb.firebaseio.com/{self.id_usuario}.json")
        requisicao_dic = requisicao.json()
        print("Requisição JSON:", requisicao_dic)

        # Preencher foto de perfil
        avatar = requisicao_dic['avatar']
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f'icones/fotos_perfil/{avatar}'
        print("Foto de perfil carregada:", foto_perfil.source)

        # Preencher lista de vendas
        try:
            vendas = requisicao_dic['vendas'][1:]
            for venda in vendas:  # Cria banner e depois adicionar no gridlayout no homepage
                print("Dados da venda:", venda)
                banner = BannerVenda(
                    cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                    produto=venda['produto'], foto_produto=venda['foto_produto'],
                    data=venda['data'], preco=venda['preco'],
                    unidade=venda['unidades'], quantidade=venda['quantidade']
                )
                pagina_homepage = self.root.ids['homepage']
                lista_vendas = pagina_homepage.ids['lista_vendas']
                lista_vendas.add_widget(banner)
                print("Banner adicionado para:", venda['cliente'])

        except Exception as e:
            print("Erro ao preencher a lista de vendas:", e)

    def mudar_tela(self, id_tela):
        # Obter o gerenciador de telas usando o id
        gerenciador_telas = self.root.ids['screen_manager']
        # Alterar a tela atual para a tela com o id fornecido
        gerenciador_telas.current = id_tela

if __name__ == "__main__":
    MainApp().run()
