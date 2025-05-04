from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.prontuario import Prontuario
from app.models.paciente import Paciente

prontuarios = Blueprint('prontuarios', __name__, url_prefix='/prontuarios')

@prontuarios.route('/')
@login_required
def index():
    todos_prontuarios = Prontuario.get_all()
    return render_template('prontuarios/index.html', prontuarios=todos_prontuarios)

@prontuarios.route('/buscar', methods=['GET'])
@login_required
def buscar():
    cartao_sus = request.args.get('cartao_sus', '')
    if cartao_sus:
        prontuarios_list = Prontuario.get_by_cartao_sus(cartao_sus)
        if prontuarios_list:
            paciente = Paciente.get_by_cartao_sus(cartao_sus)
            return render_template('prontuarios/search_results.html', 
                                  prontuarios=prontuarios_list, 
                                  paciente=paciente)
        flash('Nenhum prontuário encontrado para este cartão SUS', 'warning')
    return redirect(url_for('prontuarios.index'))

@prontuarios.route('/novo/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
def create(paciente_id):
    paciente = Paciente.get_by_id(paciente_id)
    if not paciente:
        flash('Paciente não encontrado', 'danger')
        return redirect(url_for('pacientes.index'))
    
    if request.method == 'POST':
        historico_medico = request.form.get('historico_medico')
        alergias = request.form.get('alergias')
        medicamentos_continuos = request.form.get('medicamentos_continuos')
        
        prontuario = Prontuario.create(paciente_id, historico_medico, alergias, medicamentos_continuos)
        
        if prontuario:
            flash('Prontuário criado com sucesso!', 'success')
            return redirect(url_for('prontuarios.view', id=prontuario.id))
        else:
            flash('Erro ao criar prontuário', 'danger')
    
    return render_template('prontuarios/create.html', paciente=paciente)

@prontuarios.route('/<int:id>')
@login_required
def view(id):
    prontuario = Prontuario.get_by_id(id)
    if not prontuario:
        flash('Prontuário não encontrado', 'danger')
        return redirect(url_for('prontuarios.index'))
    
    paciente = Paciente.get_by_id(prontuario.paciente_id)
    
    from app.models.consulta import Consulta
    consultas = Consulta.get_by_prontuario_id(prontuario.id)
    
    return render_template('prontuarios/view.html', 
                          prontuario=prontuario, 
                          paciente=paciente,
                          consultas=consultas)

@prontuarios.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def edit(id):
    prontuario = Prontuario.get_by_id(id)
    if not prontuario:
        flash('Prontuário não encontrado', 'danger')
        return redirect(url_for('prontuarios.index'))
    
    paciente = Paciente.get_by_id(prontuario.paciente_id)
    
    if request.method == 'POST':
        historico_medico = request.form.get('historico_medico')
        alergias = request.form.get('alergias')
        medicamentos_continuos = request.form.get('medicamentos_continuos')
        
        prontuario = Prontuario.update(id, historico_medico, alergias, medicamentos_continuos)
        
        if prontuario:
            flash('Prontuário atualizado com sucesso!', 'success')
            return redirect(url_for('prontuarios.view', id=prontuario.id))
        else:
            flash('Erro ao atualizar prontuário', 'danger')
    
    return render_template('prontuarios/edit.html', prontuario=prontuario, paciente=paciente)

@prontuarios.route('/<int:id>/excluir', methods=['POST'])
@login_required
def delete(id):
    prontuario = Prontuario.get_by_id(id)
    if not prontuario:
        flash('Prontuário não encontrado', 'danger')
        return redirect(url_for('prontuarios.index'))
    
    paciente_id = prontuario.paciente_id
    
    if Prontuario.delete(id):
        flash('Prontuário excluído com sucesso!', 'success')
        return redirect(url_for('pacientes.view', id=paciente_id))
    else:
        flash('Erro ao excluir prontuário', 'danger')
        return redirect(url_for('prontuarios.view', id=id)) 