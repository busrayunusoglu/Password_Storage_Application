from PyQt5.QtWidgets import QApplication
from main_page import MainPage

# Uygulamanın ana sayfasıdır. Bu sayfaya göre yönlendirmeler yapılır.

app=QApplication([])
window=MainPage()
window.show()
app.exec_()