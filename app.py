from flask import Flask
from flask import render_template
from flask import request

import sqlite3
from basisdata import *


app = Flask(__name__,
            template_folder='templates',
	        static_folder='static')

@app.route('/')
def singUp():
  error = ""
  return render_template('signUp.j2', error=error)

@app.route('/login', methods=["POST"])
def login():
  username = request.form["username"]
  email = request.form["email"]
  password = request.form["password"]
  rpassword = request.form["rpassword"]

  daftarUsername = User.daftarUsername()
  daftarEmail = User.daftarEmail()

  if username in daftarUsername:
    error = "Username sudah terpakai"
    return render_template('signUp.j2', error=error)
  
  if email in daftarEmail:
    error = "Email sudah terpakai"
    return render_template('signUp.j2', error=error)
  
  if password == rpassword:
     tambahUser(username, email, password)
     return render_template('login.j2') # mengarahkan ke halaman berikutnya
  else:
    error = "Password tidak sama"
    return render_template('signUp.j2', error=error) # menampilkan pesan kesalahan pada halaman yang sama

@app.route('/home', methods=["POST"])
def home():
  username = request.form["username"]
  password = request.form["password"]
  
  daftarUsername = User.daftarUsername()
  # cek username dan password 
  if username in daftarUsername:
    if password == User.cekPassword(username):
      return render_template('home.j2', username=username)
    
  
    

if __name__ == '__main__':
  app.run(host='0.0.0.0', 
          port=8000,
          debug=True)
app