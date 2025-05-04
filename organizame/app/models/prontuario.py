from datetime import datetime
from app.services.database import read_data, write_data, get_next_id
from app.models.paciente import Paciente

class Prontuario:
    def __init__(self, id, paciente_id, data_criacao, historico_medico, alergias, medicamentos_continuos):
        self.id = id
        self.paciente_id = paciente_id
        self.data_criacao = data_criacao
        self.historico_medico = historico_medico
        self.alergias = alergias
        self.medicamentos_continuos = medicamentos_continuos
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'data_criacao': self.data_criacao,
            'historico_medico': self.historico_medico,
            'alergias': self.alergias,
            'medicamentos_continuos': self.medicamentos_continuos
        }
    
    @property
    def paciente(self):
        return Paciente.get_by_id(self.paciente_id)
    
    @classmethod
    def create(cls, paciente_id, historico_medico, alergias, medicamentos_continuos):
        prontuarios = read_data('prontuarios.json')
        
        id = get_next_id('prontuarios.json')
        data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        novo_prontuario = {
            'id': id,
            'paciente_id': paciente_id,
            'data_criacao': data_criacao,
            'historico_medico': historico_medico,
            'alergias': alergias,
            'medicamentos_continuos': medicamentos_continuos
        }
        
        prontuarios.append(novo_prontuario)
        write_data('prontuarios.json', prontuarios)
        
        return cls(**novo_prontuario)
    
    @classmethod
    def get_all(cls):
        prontuarios = read_data('prontuarios.json')
        return [cls(**p) for p in prontuarios]
    
    @classmethod
    def get_by_id(cls, id):
        prontuarios = read_data('prontuarios.json')
        for prontuario in prontuarios:
            if prontuario['id'] == int(id):
                return cls(**prontuario)
        return None
    
    @classmethod
    def get_by_paciente_id(cls, paciente_id):
        prontuarios = read_data('prontuarios.json')
        return [cls(**p) for p in prontuarios if p['paciente_id'] == int(paciente_id)]
    
    @classmethod
    def get_by_cartao_sus(cls, cartao_sus):
        paciente = Paciente.get_by_cartao_sus(cartao_sus)
        if not paciente:
            return []
        
        return cls.get_by_paciente_id(paciente.id)
    
    @classmethod
    def update(cls, id, historico_medico, alergias, medicamentos_continuos):
        prontuarios = read_data('prontuarios.json')
        
        for i, prontuario in enumerate(prontuarios):
            if prontuario['id'] == int(id):
                prontuarios[i].update({
                    'historico_medico': historico_medico,
                    'alergias': alergias,
                    'medicamentos_continuos': medicamentos_continuos
                })
                write_data('prontuarios.json', prontuarios)
                return cls(**prontuarios[i])
        
        return None
    
    @classmethod
    def delete(cls, id):
        prontuarios = read_data('prontuarios.json')
        
        for i, prontuario in enumerate(prontuarios):
            if prontuario['id'] == int(id):
                del prontuarios[i]
                write_data('prontuarios.json', prontuarios)
                return True
        
        return False 