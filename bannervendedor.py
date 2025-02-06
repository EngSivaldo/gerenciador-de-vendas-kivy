from botoes import ImageButton, LabelButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
import requests

class BannerVendedor(FloatLayout):
    id_vendedor = StringProperty('')

    def __init__(self, **kwargs):
        self.id_vendedor = kwargs.get('id_vendedor', '')
        super().__init__(**kwargs)
        
        with self.canvas:
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        print(f'Buscando dados para id_vendedor: {self.id_vendedor}')
        
        link = f'https://apilactivovendashash-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo={self.id_vendedor}'
        requisicao = requests.get(link)
        print(f'Status da resposta: {requisicao.status_code}')
        requisicao_dic = requisicao.json()

        # Convertendo dict_values para uma lista e acessando o primeiro elemento corretamente
        valor = list(requisicao_dic.values())[0]
        avatar = valor['avatar']
        total_venda = valor['total_venda']

        imagem = ImageButton(source=f'icones/fotos_perfil/{avatar}', pos_hint={'right': 0.4, 'top': 0.9}, size_hint=(0.3, 0.8))
        label_id = LabelButton(text=f'ID Vendedor: {self.id_vendedor}', pos_hint={'right': 0.9, 'top': 0.9}, size_hint=(0.5, 0.5))
        label_total = LabelButton(text=f'Total de vendas: {total_venda}', pos_hint={'right': 0.9, 'top': 0.6}, size_hint=(0.5, 0.5))

        self.add_widget(imagem)
        self.add_widget(label_id)
        self.add_widget(label_total)

        for key, vendedor in requisicao_dic.items():
            print(f'Vendedor encontrado: {vendedor}')

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size
