import requests
import json

# URL do banco de dados Firebase
firebase_url = "https://apilactivovendashash-default-rtdb.firebaseio.com/.json"

# Função para apagar todos os dados existentes
def apagar_todos_os_dados():
    try:
        resposta = requests.delete(firebase_url)
        resposta.raise_for_status()
        print("Todos os dados foram apagados.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao apagar os dados: {e}")

# Função para adicionar dados iniciais
def adicionar_dados_iniciais():
    dados_iniciais = {
        "proximo_id_vendedor": 1
    }
    try:
        resposta = requests.patch(firebase_url, data=json.dumps(dados_iniciais))
        resposta.raise_for_status()
        print("Dados iniciais adicionados.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao adicionar dados iniciais: {e}")

# Executar as funções
apagar_todos_os_dados()
adicionar_dados_iniciais()
