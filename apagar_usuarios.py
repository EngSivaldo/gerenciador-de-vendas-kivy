import firebase_admin
from firebase_admin import credentials, auth

# Inicializar o Firebase Admin SDK
cred = credentials.Certificate("C:/Users/sival/Downloads/apilactivovendashash-firebase-adminsdk-fbsvc-c62dfa0aa5.json")


firebase_admin.initialize_app(cred)

# Função para apagar todos os usuários
def apagar_todos_os_usuarios():
    try:
        # Listar todos os usuários
        page = auth.list_users()
        while page:
            for user in page.users:
                print(f"Apagando usuário: {user.uid}")
                auth.delete_user(user.uid)
            page = page.get_next_page()

        print("Todos os usuários foram apagados.")
    except Exception as e:
        print(f"Erro ao apagar os usuários: {e}")

# Executar a função
apagar_todos_os_usuarios()
