
       #preencher equipe de vendedores
        equipe = requisicao_dic['equipe']
        lista_equipe = equipe.split(',')
        pagina_listavendedores = self.root.ids['listarvendedorespage']  #pegar id no main.kv
        lista_vendedores = pagina_listavendedores.ids['lista_vendedores'] #pegar id listavendedorespage.kv

        for id_vendedor_equipe in lista_equipe:
            if id_vendedor_equipe != '':
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe) #criar classe e  adicionar dentro da listavendedorespage.kv
                lista_vendedores.add_widget(banner_vendedor)