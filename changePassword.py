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

class ChangePassword(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("changePassword.ui",self)

        # SİTE ŞİFRESİ DEĞİŞTİRME
        self.buttonSiteSifreDegistir.clicked.connect(self.siteSifreDegistir)

    # Kullanıcının site şifrelerinde değişiklik yapması sağlanır.
    def siteSifreDegistir(self):        
        self.siteAdi = self.text4.toPlainText()
        self.password = self.text1.text()
        self.newPassword = self.text2.text()
 
        sifreler = baglanti.execute('SELECT site_sifresi as ŞİFRE FROM site_bilgileri WHERE site_adi = %s',(self.siteAdi))
        sifreler = baglanti.fetchall()

        if len(self.siteAdi) == 0 or len(self.password) == 0 or len(self.newPassword) == 0: 
            QMessageBox.warning(self, "ŞİFRE DEĞİŞTİRİLEMEDİ", "Eksik Alanları Doldurunuz.")
    
        else:
            tempGiris =str(sifreler[0]).split(":")
            tempSifre=str.encode(tempGiris[1].replace("'","").replace("}",""))

            key = load_key()
            f = Fernet(key)
            decrypted_password = str(f.decrypt(tempSifre))[2:-1]

            key = load_key()
            encoded_newPassword = self.newPassword.encode()
            f = Fernet(key)
            newPassword = f.encrypt(encoded_newPassword)
            if (self.password == str(decrypted_password)) :
                baglanti.execute('UPDATE site_bilgileri SET site_sifresi = %s WHERE  site_adi = %s',(str(newPassword)[2:-1],self.siteAdi))        
                db.commit()
                QMessageBox.information(self, "ŞİFRE DEĞİŞTİRİLDİ", "Site şifresi başarıyla değiştirildi.")
                self.text1.clear()
                self.text2.clear()
                self.text4.clear()
                

            else:
                QMessageBox.warning(self, "ŞİFRE DEĞİŞTİRİLEMEDİ", "Eski şifreyi hatalı girdiniz.")
