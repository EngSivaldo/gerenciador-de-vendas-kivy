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
           if 'vendas' in requisicao_dic:
            vendas = requisicao_dic['vendas'][1:]
            for venda in vendas:
                print(f"Venda: {venda}")
            else:
               print("Chave 'vendas' não encontrada no JSON.")
        except Exception as e:
            print(f"Erro ao processar vendas: {e}")