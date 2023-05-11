import sqlite3

def buatBasisdata():
  koneksi = sqlite3.connect("EWS.db")
  koneksi.close()

def buatTabelUser():
  koneksi = sqlite3.connect("EWS.db")

  sql = """CREATE TABLE IF NOT EXISTS user(
          id INTEGER PRIMARY KEY,
          username TEXT,
          email TEXT,
          password TEXT);"""
  koneksi.execute(sql)
  koneksi.close()

def buatTabelGambar():
  koneksi = sqlite3.connect("EWS.db")

  sql = """CREATE TABLE IF NOT EXISTS gambar (
          id INTEGER PRIMARY KEY,
          username TEXT,
          gambar BLOB,
          nama TEXT,
          harga TEXT,
          deskripsi TEXT);"""
  koneksi.execute(sql)
  koneksi.close()

def tambahUser(username, email, password):
  koneksi = sqlite3.connect("EWS.db")
  
  sql = f"""INSERT INTO user(username, email, password)
              VALUES (?, ?, ?)"""
  koneksi.execute(sql,(username, email, password))
  koneksi.commit()
  koneksi.close()

def buatTabelSuka():
  koneksi = sqlite3.connect("EWS.db")

  sql = """CREATE TABLE IF NOT EXISTS tabel_suka (
          id INTEGER PRIMARY KEY,
          username TEXT,
          id_gambar INTEGER);"""
  koneksi.execute(sql)
  koneksi.close()

def buatTabelKeranjang():
  koneksi = sqlite3.connect("EWS.db")

  sql = """CREATE TABLE IF NOT EXISTS tabel_keranjang (
          id INTEGER PRIMARY KEY,
          username TEXT,
          id_gambar INTEGER);"""
  koneksi.execute(sql)
  koneksi.close()