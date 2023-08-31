from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Absensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    tanggal = db.Column(db.Date)
    status = db.Column(db.String(10))  # New status field

    def __init__(self, nama, tanggal, status):
        self.nama = nama
        self.tanggal = tanggal
        self.status = status  # Initialize status

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
        
@app.route('/absensi', methods=['GET'])
def get_absensi():
    records = Absensi.query.all()
    return render_template('list_absensi.html', records=records)

@app.route('/absensi/add', methods=['GET', 'POST'])
def add_absensi():
    if request.method == 'POST':
        status = request.form['status']  # Capture the status from the dropdown
        nama = request.form['nama']
        tanggal_str = request.form['tanggal']
        tanggal_obj = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
        new_record = Absensi(nama, tanggal_obj, status)  # Include status
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('get_absensi'))
    return render_template('add_absensi.html')

@app.route('/absensi/update/<int:id>', methods=['GET', 'POST'])
def update_absensi(id):
    record = Absensi.query.get_or_404(id)
    if request.method == 'POST':
        date_str = request.form['tanggal']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        record.nama = request.form['nama']
        record.tanggal = date_obj
        record.status = request.form['status']  # New 'status' field
        db.session.commit()
        return redirect(url_for('get_absensi'))
    return render_template('update_absensi.html', record=record)


@app.route('/absensi/delete/<id>', methods=['GET'])
def delete_absensi(id):
    record = Absensi.query.get(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('get_absensi'))

if __name__ == '__main__':
    app.run(debug=True)
