from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///soal.db"
# initialize the app with the extension
db.init_app(app)

class Absensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    tanggal = db.Column(db.Date)
    status = db.Column(db.String(10))  # New status field

    def __init__(self, nama, tanggal, status):
        self.nama = nama
        self.tanggal = tanggal
        self.status = status  # Initialize status
        
with app.app_context():
    db.create_all()