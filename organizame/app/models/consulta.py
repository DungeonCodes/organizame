from datetime import datetime
from app.services.database import read_data, write_data, get_next_id
from app.models.paciente import Paciente
from app.models.prontuario import Prontuario

class Consulta:
    def __init__(self, id, prontuario_id, data_consulta, medico, sintomas, diagnostico, prescricao, observacoes):
        self.id = id
        self.prontuario_id = prontuario_id
        self.data_consulta = data_consulta
        self.medico = medico
        self.sintomas = sintomas
        self.diagnostico = diagnostico
        self.prescricao = prescricao
        self.observacoes = observacoes
    
    def to_dict(self):
        return {
            'id': self.id,
            'prontuario_id': self.prontuario_id,
            'data_consulta': self.data_consulta,
            'medico': self.medico,
            'sintomas': self.sintomas,
            'diagnostico': self.diagnostico,
            'prescricao': self.prescricao,
            'observacoes': self.observacoes
        }
    
    @property
    def prontuario(self):
        return Prontuario.get_by_id(self.prontuario_id)
    
    @classmethod
    def create(cls, prontuario_id, medico, sintomas, diagnostico, prescricao, observacoes):
        consultas = read_data('consultas.json')
        
        id = get_next_id('consultas.json')
        data_consulta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        nova_consulta = {
            'id': id,
            'prontuario_id': prontuario_id,
            'data_consulta': data_consulta,
            'medico': medico,
            'sintomas': sintomas,
            'diagnostico': diagnostico,
            'prescricao': prescricao,
            'observacoes': observacoes
        }
        
        consultas.append(nova_consulta)
        write_data('consultas.json', consultas)
        
        return cls(**nova_consulta)
    
    @classmethod
    def get_all(cls):
        consultas = read_data('consultas.json')
        return [cls(**c) for c in consultas]
    
    @classmethod
    def get_by_id(cls, id):
        consultas = read_data('consultas.json')
        for consulta in consultas:
            if consulta['id'] == int(id):
                return cls(**consulta)
        return None
    
    @classmethod
    def get_by_prontuario_id(cls, prontuario_id):
        consultas = read_data('consultas.json')
        return [cls(**c) for c in consultas if c['prontuario_id'] == int(prontuario_id)]
    
    @classmethod
    def get_by_cartao_sus(cls, cartao_sus):
        paciente = Paciente.get_by_cartao_sus(cartao_sus)
        if not paciente:
            return []
        
        prontuarios = Prontuario.get_by_paciente_id(paciente.id)
        if not prontuarios:
            return []
        
        result = []
        for prontuario in prontuarios:
            result.extend(cls.get_by_prontuario_id(prontuario.id))
        
        return result
    
    @classmethod
    def update(cls, id, medico, sintomas, diagnostico, prescricao, observacoes):
        consultas = read_data('consultas.json')
        
        for i, consulta in enumerate(consultas):
            if consulta['id'] == int(id):
                consultas[i].update({
                    'medico': medico,
                    'sintomas': sintomas,
                    'diagnostico': diagnostico,
                    'prescricao': prescricao,
                    'observacoes': observacoes
                })
                write_data('consultas.json', consultas)
                return cls(**consultas[i])
        
        return None
    
    @classmethod
    def delete(cls, id):
        consultas = read_data('consultas.json')
        
        for i, consulta in enumerate(consultas):
            if consulta['id'] == int(id):
                del consultas[i]
                write_data('consultas.json', consultas)
                return True
        
        return False 