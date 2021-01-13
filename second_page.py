from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import pymysql.cursors
import mysql.connector
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
# generate_key()

def load_key():
    return open("secret.key", "rb").read()

# Veritabanı bağlantı bilgileri
db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sifre_saklama',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# İşaretçimizi oluşturalım
baglanti = db.cursor()

class SecondPage(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("second_page.ui",self)

        # KULLANICI EKLEME
        self.buttonKaydol.clicked.connect(self.ekle)
    
    # Kullanıcı ekleme işlemi yapılır.
    def ekle(self):
        self.userName = self.text1.toPlainText()
        self.password = self.text2.text() 
        
        # Şifre encrypt edilerek kayıt işlemi gerçekleşir.
        key = load_key()
        encoded_password = self.password.encode()
        f = Fernet(key)
        encrypted_password = f.encrypt(encoded_password)

        kontrol2 = baglanti.execute('SELECT * FROM kullanici_bilgileri')
        kontrol2 = baglanti.fetchall() 

        if len(self.userName) == 0 or len(encrypted_password) == 0 :
            QMessageBox.warning(self, "KAYIT BAŞARISIZ", "Eksik Alanları Doldurunuz.")

        else:
            
            if len(kontrol2) == 0:
                baglanti.execute('INSERT INTO kullanici_bilgileri VALUES(%s,%s)',(self.userName,encrypted_password))
                db.commit()
                QMessageBox.information(self, "KAYIT BAŞARILI", "Kaydınız Başarıyla Gerçekleşti.")
                self.text1.clear()
                self.text2.clear()
                self.hide()
                
            else:
                QMessageBox.warning(self, "BİLGİ", "Kaydınız Zaten Var.")
                self.hide()

