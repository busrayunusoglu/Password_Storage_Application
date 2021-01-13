from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from second_page import SecondPage
from menu import Menu
from changeMasterPassword import ChangeMasterPassword
import pymysql.cursors
import mysql.connector
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QLineEdit
from qtwidgets import PasswordEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

# Kullanıcının giriş yaptığı, uygulamada açılan ilk sayfadır.

# Veritabanı bağlantı bilgileri
db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sifre_saklama',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# İşaretçimizi oluşturalım
baglanti = db.cursor()

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main_page.ui",self)

        # pushButton butonuna tıklandığında open_second_page fonksiyonu çalışır.
        self.pushButton.clicked.connect(self.open_second_page)
        self.btnKayitSil.clicked.connect(self.kayitSil)

        # buttonSifreDegistir butonuna tıklandığında open_changeMasterPassword fonksiyonu çalışır.
        self.buttonSifreDegistir.clicked.connect(self.open_changeMasterPassword)

        self.second_page=SecondPage()
        self.menu= Menu()
        self.changeMasterPassword = ChangeMasterPassword()

        # KULLANICI GİRİŞİ
        self.buttonGiris.clicked.connect(self.giris)
    
    # Kullanıcının bilgilerinin doğruluğuna göre menü sayfamıza yönlendirme yapılır.
    def giris(self):
        kullaniciAdi = self.text1.toPlainText()
        sifre = self.text2.text()

        giris2 = baglanti.execute('SELECT kullanici_adi FROM kullanici_bilgileri WHERE kullanici_adi = %s',(kullaniciAdi))
        giris2 = baglanti.fetchall()

        giris = baglanti.execute('SELECT kullanici_sifre as ŞİFRE FROM kullanici_bilgileri WHERE kullanici_adi = %s',(kullaniciAdi))
        giris = baglanti.fetchall()

        if len(kullaniciAdi) == 0 or len(sifre) == 0 : 
            QMessageBox.warning(self, "ŞİFRE DEĞİŞTİRİLEMEDİ", "Eksik Alanları Doldurunuz.")
        else:

            if kullaniciAdi==str(giris2)[20:-3] and len(giris2)!=0:
                tempGiris =str(giris[0]).split(":")
                tempSifre=str.encode(tempGiris[1].replace("'","").replace("}",""))

                # Encrypt edilen şifre ile girilen şifrenin encrypt edilmiş hali uyuşuyorsa uygulamaya giriş yapılır. 
                key = load_key()
                f = Fernet(key)
                decrypted_password = str(f.decrypt(tempSifre))[2:-1] 

                if (len(giris) == 1 and decrypted_password == sifre): 
                    self.menu.show()
                    self.hide()
                    db.commit()       
                else:
                    QMessageBox.warning(self, "GİRİŞ BAŞARISIZ", "Giriş Yapamadınız. Bilgilerinizi yanlış  girdiniz")
            else:
                QMessageBox.warning(self, "GİRİŞ BAŞARISIZ", "Giriş Yapamadınız. Bilgilerinizi yanlış  girdiniz")
   

    # second_page sayfasına geçiş için oluşturduk.
    def open_second_page(self):
        self.second_page.show()

    # changeMasterPassword sayfasına geçiş için oluşturduk.
    def open_changeMasterPassword(self):
        self.changeMasterPassword.show()

    def kayitSil(self):
        baglanti.execute('DELETE FROM kullanici_bilgileri')
        baglanti.execute('DELETE FROM site_bilgileri')
        QMessageBox.information(self, "İşlem Başarılı", "Uygulama Kaydınız Silindi.")
        

