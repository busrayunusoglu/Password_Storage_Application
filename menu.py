from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from addSite import AddSite
from changePassword import ChangePassword
from sitePasswords import SitePasswords

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("menu.ui",self)

        # button1'e tıklandığında open_addSite fonksiyonu çalışır.
        self.button1.clicked.connect(self.open_addSite)

        # button2'ye tıklandığında open_changePassword fonksiyonu çalışır.
        self.button2.clicked.connect(self.open_changePassword)

        # button3'e tıklandığında open_sitePasswords fonksiyonu çalışır.
        self.button3.clicked.connect(self.open_sitePasswords)

        self.addSite = AddSite()
        self.changePassword = ChangePassword()
        self.sitePasswords = SitePasswords()

    # addSite sayfasına geçiş yapılır.
    def open_addSite(self):
        self.addSite.show()

    # changePassword sayfasına geçiş yapılır.
    def open_changePassword(self):
        self.changePassword.show()

    # sitePasswords sayfasına geçiş yapılır.
    def open_sitePasswords(self):
        self.sitePasswords.show()
