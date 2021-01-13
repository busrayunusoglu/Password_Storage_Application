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
class SitePasswords(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("sitePasswords.ui",self)

        # SİTE ŞİFRELERİNİ GÖRME
        self.buttonSifreyiGor.clicked.connect(self.sifreleriGetir)
        
        # SİTE BİLGİLERİNİ SİLME
        self.buttonSiteSil.clicked.connect(self.siteyiSil)

    
    # Kullanıcı aradığı sitenin şifrelerini ve site adresini görebilir.
    def sifreleriGetir(self):
        self.siteAdi = self.text1.toPlainText()

        sifreler = baglanti.execute('SELECT site_sifresi as ŞİFRE FROM site_bilgileri WHERE site_adi = %s',(self.siteAdi))
        sifreler = baglanti.fetchall()

        siteler = baglanti.execute('SELECT site_adi FROM site_bilgileri WHERE site_adi = %s',(self.siteAdi))
        siteler = baglanti.fetchall()

        if len(self.siteAdi) == 0:
            QMessageBox.warning(self, "SİTE GÖSTERİLEMEDİ", "Şifresini Görmek İstediğiniz Sitenin Adını Giriniz.")
        
        else:
            if self.siteAdi == str(siteler)[15:-3] and len(siteler) != 0:
                tempGiris =str(sifreler[0]).split(":")
                tempSifre=str.encode(tempGiris[1].replace("'","").replace("}",""))

                # Site şifreleri decrypt edilerek gösterilir.
                key = load_key()
                f = Fernet(key)
                decrypted_password = f.decrypt(tempSifre)

                self.text2.setPlainText(str(decrypted_password)[2:-1])
                db.commit()

            
                siteAdresi = baglanti.execute("SELECT site_adresi FROM site_bilgileri WHERE site_adi = %s",(self.siteAdi))
                siteAdresi = baglanti.fetchall()
                self.text4.setPlainText(str(siteAdresi)[18:-3])
                db.commit()

            else:
                self.text2.clear()
                self.text4.clear()
                QMessageBox.warning(self, "SİTE BULUNAMADI", "Bu Siteye Şifre Kaydınız Yok.")

    # Kullanıcı istediği site şifresini silebilmesini sağlar.
    def siteyiSil(self):
        self.siteAdi = self.text1.toPlainText()

        if(len(self.siteAdi) == 0):
            QMessageBox.warning(self, "SİTE SİLİNEMEDİ", "Silinecek Sitenin Adını Giriniz.")

        else:
            siteler = baglanti.execute('SELECT site_adi FROM site_bilgileri WHERE site_adi = %s',(self.siteAdi))
            siteler = baglanti.fetchall()

            if self.siteAdi != str(siteler)[15:-3] and len(siteler) == 0:
                QMessageBox.warning(self, "SİTE SİLİNEMEDİ", "Bu Siteye Şifre Kaydınız Yok.")
            else:
                baglanti.execute("DELETE FROM site_bilgileri WHERE site_adi = %s",(self.siteAdi))
                db.commit()
                QMessageBox.information(self, "SİTE SİLİNDİ", "Site Bilgileriniz Silindi.")
                self.text1.clear()
                self.text2.clear()
                self.text4.clear()
