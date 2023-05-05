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
                VALUES (?, ?, ?);"""
        koneksi.execute(sql, (username, gambar, nama, harga, deskripsi))
        koneksi.commit()
        koneksi.close()