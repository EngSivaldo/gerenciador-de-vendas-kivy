from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

class BannerVenda(GridLayout):
    def __init__(self, **kwargs):
        # Inicializa a classe pai GridLayout
        super().__init__()
        self.rows = 1  # Definindo o número de linhas do layout

        # Definindo um fundo preto para o banner
        with self.canvas:
            Color(rgb=(0, 0, 0, 1))  # Definindo a cor preta
            self.rec = Rectangle(size=self.size, pos=self.pos)  # Criando um retângulo que cobre o fundo do layout
        # Vinculando atualizações de posição e tamanho do layout à função atualizar_rec
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        # Extraindo informações dos argumentos passados para a classe
        cliente = kwargs['cliente']
        foto_cliente = kwargs['foto_cliente']
        produto = kwargs['produto']
        foto_produto = kwargs['foto_produto']
        data = kwargs['data']
        unidade = kwargs['unidade']
        quantidade = kwargs['quantidade']
        preco = kwargs['preco']

        # Seção esquerda do layout, contendo a imagem e o nome do cliente
        esquerda = FloatLayout()
        esquerda_imagem = Image(pos_hint={'right': 1, 'top': 0.95}, size_hint=(1, 0.75), source=f'icones/fotos_clientes/{foto_cliente}')
        esquerda_label = Label(text=cliente, size_hint=(1, 0.2), pos_hint={'right': 1, 'top': 0.2})
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)

        # Seção do meio do layout, contendo a imagem e o nome do produto
        meio = FloatLayout()
        meio_imagem = Image(pos_hint={'right': 1, 'top': 0.95}, size_hint=(1, 0.75), source=f'icones/fotos_produtos/{foto_produto}')
        meio_label = Label(text=produto, size_hint=(1, 0.2), pos_hint={'right': 1, 'top': 0.2})
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)

        # Seção direita do layout, contendo data, preço e quantidade do produto
        direita = FloatLayout()
        direita_label_data = Label(text=f'Data: {data}', size_hint=(1, 0.33), pos_hint={'right': 1, 'top': 0.9})
        direita_label_preco = Label(text=f'Preço: {preco:.2f}', size_hint=(1, 0.33), pos_hint={'right': 1, 'top': 0.65})
        direita_label_quantidade = Label(text=f'Quantidade: {quantidade} {unidade}', size_hint=(1, 0.33), pos_hint={'right': 1, 'top': 0.4})
        direita.add_widget(direita_label_data)
        direita.add_widget(direita_label_preco)
        direita.add_widget(direita_label_quantidade)

        # Adicionando as três seções (esquerda, meio e direita) ao GridLayout
        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_rec(self, *args):
        # Atualiza a posição e o tamanho do retângulo de fundo quando o layout muda
        self.rec.pos = self.pos
        self.rec.size = self.size
