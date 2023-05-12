import sqlite3

class Gambar:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return f"user(username:{self.username}, email:{self.email}, password:{self.password})"
    
    def tambahGambar(username, gambar, nama, harga, deskripsi):
    
        koneksi = sqlite3.connect("EWS.db")

        sql = f"""INSERT INTO gambar(username, gambar, nama, harga, deskripsi)
                VALUES (?, ?, ?, ?, ?);"""
        koneksi.execute(sql, (username, gambar, nama, harga, deskripsi))
        koneksi.commit()
        koneksi.close()

    def ubahBarang(id, gambar, nama, harga, deskripsi):
        koneksi = sqlite3.connect("EWS.db")

        sql = f"""UPDATE gambar
              SET gambar=?,
                  nama=?,
                  harga=?,
                  deskripsi=?
              WHERE id=?;"""
        koneksi.execute(sql, (gambar, nama, harga, deskripsi, id))
        koneksi.commit()
        koneksi.close()

    def ambilSatuBarang (id):
        conn = sqlite3.connect('EWS.db')
        cursor = conn.cursor()
        cursor.execute('SELECT gambar, nama, harga, deskripsi, id FROM gambar WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()

        return row
    
    def ambilBarangSatuToko (username):
        conn = sqlite3.connect('EWS.db')
        cursor = conn.cursor()
        cursor.execute('SELECT gambar, nama, harga, deskripsi, id FROM gambar WHERE username = ?', (username,))
        rows = cursor.fetchall()
        conn.close()

        return rows
    
    def ambilBarangTokoOrang (username):
        conn = sqlite3.connect('EWS.db')
        cursor = conn.cursor()
        cursor.execute('SELECT gambar, nama, harga, deskripsi, id FROM gambar WHERE username != ?', (username,))
        rows = cursor.fetchall()
        conn.close()

        return rows
    
    def hapusBarang(id):
  
        koneksi = sqlite3.connect("EWS.db")

        sql = f"""DELETE FROM gambar
                WHERE id=?;"""
        koneksi.execute(sql, (id,))
        koneksi.commit()

        koneksi.close()