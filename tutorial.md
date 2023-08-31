# Membuat Aplikasi Absensi dengan Flask dan SQLite

Dalam tutorial ini, kita akan membuat aplikasi sederhana untuk mencatat absensi menggunakan Flask dan SQLite. Aplikasi ini akan memungkinkan kita untuk menambah, mengedit, dan menghapus catatan absensi.

## Persiapan

- Pastikan Anda sudah menginstal Python 3.x dan pip di komputer Anda.
- Instal Flask dan Flask-SQLAlchemy menggunakan pip:

  ```bash
  pip install Flask
  pip install Flask-SQLAlchemy
  ```

## Struktur Direktori

```plaintext
- Flask_Absensi_App/
  - app.py
  - soal.db
  - templates/
    - list_absensi.html
    - add_absensi.html
    - update_absensi.html
```

## Langkah-langkah

### 1. Membuat Model Database (`app.py`)

Buka teks editor favorit Anda dan buat file `app.py`. Lalu, tambahkan kode berikut untuk mendefinisikan model database dan konfigurasi aplikasi Flask:

```python
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soal.db'
db = SQLAlchemy(app)

class Absensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    tanggal = db.Column(db.Date)
    sakit = db.Column(db.Integer)
    alpa = db.Column(db.Integer)
    izin = db.Column(db.Integer)
```

### 2. Membuat Template HTML

#### `list_absensi.html`

Buat file HTML dengan nama `list_absensi.html` di folder `templates`. Isi file ini dengan kode berikut:

```html
<!-- Potongan kode HTML -->
```

#### `add_absensi.html`

Buat file HTML dengan nama `add_absensi.html` di folder `templates`. Isi file ini dengan kode berikut:

```html
<!-- Potongan kode HTML -->
```

#### `update_absensi.html`

Buat file HTML dengan nama `update_absensi.html` di folder `templates`. Isi file ini dengan kode berikut:

```html
<!-- Potongan kode HTML -->
```

### 3. Menambahkan Fungsi CRUD di `app.py`

Kembali ke `app.py` dan tambahkan fungsi-fungsi CRUD (Create, Read, Update, Delete).

```python
@app.route('/absensi', methods=['GET'])
def get_absensi():
    records = Absensi.query.all()
    return render_template('list_absensi.html', records=records)

@app.route('/absensi/add', methods=['GET', 'POST'])
def add_absensi():
    if request.method == 'POST':
        date_str = request.form['tanggal']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  # Mengubah string menjadi objek date
        
        new_record = Absensi(
            nama=request.form['nama'],
            tanggal=date_obj,
            sakit=int(request.form['sakit']),
            alpa=int(request.form['alpa']),
            izin=int(request.form['izin'])
        )
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('get_absensi'))
    return render_template('add_absensi.html')

@app.route('/absensi/update/<id>', methods=['GET', 'POST'])
def update_absensi(id):
    record = Absensi.query.get(id)
    if request.method == 'POST':
        date_str = request.form['tanggal']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  # Mengubah string menjadi objek date
        
        record.nama = request.form['nama']
        record.tanggal = date_obj
        record.sakit = int(request.form['sakit'])
        record.alpa = int(request.form['alpa'])
        record.izin = int(request.form['izin'])
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
```

### 4. Menjalankan Aplikasi

1. Taruh file `soal.db` di folder yang sama dengan `app.py`.
2. Buka terminal dan navigasi ke direktori di mana `app.py` berada.
3. Jalankan perintah `python app.py`.
4. Buka browser dan masuk ke `http://127.0.0.1:5000/absensi`.

Dengan ini, Anda telah berhasil membuat aplikasi absensi sederhana dengan Flask dan SQLite!