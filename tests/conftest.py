import sys, os
from os import environ

# #Postgres
environ['DATABASE_URL'] =  'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres_test'
environ['SECRET_KEY'] = "test_secret_key"
environ['ALGORITHM'] = "HS256"


# Linux
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../")

# Windows
# testPath = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, testPath)
# sys.path.insert(0, testPath + '\\..\\src\\')
# sys.path.insert(0, testPath + '\\..\\layers\\python\\')

#Configurar as variaveis de ambiente dos testes unitarios.
#Exemplo: os.environ['TZ'] = 'America/Sao_Paulo'
