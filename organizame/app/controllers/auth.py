from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pacientes.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.get_by_email(email)
        
        if usuario and usuario.check_password(senha):
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('pacientes.index'))
        
        flash('Email ou senha inválidos', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('pacientes.index'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem', 'danger')
            return render_template('auth/register.html')
        
        usuario = Usuario.create(nome, email, senha)
        
        if usuario:
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email já está em uso', 'danger')
    
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 