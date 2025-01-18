from flask import Flask
from app.models.user import User
from app.views.user_views import user_bp
from app.services.user_service import get_user_by_id
from config import Config
from app.extensions import bcrypt, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Charger un utilisateur avec Flask-Login"""
    user_data = get_user_by_id(user_id) 
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['role'])
    return None



def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")


    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    app.register_blueprint(user_bp)

    return app
