from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
import os



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes,models