from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.paciente import Paciente

pacientes = Blueprint('pacientes', __name__, url_prefix='/pacientes')

@pacientes.route('/')
@login_required
def index():
    todos_pacientes = Paciente.get_all()
    return render_template('pacientes/index.html', pacientes=todos_pacientes)

@pacientes.route('/buscar', methods=['GET'])
@login_required
def buscar():
    cartao_sus = request.args.get('cartao_sus', '')
    if cartao_sus:
        paciente = Paciente.get_by_cartao_sus(cartao_sus)
        if paciente:
            return redirect(url_for('pacientes.view', id=paciente.id))
        flash('Paciente não encontrado', 'danger')
    return redirect(url_for('pacientes.index'))

@pacientes.route('/novo', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cartao_sus = request.form.get('cartao_sus')
        data_nascimento = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        
        paciente = Paciente.create(nome, cartao_sus, data_nascimento, telefone, endereco)
        
        if paciente:
            flash('Paciente cadastrado com sucesso!', 'success')
            return redirect(url_for('pacientes.view', id=paciente.id))
        else:
            flash('Cartão SUS já cadastrado', 'danger')
    
    return render_template('pacientes/create.html')

@pacientes.route('/<int:id>')
@login_required
def view(id):
    paciente = Paciente.get_by_id(id)
    if not paciente:
        flash('Paciente não encontrado', 'danger')
        return redirect(url_for('pacientes.index'))
    
    from app.models.prontuario import Prontuario
    prontuarios = Prontuario.get_by_paciente_id(paciente.id)
    
    return render_template('pacientes/view.html', paciente=paciente, prontuarios=prontuarios)

@pacientes.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def edit(id):
    paciente = Paciente.get_by_id(id)
    if not paciente:
        flash('Paciente não encontrado', 'danger')
        return redirect(url_for('pacientes.index'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        cartao_sus = request.form.get('cartao_sus')
        data_nascimento = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        
        paciente = Paciente.update(id, nome, cartao_sus, data_nascimento, telefone, endereco)
        
        if paciente:
            flash('Paciente atualizado com sucesso!', 'success')
            return redirect(url_for('pacientes.view', id=paciente.id))
        else:
            flash('Erro ao atualizar paciente', 'danger')
    
    return render_template('pacientes/edit.html', paciente=paciente)

@pacientes.route('/<int:id>/excluir', methods=['POST'])
@login_required
def delete(id):
    if Paciente.delete(id):
        flash('Paciente excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir paciente', 'danger')
    
    return redirect(url_for('pacientes.index')) 