from app import create_app
from config import Config
from app.utils.database import Database

app = create_app()

if __name__=="__main__":
    app.run(debug=True)
