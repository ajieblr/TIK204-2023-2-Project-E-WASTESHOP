import sqlite3

class User:
  
  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password

  def __str__(self):
    return f"user(username:{self.username}, email:{self.email}, password:{self.password})"

  def tambahUser(username, email, password):
    
    koneksi = sqlite3.connect("EWS.db")

    sql = f"""INSERT INTO user(username, email, password)
            VALUES (?, ?, ?);"""
    koneksi.execute(sql, (username, email, password))
    koneksi.commit()
    koneksi.close()

  def tampilkanSemuaUser():

    koneksi = sqlite3.connect("EWS.db")

    sql = "SELECT * FROM user;"
    kursor = koneksi.execute(sql)
    for satu_baris in kursor.fetchall():
      print(satu_baris)

    koneksi.close()

  def ambilSatuUser(id):
    koneksi = sqlite3.connect("EWS.db")

    sql = "SELECT * FROM user where id=?;"
    kursor = koneksi.execute(sql, (id, ))
    hasil = kursor.fetchone()
  
    koneksi.close()

    return hasil

  def ubahUser(id, username, email, password):
  
    koneksi = sqlite3.connect("EWS.db")

    sql = f"""UPDATE user
              SET username=?,
                  email=?,
                  password=?
              WHERE id=?;"""
    koneksi.execute(sql, (username, email, password, id))
    koneksi.commit()

    koneksi.close()

  def hapusUser(id):
  
    koneksi = sqlite3.connect("EWS.db")

    sql = f"""DELETE FROM user
            WHERE id=?;"""
    koneksi.execute(sql, (id,))
    koneksi.commit()

    koneksi.close()

  def hapusSemuaUser():

    koneksi = sqlite3.connect("EWS.db")

    sql = f"""DELETE FROM user;"""
    koneksi.execute(sql,)
    koneksi.commit()

    koneksi.close()
    print("berhasil clear data")

  def daftarId():
    koneksi = sqlite3.connect("EWS.db")
    sql = "select id from user"
    kursor = koneksi.execute(sql)
    hasil=kursor.fetchall()
    koneksi.close()
    return hasil
  
  def daftarUsername():
    koneksi = sqlite3.connect("EWS.db")
    sql = "select username from user"
    kursor = koneksi.execute(sql)
    hasil=kursor.fetchall()
    hasil = [i[0] for i in hasil]
    koneksi.close()
    return hasil
  
  def daftarEmail():
    koneksi = sqlite3.connect("EWS.db")
    sql = "select email from user"
    kursor = koneksi.execute(sql)
    hasil=kursor.fetchall()
    hasil = [i[0] for i in hasil]
    koneksi.close()
    return hasil
  
  def cekPassword(username):
    koneksi = sqlite3.connect("EWS.db")

    sql = "SELECT password FROM user where username=?;"
    kursor = koneksi.execute(sql, (username, ))
    hasil = kursor.fetchone()
  
    koneksi.close()

    return hasil[0]
  
  def cekPasswordDgEmail(email):
    koneksi = sqlite3.connect("EWS.db")

    sql = "SELECT password FROM user where email=?;"
    kursor = koneksi.execute(sql, (email, ))
    hasil = kursor.fetchone()
  
    koneksi.close()
    print(hasil[0])
    return hasil[0]