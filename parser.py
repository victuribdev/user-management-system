import json
import pymongo
from dataclasses import dataclass, asdict
from datetime import datetime
import time
import traceback

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    created_ts: float
    active: bool = True

def parse_roles(user_data):
    """Extrai roles de acordo com os campos is_user_*"""
    roles = []
    for key, value in user_data.items():
        if key.startswith('is_user_') and value and key != 'is_user_active':
            role = key.replace('is_user_', '')
            roles.append(role)
    return roles

def iso_to_timestamp(iso_date):
    """Converte data ISO para timestamp Unix"""
    try:
        dt = datetime.strptime(iso_date, '%Y-%m-%dT%H:%M:%SZ')
        return dt.timestamp()
    except:
        return time.time()  # Retorna timestamp atual se falhar

def parse_users(data):
    """Processa os dados para extrair usuários no formato correto"""
    users = []
    
    # Obtém a lista de usuários
    users_list = data.get('users', [])
    print(f"Encontrados {len(users_list)} usuários na lista")
    
    for i, user_data in enumerate(users_list):
        try:
            # Extrai campos específicos
            username = user_data.get('user', 'unknown')
            password = user_data.get('password', '')
            
            print(f"Processando usuário {i+1}/{len(users_list)}: {username}")
            
            # Extrai roles
            roles = parse_roles(user_data)
            
            # Obtém timezone
            timezone = user_data.get('user_timezone', 'UTC')
            
            # Cria objeto preferences
            preferences = UserPreferences(timezone=timezone)
            
            # Obtém created_at e converte para timestamp
            created_ts = iso_to_timestamp(user_data.get('created_at', ''))
            
            # Obtém active status
            active = user_data.get('is_user_active', True)
            
            user = User(
                username=username,
                password=password,
                roles=roles,
                preferences=preferences,
                created_ts=created_ts,
                active=active
            )
            
            users.append(user)
        except Exception as e:
            print(f"Erro ao processar usuário {i+1}: {e}")
            traceback.print_exc()
    
    print(f"Total de {len(users)} usuários processados com sucesso")
    return users

def insert_to_mongodb(users):
    if not users:
        print("Nenhum usuário para importar")
        return
        
    try:
        print("Conectando ao MongoDB...")
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        
        print("Acessando banco user_database...")
        db = client["user_database"]
        collection = db["users"]
        
        print("Limpando coleção existente...")
        result = collection.delete_many({})
        print(f"Documentos removidos: {result.deleted_count}")
        
        print(f"Inserindo {len(users)} usuários...")
        inserted_count = 0
        for user in users:
            user_dict = asdict(user)
            result = collection.insert_one(user_dict)
            inserted_count += 1
            if inserted_count % 10 == 0:
                print(f"Inseridos {inserted_count}/{len(users)} usuários...")
        
        print(f"{inserted_count} usuários importados com sucesso.")
        
        # Verificar se os documentos estão lá
        count = collection.count_documents({})
        print(f"Número de documentos após importação: {count}")
        
    except Exception as e:
        print(f"ERRO ao inserir no MongoDB: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        print("Abrindo arquivo udata.json...")
        with open('udata.json', 'r') as f:
            data = json.load(f)
        
        print("Arquivo carregado com sucesso!")
        print(f"Tipo de dados: {type(data)}")
        if isinstance(data, dict):
            print(f"Chaves no dicionário: {list(data.keys())}")
        
        users = parse_users(data)
        if users:
            insert_to_mongodb(users)
        else:
            print("Não foi possível extrair usuários válidos dos dados")
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        traceback.print_exc() 