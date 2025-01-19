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

    def disconnect(self):
        self.connection.close()
        self.connection = None

    def fetch_one(self, query, params=()):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=()):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def execute(self, query, params=()):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        return True

     # CRUD pour STUDENT

    def create_student(self, first_name, last_name, username, password, student_class=None):
        return self.execute(
            "INSERT INTO students (first_name, last_name, username, password, class) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, username, password, student_class),
        )

    def get_all_students(self):
        return self.fetch_all("SELECT * FROM students")

    def get_student_by_username(self, username):
        return self.fetch_one("SELECT * FROM students WHERE username = %s", (username,))

    def get_student_by_id(self, student_id):
        return self.fetch_one("SELECT * FROM students WHERE id = %s", (student_id,))

    def get_student_grade(self, student_id):
        return self.fetch_all(
            "SELECT * FROM grades WHERE student_id = %s",
            (student_id,),
        )

    # CRUD pour TEACHER
    def create_teacher(self, first_name, last_name, username, password, subject):
        return self.execute(
            "INSERT INTO teachers (first_name, last_name, username, password, subject) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, username, password, subject),
        )

    def get_all_teachers(self):
        return self.fetch_all("SELECT * FROM teachers")

    def get_teacher_by_username(self, username):
        return self.fetch_one("SELECT * FROM teachers WHERE username = %s", (username,))

    def get_teacher_by_id(self, teacher_id):
        return self.fetch_one("SELECT * FROM teachers WHERE id = %s", (teacher_id,))

    def add_grade(self, student_id, subject, grade, comment=None):
        return self.execute(
            "INSERT INTO grades (student_id, subject, grade, comment) VALUES (%s, %s, %s, %s)",
            (student_id, subject, grade, comment),
        )