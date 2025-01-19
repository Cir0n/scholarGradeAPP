import mysql.connector


class Database:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.config["MYSQL_HOST"],
            user=self.config["MYSQL_USER"],
            password=self.config["MYSQL_PASSWORD"],
            database=self.config["MYSQL_DB"],
        )
        return self.connection

    def create_user(self, username, password_hash, role="student"):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
            (username, password_hash, role),
        )
        connection.commit()
        cursor.close()
        return True

    def get__all_user(self):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        return users
    

    def get_user_by_username(self, username):
        connection = self.connect() 
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def get_user_by_id(self, user_id):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
    

    def disconnect(self):
        self.connection.close()
        self.connection = None
