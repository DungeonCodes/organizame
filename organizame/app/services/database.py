import json
import os
from app.config import Config

def init_db():
    """Inicializa os arquivos de banco de dados se não existirem"""
    os.makedirs(Config.DATA_FOLDER, exist_ok=True)
    
    # Lista de arquivos de banco de dados
    db_files = ['usuarios.json', 'pacientes.json', 'prontuarios.json', 'consultas.json']
    
    for file in db_files:
        file_path = os.path.join(Config.DATA_FOLDER, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

def read_data(file_name):
    """Lê dados de um arquivo JSON"""
    file_path = os.path.join(Config.DATA_FOLDER, file_name)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_data(file_name, data):
    """Escreve dados em um arquivo JSON"""
    file_path = os.path.join(Config.DATA_FOLDER, file_name)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_next_id(file_name):
    """Obtém o próximo ID disponível para um novo registro"""
    data = read_data(file_name)
    if not data:
        return 1
    return max(item.get('id', 0) for item in data) + 1 