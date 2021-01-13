from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import pymysql.cursors
import mysql.connector
from PyQt5 import QtGui
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

class AddSite(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("addSite.ui",self)
        
        # SİTE EKLEME
        self.buttonSiteEkle.clicked.connect(self.siteEkle)
            
    # Kullanıcının site bilgileri eklemesi sağlanır.
    def siteEkle(self):
        self.siteAdi = self.text1.toPlainText()
        self.siteAdresi = self.text2.toPlainText()
        self.siteSifresi = self.text3.text()
        
        if len(self.siteAdi) == 0 or len(self.siteAdresi) == 0 or len(self.siteSifresi) == 0: 
            QMessageBox.warning(self, "SİTE EKLENEMEDİ", "Eksik Alanları Doldurunuz.")

        else:
            key=load_key()
            encoded_password = self.siteSifresi.encode()
            f=Fernet(key)
            encryptedPass=f.encrypt(encoded_password)
            baglanti.execute('INSERT INTO site_bilgileri VALUES(%s,%s,%s)',(self.siteAdi,self.siteAdresi,encryptedPass))
            db.commit()
            QMessageBox.information(self, "SİTE EKLENDİ", self.siteAdi + " sitesi başarıyla eklendi.")
            self.text1.clear()
            self.text2.clear()
            self.text3.clear()

