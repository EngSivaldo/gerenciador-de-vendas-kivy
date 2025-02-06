import requests
import json
from kivy.app import App

class MyFirebase():
    API_KEY = "AIzaSyAMsPQXCGqaFQRhIPb14kNbt6mrcIfjSCk"

    # Associar esta função no LabelButton/ arquivo loginpage
    def criar_conta(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'
        print(email, senha)
        info = {
            'email': email,
            'password': senha,
            'returnSecureToken': True
        }

        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            print('Usuário cadastrado!')
            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open('refreshtoken.txt', 'w') as arquivo:
                arquivo.write(refresh_token)

            # Fazer requisição no banco de dados
            try:
                req_id = requests.get("https://apilactivovendashash-default-rtdb.firebaseio.com/.json")
                req_id.raise_for_status()  # Lança uma exceção se a requisição falhar
                dados = req_id.json()

                # Supondo que o id_vendedor está dentro do dicionário 'dados' como 'proximo_id_vendedor'
                if 'proximo_id_vendedor' in dados:
                    proximo_id_vendedor = dados['proximo_id_vendedor']
                    if isinstance(proximo_id_vendedor, int):
                        novo_id_vendedor = proximo_id_vendedor
                        proximo_id_vendedor += 1
                    else:
                        raise ValueError("proximo_id_vendedor não é um inteiro")
                else:
                    print("Campo 'proximo_id_vendedor' não encontrado no dicionário.")
                    novo_id_vendedor = 1  # Valor padrão se não encontrado
                    proximo_id_vendedor = 2  # O próximo valor será 2
                
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição: {e}")
                novo_id_vendedor = 1
                proximo_id_vendedor = 2

            # Criar conta do usuário
            link = f'https://apilactivovendashash-default-rtdb.firebaseio.com/{local_id}.json'
            info_usuario = json.dumps({
                "avatar": "foto1.png", 
                "equipe": "", 
                "total_venda": "0", 
                "vendas": "", 
                "id_vendedor": novo_id_vendedor,
                "email": email
            })
            headers = {"Content-Type": "application/json"}
            requisicao_usuario = requests.patch(link, data=info_usuario, headers=headers)

            # Atualizar o valor do proximo_id_vendedor no banco de dados
            info_proximo_id_vendedor = json.dumps({"proximo_id_vendedor": proximo_id_vendedor})
            requests.patch("https://apilactivovendashash-default-rtdb.firebaseio.com/.json", data=info_proximo_id_vendedor)

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela('homepage')
        else:
            mensagem_erro = requisicao_dic['error']['message']
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids['loginpage']
            pagina_login.ids['mensagem_login'].text = mensagem_erro
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)

    # Associar esta função no LabelButton/ arquivo loginpage
    def fazer_login(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}'
        info = {
            'email': email,
            'password': senha,
            'returnSecureToken': True
        }

        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:  # Se a requisição der certo
            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open('refreshtoken.txt', 'w') as arquivo:
                arquivo.write(refresh_token)

            # Atualizar informações do usuário na interface
            try:
                dados_usuario = requests.get(f"https://apilactivovendashash-default-rtdb.firebaseio.com/{local_id}.json")
                dados_usuario.raise_for_status()
                dados_usuario_dic = dados_usuario.json()

                # Preencher ID do usuário
                id_vendedor = dados_usuario_dic.get('id_vendedor', '')
                pagina_ajustes = meu_aplicativo.root.ids['ajustespage']
                pagina_ajustes.ids['id_vendedor'].text = f'Seu ID Único: {id_vendedor}'

                # Atualizar total de vendas
                total_vendas = dados_usuario_dic.get('total_venda', '0')
                homepage = meu_aplicativo.root.ids['homepage']
                homepage.ids['label_total_vendas'].text = f'Total de Vendas: R${total_vendas}'

            except requests.exceptions.RequestException as e:
                print(f"Erro ao obter dados do usuário: {e}")

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela('homepage')  # Mudar para homepage
        else:  # Se a requisição der errado
            mensagem_erro = requisicao_dic['error']['message']
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids['loginpage']
            pagina_login.ids['mensagem_login'].text = mensagem_erro
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)

    def trocar_token(self, refresh_token):
        link = f'https://securetoken.googleapis.com/v1/token?key={self.API_KEY}'

        info = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        print("Resposta da troca de token:", requisicao_dic)

        if 'user_id' in requisicao_dic and 'id_token' in requisicao_dic:
            local_id = requisicao_dic['user_id']
            id_token = requisicao_dic['id_token']
            return local_id, id_token
        else:
            raise Exception("Erro ao trocar o token. Verifique a resposta da API.")

# Exemplo de uso
# my_firebase = MyFirebase()
# my_firebase.criar_conta('re@gmail.com', '123456')
# my_firebase.fazer_login('re@gmail.com', '123456')
