from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import pymysql.cursors
import mysql.connector
from cryptography.fernet import Fernet

# Veritabanı bağlantı bilgileri
db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sifre_saklama',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# İşaretçimizi oluşturalım
baglanti = db.cursor()

def load_key():
    return open("secret.key", "rb").read()

class ChangeMasterPassword(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("changeMasterPassword.ui",self)

        # KULLANICI ANA ŞİFRE DEĞİŞTİRME
        self.buttonSifreDegistir.clicked.connect(self.sifreDegistir)
    
    # Kullanıcının uygulamaya giriş şifresini değiştirmesi sağlanır.
    def sifreDegistir(self):
        self.password = self.text1.text()
        self.newPassword = self.text2.text()

        sifreler = baglanti.execute('SELECT kullanici_sifre as ŞİFRE FROM kullanici_bilgileri')
        sifreler = baglanti.fetchall()

        tempGiris =str(sifreler[0]).split(":")
        tempSifre=str.encode(tempGiris[1].replace("'","").replace("}",""))  
        
        if len(self.password) == 0 or len(self.newPassword) == 0 : 
            QMessageBox.warning(self, "ŞİFRE DEĞİŞTİRİLEMEDİ", "Eksik Alanları Doldurunuz.")
        else:
            key = load_key()
            f = Fernet(key)
            decrypted_password = str(f.decrypt(tempSifre))[2:-1]

            key = load_key()
            encoded_newPassword = self.newPassword.encode()
            f = Fernet(key)
            newPassword = f.encrypt(encoded_newPassword)

            if (self.password == str(decrypted_password)):
                sifreDegis = baglanti.execute('UPDATE kullanici_bilgileri SET kullanici_sifre = %s',(str(newPassword)[2:-1],))
                db.commit()
                QMessageBox.information(self, "ŞİFRE GÜNCELLENDİ", "Şifreniz başarıyla değiştirildi.")
                self.text1.clear()
                self.text2.clear()
                self.hide()
            
            else:
                QMessageBox.warning(self,"ŞİFRE DEĞİŞTİRİLEMEDİ", "Eski şifreyi hatalı girdiniz.")