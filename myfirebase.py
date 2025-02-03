import requests
from kivy.app import App
import json

class MyFirebase():
    API_KEY = "AIzaSyAMsPQXCGqaFQRhIPb14kNbt6mrcIfjSCk"

    # Função para criar uma conta com email e senha
    def criar_conta(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'
        print(email, senha)
        info = {'email': email,
                'password': senha,
                'returnSecureToken': True}
        
        # Envia uma requisição POST para o link com os dados do usuário
        requisicao = requests.post(link, data=info)
        # Converte a resposta da requisição para um dicionário
        requisicao_dic = requisicao.json()

        # Se a requisição foi bem-sucedida
        if requisicao.ok:
            print('Usuário cadastrado!')
            # Obtém o valor de 'refreshToken' do dicionário 'requisicao_dic' e o atribui à variável 'refresh_token'
            refresh_token = requisicao_dic['refreshToken']
            # Obtém o valor de 'localId' do dicionário 'requisicao_dic' e o atribui à variável 'local_id'
            local_id = requisicao_dic['localId']
            # Obtém o valor de 'idToken' do dicionário 'requisicao_dic' e o atribui à variável 'id_token'
            id_token = requisicao_dic['idToken']

            # Obtém a instância do aplicativo que está em execução
            meu_aplicativo = App.get_running_app()
            # Atribui o valor da variável 'local_id' ao atributo 'local_id' do aplicativo
            meu_aplicativo.local_id = local_id
            # Atribui o valor da variável 'id_token' ao atributo 'id_token' do aplicativo
            meu_aplicativo.id_token = id_token

            # Abre (ou cria, se não existir) o arquivo 'refreshtoken.txt' em modo de escrita ('w')
            with open('refreshtoken.txt', 'w') as arquivo:
                # Escreve o conteúdo da variável 'refresh_token' dentro do arquivo
                arquivo.write(refresh_token)

            # Cria um usuário no banco de dados Firebase Realtime Database
            link = f'https://apilactivovendashash-default-rtdb.firebaseio.com/{local_id}.json'
            info_usuario = json.dumps({"avatar": "foto10.png", "equipe": "", "total_venda": "0", "vendas": ""})
            headers = {"Content-Type": "application/json"}
            requisicao_usuario = requests.patch(link, data=info_usuario, headers=headers)
            # Muda a tela do aplicativo para 'homepage'
            meu_aplicativo.mudar_tela('homepage')

        else:
            # Mensagem de erro caso a requisição falhe
            mensagem_erro = requisicao_dic['error']['message']
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids['loginpage']
            pagina_login.ids['mensagem_login'].text = mensagem_erro
            pagina_login.ids['mensagem_login'].color = (1,0,0,1)
        
        # Imprime o dicionário da resposta da requisição
        print(requisicao_dic)

    


def fazer_login(self, email, senha):
    pass

