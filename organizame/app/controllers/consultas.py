from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.consulta import Consulta
from app.models.prontuario import Prontuario
from app.models.paciente import Paciente

consultas = Blueprint('consultas', __name__, url_prefix='/consultas')

@consultas.route('/')
@login_required
def index():
    todas_consultas = Consulta.get_all()
    return render_template('consultas/index.html', consultas=todas_consultas)

@consultas.route('/buscar', methods=['GET'])
@login_required
def buscar():
    cartao_sus = request.args.get('cartao_sus', '')
    if cartao_sus:
        consultas_list = Consulta.get_by_cartao_sus(cartao_sus)
        if consultas_list:
            paciente = Paciente.get_by_cartao_sus(cartao_sus)
            return render_template('consultas/search_results.html', 
                                  consultas=consultas_list, 
                                  paciente=paciente)
        flash('Nenhuma consulta encontrada para este cartão SUS', 'warning')
    return redirect(url_for('consultas.index'))

@consultas.route('/nova/<int:prontuario_id>', methods=['GET', 'POST'])
@login_required
def create(prontuario_id):
    prontuario = Prontuario.get_by_id(prontuario_id)
    if not prontuario:
        flash('Prontuário não encontrado', 'danger')
        return redirect(url_for('prontuarios.index'))
    
    paciente = Paciente.get_by_id(prontuario.paciente_id)
    
    if request.method == 'POST':
        medico = request.form.get('medico')
        sintomas = request.form.get('sintomas')
        diagnostico = request.form.get('diagnostico')
        prescricao = request.form.get('prescricao')
        observacoes = request.form.get('observacoes')
        
        consulta = Consulta.create(prontuario_id, medico, sintomas, diagnostico, prescricao, observacoes)
        
        if consulta:
            flash('Consulta registrada com sucesso!', 'success')
            return redirect(url_for('consultas.view', id=consulta.id))
        else:
            flash('Erro ao registrar consulta', 'danger')
    
    return render_template('consultas/create.html', prontuario=prontuario, paciente=paciente)

@consultas.route('/<int:id>')
@login_required
def view(id):
    consulta = Consulta.get_by_id(id)
    if not consulta:
        flash('Consulta não encontrada', 'danger')
        return redirect(url_for('consultas.index'))
    
    prontuario = Prontuario.get_by_id(consulta.prontuario_id)
    paciente = Paciente.get_by_id(prontuario.paciente_id)
    
    return render_template('consultas/view.html', 
                          consulta=consulta, 
                          prontuario=prontuario,
                          paciente=paciente)

@consultas.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def edit(id):
    consulta = Consulta.get_by_id(id)
    if not consulta:
        flash('Consulta não encontrada', 'danger')
        return redirect(url_for('consultas.index'))
    
    prontuario = Prontuario.get_by_id(consulta.prontuario_id)
    paciente = Paciente.get_by_id(prontuario.paciente_id)
    
    if request.method == 'POST':
        medico = request.form.get('medico')
        sintomas = request.form.get('sintomas')
        diagnostico = request.form.get('diagnostico')
        prescricao = request.form.get('prescricao')
        observacoes = request.form.get('observacoes')
        
        consulta = Consulta.update(id, medico, sintomas, diagnostico, prescricao, observacoes)
        
        if consulta:
            flash('Consulta atualizada com sucesso!', 'success')
            return redirect(url_for('consultas.view', id=consulta.id))
        else:
            flash('Erro ao atualizar consulta', 'danger')
    
    return render_template('consultas/edit.html', 
                          consulta=consulta, 
                          prontuario=prontuario,
                          paciente=paciente)

@consultas.route('/<int:id>/excluir', methods=['POST'])
@login_required
def delete(id):
    consulta = Consulta.get_by_id(id)
    if not consulta:
        flash('Consulta não encontrada', 'danger')
        return redirect(url_for('consultas.index'))
    
    prontuario_id = consulta.prontuario_id
    
    if Consulta.delete(id):
        flash('Consulta excluída com sucesso!', 'success')
        return redirect(url_for('prontuarios.view', id=prontuario_id))
    else:
        flash('Erro ao excluir consulta', 'danger')
        return redirect(url_for('consultas.view', id=id)) 