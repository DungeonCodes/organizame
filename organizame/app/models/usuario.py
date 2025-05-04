from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.database import read_data, write_data, get_next_id

class Usuario(UserMixin):
    def __init__(self, id, nome, email, senha_hash):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
    
    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha_hash': self.senha_hash
        }
    
    @classmethod
    def create(cls, nome, email, senha):
        usuarios = read_data('usuarios.json')
        
        # Verificar se o email já está em uso
        if any(u['email'] == email for u in usuarios):
            return None
        
        id = get_next_id('usuarios.json')
        senha_hash = generate_password_hash(senha)
        
        novo_usuario = {
            'id': id,
            'nome': nome,
            'email': email,
            'senha_hash': senha_hash
        }
        
        usuarios.append(novo_usuario)
        write_data('usuarios.json', usuarios)
        
        return cls(id, nome, email, senha_hash)
    
    @classmethod
    def get_by_email(cls, email):
        usuarios = read_data('usuarios.json')
        for usuario in usuarios:
            if usuario['email'] == email:
                return cls(
                    usuario['id'],
                    usuario['nome'],
                    usuario['email'],
                    usuario['senha_hash']
                )
        return None
    
    @classmethod
    def get_by_id(cls, id):
        usuarios = read_data('usuarios.json')
        for usuario in usuarios:
            if usuario['id'] == int(id):
                return cls(
                    usuario['id'],
                    usuario['nome'],
                    usuario['email'],
                    usuario['senha_hash']
                )
        return None 