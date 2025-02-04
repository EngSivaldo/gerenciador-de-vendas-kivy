# main.py
from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
from banner_venda import BannerVenda
import os
from functools import partial
import json
import requests   
from myfirebase import MyFirebase


# Carregar o arquivo KV
GUI = Builder.load_file("main.kv")

class MainApp(App):
    # Constroe parte visual
    def build(self):
        self.firebase = MyFirebase()
        return GUI

    # Executa assim que ele inicia
    def on_start(self):
        #carregar as fotos de perfil
        arquivos = os.listdir('icones/fotos_perfil')
        pagina_fotoperfil = self.root.ids['fotoperfilpage']
        lista_fotos = pagina_fotoperfil.ids['lista_fotos_perfil']
        for foto in arquivos:
            imagem = ImageButton(source=f'icones/fotos_perfil/{foto}', on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        self.carregar_infos_usuario()
      

    def carregar_infos_usuario(self):    
        try:
            with open('refreshtoken.txt', 'r') as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            
            self.local_id = local_id
            self.id_token = id_token

            requisicao = requests.get(f"https://apilactivovendashash-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            # print("Requisição JSON:", requisicao_dic)

            if 'avatar' in requisicao_dic:
                avatar = requisicao_dic['avatar']
                foto_perfil = self.root.ids['foto_perfil']
                foto_perfil.source = f'icones/fotos_perfil/{avatar}'
                print("Foto de perfil carregada:", foto_perfil.source)
            else:
                print("Campo 'avatar' não encontrado na resposta JSON.")
            
            if 'vendas' in requisicao_dic and requisicao_dic['vendas']:
                vendas = requisicao_dic['vendas'][1:]
                pagina_homepage = self.root.ids['homepage']
                lista_vendas = pagina_homepage.ids['lista_vendas']
                for venda in vendas:
                    print("Dados da venda:", venda)
                    banner = BannerVenda(
                        cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                        produto=venda['produto'], foto_produto=venda['foto_produto'],
                        data=venda['data'], preco=venda['preco'],
                        unidade=venda['unidades'], quantidade=venda['quantidade']
                    )
                    lista_vendas.add_widget(banner)
            else:
                print("Campo 'vendas' não encontrado ou está vazio na resposta JSON.")
            self.mudar_tela('homepage') #vai para homepage
            
        except Exception as e:
            print("Erro ao carregar informações do usuário:", e)



            

    def mudar_tela(self, id_tela):
        # Obter o gerenciador de telas usando o id
        gerenciador_telas = self.root.ids['screen_manager']
        # Alterar a tela atual para a tela com o id fornecido
        gerenciador_telas.current = id_tela