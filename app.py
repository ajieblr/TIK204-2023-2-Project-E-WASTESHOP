from flask import Flask,redirect, url_for, render_template, request

import sqlite3
from basisdata import *

app = Flask(__name__,
            template_folder='templates',
	          static_folder='static')

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
        User.tambahUser(username, email, password)

        # Redirect ke halaman login
        return redirect(url_for('home'))

    # Tampilkan halaman signup
    return render_template('signUp.j2')

@app.route('/home')
def home():
    return render_template('index.html')
    print('Selamat datang di halaman home') 

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