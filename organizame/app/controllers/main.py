from flask import Blueprint, redirect, url_for, current_app
from flask_login import current_user
from datetime import datetime

main = Blueprint('main', __name__)

# Rota raiz (redireciona conforme autenticação)
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('pacientes.index'))
    else:
        return redirect(url_for('auth.login'))

# Rota pública de teste (acessível sem login)
@main.route('/ping')
def ping():
    return 'Pong! Aplicação está rodando no Railway.'

# Contexto adicional para os templates
@main.app_context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}
