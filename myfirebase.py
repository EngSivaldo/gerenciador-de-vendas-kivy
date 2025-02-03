import requests
from kivy.app import App


class MyFirebase():
  API_KEY = "AIzaSyAMsPQXCGqaFQRhIPb14kNbt6mrcIfjSCk"
  

  def criar_conta(self, email, senha):
    link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'
    print(email, senha)
    info = {'email': email,
            'password': senha,
            'returnSecureToken': True            
            
            }
    requisicao = requests.post(link, data=info)
    requisicao_dic = requisicao.json()

    if requisicao.ok:
      print('Usuário cadastrado!')
      #requisicao_dic['idToken'] # autenticação do usuário
     # requisicao_dic['refreshToken'] # token que mantém o usuário logado
      #requisicao_dic['localId'] #id do usuario no firebase

      # Obtém o valor de 'refreshToken' do dicionário 'requisicao_dic' e o atribui à variável 'refresh_token'
      refresh_token = requisicao_dic['refreshToken']
      # Obtém o valor de 'localId' do dicionário 'requisicao_dic' e o atribui à variável 'local_d'
      local_d = requisicao_dic['localId']
      # Obtém o valor de 'idToken' do dicionário 'requisicao_dic' e o atribui à variável 'id_token'
      id_token = requisicao_dic['idToken']

      # Obtém a instância do aplicativo que está em execução
      meu_aplicativo = App.get_running_app()
      # Atribui o valor da variável 'local_d' ao atributo 'local_id' do aplicativo
      meu_aplicativo.local_id = local_d
      # Atribui o valor da variável 'id_token' ao atributo 'id_token' do aplicativo
      meu_aplicativo.id_token = id_token


      # Abre (ou cria, se não existir) o arquivo 'refreshtoken.txt' em modo de escrita ('w')
      with open('refreshtoken.txt', 'w') as arquivo:
    # Escreve o conteúdo da variável 'refresh_token' dentro do arquivo
        arquivo.write(refresh_token)




    else:  #msg caso de errado na pagina de loginpage.kv ,label subtitle
      mensagem_erro = requisicao_dic['error']['message']
      meu_aplicativo = App.get_running_app()
      pagina_login = meu_aplicativo.root.ids['loginpage']
      pagina_login.ids['mensagem_login'].text = mensagem_erro
      pagina_login.ids['mensagem_login'].color = (1,0,0,1)
    print(requisicao_dic)
    


  def fazer_login(self, email, senha):
    pass

