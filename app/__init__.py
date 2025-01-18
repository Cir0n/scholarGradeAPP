from flask import Flask
from flask_bcrypt import Bcrypt

from app.views.user_views import user_bp

# Initialisation de Flask-Bcrypt
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialiser Bcrypt
    bcrypt.init_app(app)

    app.register_blueprint(user_bp)

    return app
