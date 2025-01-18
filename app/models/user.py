from flask_login import UserMixin

class User(UserMixin):
    """Classe utilisateur pour Flask-Login"""
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
