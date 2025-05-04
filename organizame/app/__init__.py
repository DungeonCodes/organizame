from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.services.database import init_db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login_manager.init_app(app)
    
    # Inicializar banco de dados
    init_db()
    
    # Registrar blueprints
    from app.controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.controllers.pacientes import pacientes as pacientes_blueprint
    app.register_blueprint(pacientes_blueprint)
    
    from app.controllers.prontuarios import prontuarios as prontuarios_blueprint
    app.register_blueprint(prontuarios_blueprint)
    
    from app.controllers.consultas import consultas as consultas_blueprint
    app.register_blueprint(consultas_blueprint)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuario import Usuario
        return Usuario.get_by_id(user_id)
    
    return app 