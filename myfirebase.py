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
    else:  #msg mudar na pagina de loginpage.kv ,label subtitle
      mensagem_erro = requisicao_dic['error']['message']
      meu_aplicativo = App.get_running_app()
      pagina_login = meu_aplicativo.root.ids['loginpage']
      pagina_login.ids['mensagem_login'].text = mensagem_erro
      pagina_login.ids['mensagem_login'].color = (1,0,0,1)


    print(requisicao_dic)
    


  def fazer_login(self, email, senha):
    pass

