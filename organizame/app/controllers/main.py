from flask import Blueprint, redirect, url_for, current_app
from flask_login import login_required, current_user
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('pacientes.index'))
    else:
        return redirect(url_for('auth.login'))

# Adicione esta função para fornecer o ano atual aos templates
@main.app_context_processor
def inject_current_year():
    return {'current_year': datetime.now().year} 