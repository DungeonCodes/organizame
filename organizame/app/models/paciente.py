from app.services.database import read_data, write_data, get_next_id

class Paciente:
    def __init__(self, id, nome, cartao_sus, data_nascimento, telefone, endereco):
        self.id = id
        self.nome = nome
        self.cartao_sus = cartao_sus
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.endereco = endereco
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cartao_sus': self.cartao_sus,
            'data_nascimento': self.data_nascimento,
            'telefone': self.telefone,
            'endereco': self.endereco
        }
    
    @classmethod
    def create(cls, nome, cartao_sus, data_nascimento, telefone, endereco):
        pacientes = read_data('pacientes.json')
        
        # Verificar se o cartão SUS já está cadastrado
        if any(p['cartao_sus'] == cartao_sus for p in pacientes):
            return None
        
        id = get_next_id('pacientes.json')
        
        novo_paciente = {
            'id': id,
            'nome': nome,
            'cartao_sus': cartao_sus,
            'data_nascimento': data_nascimento,
            'telefone': telefone,
            'endereco': endereco
        }
        
        pacientes.append(novo_paciente)
        write_data('pacientes.json', pacientes)
        
        return cls(id, nome, cartao_sus, data_nascimento, telefone, endereco)
    
    @classmethod
    def get_all(cls):
        pacientes = read_data('pacientes.json')
        return [cls(**p) for p in pacientes]
    
    @classmethod
    def get_by_id(cls, id):
        pacientes = read_data('pacientes.json')
        for paciente in pacientes:
            if paciente['id'] == int(id):
                return cls(**paciente)
        return None
    
    @classmethod
    def get_by_cartao_sus(cls, cartao_sus):
        pacientes = read_data('pacientes.json')
        for paciente in pacientes:
            if paciente['cartao_sus'] == cartao_sus:
                return cls(**paciente)
        return None
    
    @classmethod
    def update(cls, id, nome, cartao_sus, data_nascimento, telefone, endereco):
        pacientes = read_data('pacientes.json')
        
        for i, paciente in enumerate(pacientes):
            if paciente['id'] == int(id):
                pacientes[i] = {
                    'id': int(id),
                    'nome': nome,
                    'cartao_sus': cartao_sus,
                    'data_nascimento': data_nascimento,
                    'telefone': telefone,
                    'endereco': endereco
                }
                write_data('pacientes.json', pacientes)
                return cls(**pacientes[i])
        
        return None
    
    @classmethod
    def delete(cls, id):
        pacientes = read_data('pacientes.json')
        
        for i, paciente in enumerate(pacientes):
            if paciente['id'] == int(id):
                del pacientes[i]
                write_data('pacientes.json', pacientes)
                return True
        
        return False 