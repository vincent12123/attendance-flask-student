- [Tutorial: Membangun Aplikasi Absensi dengan Flask dan SQLite](#tutorial-membangun-aplikasi-absensi-dengan-flask-dan-sqlite)
  - [Pendahuluan](#pendahuluan)
  - [Persiapan](#persiapan)
    - [Instalasi Paket](#instalasi-paket)
  - [Struktur Direktori](#struktur-direktori)
  - [Langkah-langkah](#langkah-langkah)
    - [Langkah 1: Inisialisasi Aplikasi Flask](#langkah-1-inisialisasi-aplikasi-flask)
    - [Langkah 2: Mendefinisikan Model Data](#langkah-2-mendefinisikan-model-data)
    - [Langkah 3: Membuat Endpoint](#langkah-3-membuat-endpoint)
    - [Langkah 4: Membuat Template HTML](#langkah-4-membuat-template-html)
      - [`list_absensi.html`](#list_absensihtml)
      - [`add_absensi.html`](#add_absensihtml)
      - [`update_absensi.html`](#update_absensihtml)
    - [Langkah 5: Menjalankan Aplikasi](#langkah-5-menjalankan-aplikasi)
  - [Penjelasan Kode](#penjelasan-kode)

# Tutorial: Membangun Aplikasi Absensi dengan Flask dan SQLite

## Pendahuluan

Dalam tutorial ini, kita akan membangun sebuah aplikasi web untuk mengelola data absensi menggunakan Flask dan SQLite sebagai basis data. Aplikasi ini akan mendukung operasi CRUD (Create, Read, Update, Delete).

## Persiapan

Pastikan Anda sudah menginstal Python dan pip. Jika belum, Anda bisa mengunduhnya dari [situs resmi Python](https://www.python.org/downloads/).

### Instalasi Paket

Buka terminal atau Command Prompt, kemudian jalankan perintah berikut:

```bash
pip install Flask
pip install Flask-SQLAlchemy
```

## Struktur Direktori

- Flask_Absensi_App/
  - app.py
  - soal.db (basis data SQLite Anda)
  - templates/
    - list_absensi.html
    - add_absensi.html
    - update_absensi.html

## Langkah-langkah

### Langkah 1: Inisialisasi Aplikasi Flask

Buka editor teks Anda dan buat file baru dengan nama `app.py`. Kemudian tambahkan kode berikut:

```python
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Tambahkan baris ini

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soal.db'
db = SQLAlchemy(app)
```

### Langkah 2: Mendefinisikan Model Data

Tambahkan kode berikut ke `app.py` untuk mendefinisikan model data dalam basis data SQLite.

```python
class Absensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    tanggal = db.Column(db.Date)
    sakit = db.Column(db.Integer)
    alpa = db.Column(db.Integer)
    izin = db.Column(db.Integer)
```

### Langkah 3: Membuat Endpoint

Sekarang, kita akan menambahkan beberapa fungsi untuk menangani operasi CRUD.

```python
# Menampilkan semua data absensi
@app.route('/absensi', methods=['GET'])
def get_absensi():
    records = Absensi.query.all()
    return render_template('list_absensi.html', records=records)

# Menambahkan data absensi baru
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

# Mengedit data absensi
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

# Menghapus data absensi
@app.route('/absensi/delete/<id>', methods=['GET'])
def delete_absensi(id):
    record = Absensi.query.get(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('get_absensi'))
```

### Langkah 4: Membuat Template HTML

Buat folder bernama `templates` di direktori yang sama dengan `app.py`. Di dalam folder ini, buat tiga file HTML: `list_absensi.html`, `add_absensi.html`, dan `update_absensi.html`.

#### `list_absensi.html`

Buat file HTML dengan nama `list_absensi.html` di folder `templates`. Isi file ini dengan kode berikut:

```html

<!DOCTYPE html>
<html>
<head>
    <title>Attendance Records</title>
</head>
<body>

<h1>Attendance Records</h1>
<a href="/absensi/add">Add New Record</a>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Date</th>
        <th>Sick</th>
        <th>Absent</th>
        <th>Permission</th>
        <th>Actions</th>
    </tr>
    {% for record in records %}
    <tr>
        <td>{{ record.id }}</td>
        <td>{{ record.nama }}</td>
        <td>{{ record.tanggal }}</td>
        <td>{{ record.sakit }}</td>
        <td>{{ record.alpa }}</td>
        <td>{{ record.izin }}</td>
        <td>
            <a href="/absensi/update/{{ record.id }}">Edit</a> |
            <a href="/absensi/delete/{{ record.id }}">Delete</a>
        </td>
    </tr>
    {% endfor %}
</table>

</body>
</html>

```

#### `add_absensi.html`

Buat file HTML dengan nama `add_absensi.html` di folder `templates`. Isi file ini dengan kode berikut:

```html

<!DOCTYPE html>
<html>
<head>
    <title>Add Attendance Record</title>
</head>
<body>

<h1>Add Attendance Record</h1>

<form action="/absensi/add" method="post">
    Name: <input type="text" name="nama"><br>
    Date: <input type="date" name="tanggal"><br>
    Sick: <input type="number" name="sakit"><br>
    Absent: <input type="number" name="alpa"><br>
    Permission: <input type="number" name="izin"><br>
    <input type="submit" value="Add">
</form>

</body>
</html>

```

#### `update_absensi.html`

Buat file HTML dengan nama `update_absensi.html` di folder `templates`. Isi file ini dengan kode berikut:

```html

<!DOCTYPE html>
<html>
<head>
    <title>Update Attendance Record</title>
</head>
<body>

<h1>Update Attendance Record</h1>

<form action="/absensi/update/{{ record.id }}" method="post">
    Name: <input type="text" name="nama" value="{{ record.nama }}"><br>
    Date: <input type="date" name="tanggal" value="{{ record.tanggal }}"><br>
    Sick: <input type="number" name="sakit" value="{{ record.sakit }}"><br>
    Absent: <input type="number" name="alpa" value="{{ record.alpa }}"><br>
    Permission: <input type="number" name="izin" value="{{ record.izin }}"><br>
    <input type="submit" value="Update">
</form>

</body>
</html>

```

### Langkah 5: Menjalankan Aplikasi

Jalankan aplikasi Anda dengan perintah berikut di terminal:

```bash
python app.py
```

Buka browser dan kunjungi `http://127.0.0.1:5000/absensi` untuk melihat aplikasi Anda.

## Penjelasan Kode

- `datetime.strptime(date_str, '%Y-%m-%d').date()` digunakan untuk mengubah string tanggal menjadi objek `date` yang bisa diterima oleh SQLite.
- `int(request.form['sakit'])` digunakan untuk mengubah input formulir ke tipe data integer.

Dengan demikian, Anda telah berhasil membuat aplikasi CRUD sederhana untuk mengelola data absensi menggunakan Flask dan SQLite. Selamat mencoba!