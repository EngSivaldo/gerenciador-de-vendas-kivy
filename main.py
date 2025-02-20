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
from bannervendedor import BannerVendedor
from datetime import date


# Carregar o arquivo KV
GUI = Builder.load_file("main.kv")

class MainApp(App):
    # Constroe parte visual
    def build(self):
        self.firebase = MyFirebase()
        return GUI

    # Executa assim que ele inicia
    def on_start(self):
        # Carregar as fotos de perfil
        arquivos = os.listdir('icones/fotos_perfil')
        pagina_fotoperfil = self.root.ids['fotoperfilpage']
        lista_fotos = pagina_fotoperfil.ids['lista_fotos_perfil']
        for foto in arquivos:
            imagem = ImageButton(source=f'icones/fotos_perfil/{foto}', on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        self.verificar_usuario_logado()

        #carregar as fotos dos clientes
        arquivos = os.listdir('icones/fotos_clientes')
        pagina_adicionarvendas = self.root.ids['adicionarvendaspage']
        lista_clientes = pagina_adicionarvendas.ids['lista_clientes']
        for foto_cliente in arquivos:
            imagem = ImageButton(source=f'icones/fotos_clientes/{foto_cliente}', on_release=partial(self.selecionar_cliente, foto_cliente))
            label_text = foto_cliente.replace('.png', '').capitalize()
            label = LabelButton(text=label_text, on_release=partial(self.selecionar_cliente, foto_cliente))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label) 



        #carregar as fotos dos produtos
        arquivos = os.listdir('icones/fotos_produtos')
        pagina_adicionarvendas = self.root.ids['adicionarvendaspage']
        lista_produtos = pagina_adicionarvendas.ids['lista_produtos']
        for foto_produtos in arquivos:
            imagem = ImageButton(source=f'icones/fotos_produtos/{foto_produtos}', on_release=partial(self.selecionar_produto, foto_produtos))
            label_text = foto_produtos.replace('.png', '').capitalize()
            label = LabelButton(text=label_text, on_release=partial(self.selecionar_produto, foto_produtos))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        #carregar a data na pagina adicionarvendaspage
        pagina_adicionarvendas = self.root.ids['adicionarvendaspage']
        label_data = pagina_adicionarvendas.ids['label_data']
        label_data.text = f'Data: {date.today().strftime("%d/%m/%y")}'  #d/m/a

        #carregar as info do usuário
        self.carregar_infos_usuario()



    def verificar_usuario_logado(self):
        try:
            with open('refreshtoken.txt', 'r') as arquivo:
                refresh_token = arquivo.read().strip()
                if not refresh_token:
                    raise Exception("Refresh token está vazio ou não foi encontrado.")

            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            self.carregar_infos_usuario()
            self.mudar_tela('homepage')  # Redirecionar para a tela principal se o usuário estiver logado
        except Exception as e:
            print("Usuário não logado ou erro ao verificar token:", e)
            self.mudar_tela('loginpage')  # Redirecionar para a tela de login se o usuário não estiver logado


      
    def carregar_infos_usuario(self):
        try:
            with open('refreshtoken.txt', 'r') as arquivo:
                refresh_token = arquivo.read().strip()
                if not refresh_token:
                    raise Exception("Refresh token está vazio ou não foi encontrado.")

            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            # pegar info do usuario
            requisicao = requests.get(f"https://apilactivovendashash-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            print("Requisição JSON:", requisicao_dic)

            # preencher foto de perfil
            if 'avatar' in requisicao_dic:
                avatar = requisicao_dic['avatar']
                self.avatar = avatar
                foto_perfil = self.root.ids['foto_perfil']
                foto_perfil.source = f'icones/fotos_perfil/{avatar}'
                print("Foto de perfil carregada:", foto_perfil.source)
            else:
                print("Campo 'avatar' não encontrado na resposta JSON.")

            # preencher ID usuario
            id_vendedor = requisicao_dic['id_vendedor']
            self.id_vendedor = id_vendedor
            # atualizar no ajustespage
            pagina_ajustes = self.root.ids['ajustespage']
            pagina_ajustes.ids['id_vendedor'].text = f'Seu ID Único: {id_vendedor}'

            # atualizar total de vendas
            total_vendas = requisicao_dic['total_venda']  # Corrigido de 'total_vendas' para 'total_venda'
            self.total_vendas = total_vendas
            # atualizar na homepage
            homepage = self.root.ids['homepage']
            homepage.ids['label_total_vendas'].markup = True
            homepage.ids['label_total_vendas'].text = f'[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]'

            #preencher equipe
            self.equipe = requisicao_dic['equipe']

            # preencher lista de vendas
            if 'vendas' in requisicao_dic and requisicao_dic['vendas']:
                vendas = requisicao_dic['vendas'][1:]
                self.vendas = vendas
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
            
        except Exception as e:
            print("Erro ao carregar informações do usuário:", e)

       #preencher equipe de vendedores
        # Preencher equipe de vendedores
        equipe = requisicao_dic['equipe']
        lista_equipe = equipe.split(',')
        pagina_listavendedores = self.root.ids['listarvendedorespage']
        lista_vendedores = pagina_listavendedores.ids['lista_vendedores']

        for id_vendedor_equipe in lista_equipe:
            if id_vendedor_equipe:
                # Criar a instância de BannerVendedor com o ID correto
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                lista_vendedores.add_widget(banner_vendedor)
        self.mudar_tela('homepage')


    def mudar_tela(self, id_tela):
        # Obter o gerenciador de telas usando o id
        gerenciador_telas = self.root.ids['screen_manager']
        # Alterar a tela atual para a tela com o id fornecido
        gerenciador_telas.current = id_tela

    # função para trocar a foto de perfil, chamada como parâmetro na função on_start
    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f'icones/fotos_perfil/{foto}'

        info = json.dumps({"avatar": foto})
        headers = {"Content-Type": "application/json"}
        # requisição PATCH com headers
        requisicao = requests.patch(
            f'https://apilactivovendashash-default-rtdb.firebaseio.com/{self.local_id}.json',
            data=info,
            headers=headers
        )
        if requisicao.ok:
            # print('Foto de perfil atualizada com sucesso.')
            self.mudar_tela('ajustespage')
        else:
            print('Erro ao atualizar a foto de perfil:', requisicao.json())

        self.mudar_tela('ajustespage')



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_vendedor_adicionado = None  # Inicializa o atributo com um valor padrão
        self.equipe = ""  # Inicializa o atributo equipe

    def adicionar_vendedor(self, id_vendedor_adicionado):
        self.id_vendedor_adicionado = id_vendedor_adicionado  # Define o valor do atributo
        link = f'https://apilactivovendashash-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo={self.id_vendedor_adicionado}'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        
        pagina_adicionarvendedor = self.root.ids['adicionarvendedorpage']
        mensagem_texto = pagina_adicionarvendedor.ids['mensagem_outrovendedor']

        if requisicao_dic == {}:
            mensagem_texto.text = 'Usuário não encontrado!'
        else:
            equipe = self.equipe.split(',')
            if id_vendedor_adicionado in equipe:
                mensagem_texto.text = 'Vendedor já faz parte da equipe!'
            else:
                # Adicionar o vendedor na equipe
                self.equipe += f',{id_vendedor_adicionado}'
                mensagem_texto.text = 'Vendedor adicionado com sucesso!'
                
                # Atualizar a equipe no banco de dados
                info = json.dumps({"equipe": self.equipe})
                headers = {"Content-Type": "application/json"}
                requisicao = requests.patch(
                    f'https://apilactivovendashash-default-rtdb.firebaseio.com/{self.local_id}.json',
                    data=info,
                    headers=headers
                )
                #adicionar um novo banner na lista de vendedores
                pagina_listavendedores = self.root.ids['listarvendedorespage']
                lista_vendedores = pagina_listavendedores.ids['lista_vendedores']
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_adicionado)
                lista_vendedores.add_widget(banner_vendedor)

                if not requisicao.ok:
                    print('Erro ao atualizar a equipe no banco de dados:', requisicao.json())
    

    def selecionar_cliente(self, foto, *args):
        # Pintar de branco todas as outras letras
        pagina_adicionarvendas = self.root.ids['adicionarvendaspage']
        lista_clientes = pagina_adicionarvendas.ids['lista_clientes']

        for item in list(lista_clientes.children):
            item.color = (1, 1, 1, 1)

        # Pintar de azul a letra do item selecionado
        # foto -> carrefour.png / Label -> Carrefour -> carrefour -> carrefour.png
        for item in lista_clientes.children:
            try:
                texto = item.text.lower() + '.png'
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except AttributeError:
                pass

    def selecionar_produto(self, foto, *args):
        # Pintar de branco todas as outras letras
        pagina_adicionarvendas = self.root.ids['adicionarvendaspage']
        lista_produtos = pagina_adicionarvendas.ids['lista_produtos']

        for item in list(lista_produtos.children):
            item.color = (1, 1, 1, 1)

        # Pintar de azul a letra do item selecionado
        # foto -> produto.png / Label -> Produto -> produto -> produto.png
        for item in lista_produtos.children:
            try:
                texto = item.text.lower() + '.png'
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except AttributeError:
                pass

    def selecionar_unidade(self, id_label, *args):
        pagina_adicionarvendas = self.root.ids['adicionarvendaspage']

        # Pintar de branco todas as outras letras
        pagina_adicionarvendas.ids['unidades_kg'].color = (1,1,1,1)
        pagina_adicionarvendas.ids['unidades_unidades'].color = (1,1,1,1)
        pagina_adicionarvendas.ids['unidades_litros'].color = (1,1,1,1)

        # Pintar de azul a letra do item selecionado
        pagina_adicionarvendas.ids[id_label].color = (0, 207/255, 219/255, 1)









if __name__ == "__main__":
    MainApp().run()
