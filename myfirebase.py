import requests


class MyFirebase():
  API_KEY = "AIzaSyAMsPQXCGqaFQRhIPb14kNbt6mrcIfjSCk"
  

  def criar_conta(self, email, senha):
    link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'
    print(email, senha)
    info = {'email': email,
            'senha': senha,
            'returnSecureToken': True            
            
            }
    requisicao = requests.post(link, data=info)
    requisicao_dic = requisicao.json()
    print(requisicao_dic)
    


  def fazer_login(self, email, senha):
    pass

