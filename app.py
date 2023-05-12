from flask import Flask,redirect, url_for, render_template, request, session, send_file, make_response
from functools import wraps
import os
from io import BytesIO
import base64
from PIL import Image

import sqlite3
from basisdata import *

app = Flask(__name__,
            template_folder='templates',
	          static_folder='static')

app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ambil data dari form login
        username = request.form['username']
        password = request.form['password']

        # Cari user di database
        try:
            pswd = User.cekPassword(username)
            # Validasi user
            if password == pswd:
                session['username'] = username
                # Redirect ke halaman home jika user valid
                return redirect(url_for('home'))
            else:
                error = 'Password salah'
                return render_template('login.j2', error=error)
        except:
            error = 'Username salah'
            return render_template('login.j2', error=error)

    # Tampilkan halaman login
    return render_template('login.j2')

@app.route('/daftar', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Ambil data dari form signup
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['rpassword']

        if username in User.daftarUsername():
            error = 'Username sudah digunakan'
            return render_template('signup.j2', error=error)
        
        if username in User.daftarEmail():
            error = 'Email sudah digunakan'
            return render_template('signup.j2', error=error)
        
        # Validasi data
        if password != repeat_password:
            error = 'Password tidak sama'
            return render_template('signup.j2', error=error)

        # Tambahkan user baru ke database
        session['username'] = username
        User.tambahUser(username, email, password)

        # Redirect ke halaman login
        return redirect(url_for('home'))

    # Tampilkan halaman signup
    return render_template('signUp.j2')

# fungsi untuk logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# decorator untuk memeriksa apakah pengguna sudah login atau belum
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/home')
def home():
    try:
        username=session['username']
        rows = Gambar.ambilBarangTokoOrang(username)

        daftar = []
        for row in rows:
            gambar = base64.b64encode(row[0]).decode('ascii')
            daftar.append((gambar, row[1], row[2], row[3], row[4]))

        return render_template('home.j2', semuaData=daftar, username=session['username'])
    except:
        return redirect(url_for('login'))

@app.route('/suka/<string:id>')
def suka(id):
    username=session['username']
    print(id)

@app.route('/detail/<string:id>')
def detail(id):
    try:
        username=session['username']
        daftar = []

        row = Gambar.ambilSatuBarang(id)
        gambar = base64.b64encode(row[0]).decode('ascii')
        daftar.append((gambar, row[1], row[2], row[3], row[4]))
        print(row)

        # for row in rows:
        #     gambar = base64.b64encode(row[0]).decode('ascii')
        #     daftar.append((gambar, row[1], row[2], row[3], row[4]))

        return render_template('detail.j2', semuaData=daftar, username=session['username'])
    except:    
        return redirect(url_for('login'))

@app.route('/toko', methods=['GET', 'POST'])
def toko():
    try:
        if request.method == 'POST':
            username=session['username']
            nama = request.form['nama']
            filename = request.files['gambar'].read()
            harga = request.form['harga']
            deskripsi = request.form['deskripsi']

            Gambar.tambahGambar(username, filename, nama, harga, deskripsi)

            rows = Gambar.ambilBarangSatuToko(username)

            daftar = []
            for row in rows:
                gambar = base64.b64encode(row[0]).decode('ascii')
                daftar.append((gambar, row[1], row[2], row[3], row[4]))

            return render_template('toko.j2', semuaData=daftar, username=session['username'])
        
        username=session['username']
        rows = Gambar.ambilBarangSatuToko(username)

        daftar = []
        for row in rows:
            gambar = base64.b64encode(row[0]).decode('ascii')
            daftar.append((gambar, row[1], row[2], row[3], row[4]))
        return render_template('toko.j2', semuaData=daftar, username=session['username'])
    except:
        return redirect(url_for('login'))

@app.route("/edit/<string:id>", methods=['GET', 'POST'])
def edit(id):
    try:
        if request.method == 'POST':
            username=session['username']
            nama = request.form['nama']
            filename = request.files['gambar'].read()
            harga = request.form['harga']
            deskripsi = request.form['deskripsi']

            Gambar.ubahBarang(id, filename, nama, harga, deskripsi)

            rows = Gambar.ambilBarangSatuToko(username)

            daftar = []
            for row in rows:
                gambar = base64.b64encode(row[0]).decode('ascii')
                daftar.append((gambar, row[1], row[2], row[3], row[4]))

            return redirect(url_for('toko'))
        # print(id)
        return render_template('editGambar.j2', username=session['username'])
    except:
        return redirect(url_for('login'))

@app.route("/hapus/<string:id>")
def hapus(id):
    try:
        Gambar.hapusBarang(id)
        print('berhasil')
        return redirect(url_for('toko'))
    except:
        return redirect(url_for('login'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgotPass():
    import smtplib
    if request.method == 'POST':
        # Ambil data dari form login
        email = request.form['email']

        password = User.cekPasswordDgEmail(email)

        sender_email = "aufarafi21@mhs.unsyiah.ac.id"
        sender_password = "Aufarafi21@mhs.unsyiah.ac.id"
        try:
            smtp_server = smtplib.SMTP('smtp.mhs.unsyiah.ac.id', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            print(1)

            msg = f'Subject: Kiriman Password\n\nYour Password: {password}'
            smtp_server.sendmail(sender_email, email, msg)

            smtp_server.quit()
            return redirect(url_for('login'))
        except:
            print('gagal')
            return render_template('signUp.j2')

    return render_template('lupaPassword.j2')


if __name__ == '__main__':
  app.run(host='0.0.0.0', 
          port=8001,
          debug=True)
app