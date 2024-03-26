import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, \
    QTabWidget
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView


class WebTarayici(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 800, 600)

        self.ana_widget = QWidget(self)
        self.setCentralWidget(self.ana_widget)

        self.duzen = QVBoxLayout()
        self.ana_widget.setLayout(self.duzen)

        self.sekmeler_widget = QTabWidget()
        self.duzen.addWidget(self.sekmeler_widget)

        self.yeni_sekme_ac()

        sekmeler_duzeni = QHBoxLayout()

        self.yeni_sekme_butonu = QPushButton("Yeni Sekme")
        self.yeni_sekme_butonu.clicked.connect(self.yeni_sekme_ac)
        sekmeler_duzeni.addWidget(self.yeni_sekme_butonu)

        self.sekme_kapat_butonu = QPushButton("Sekmeyi Kapat")
        self.sekme_kapat_butonu.clicked.connect(self.sekme_kapat)
        sekmeler_duzeni.addWidget(self.sekme_kapat_butonu)

        self.githublink = QPushButton("Github")
        self.githublink.clicked.connect(self.git)

        sekmeler_duzeni.addWidget(self.githublink)

        self.duzen.addLayout(sekmeler_duzeni)

    def yeni_sekme_ac(self):
        tarayici = QWebEngineView()
        tarayici.setUrl(QUrl("https://example.com"))

        arama_cubugu = QLineEdit()
        arama_cubugu.returnPressed.connect(lambda: self.url_git(arama_cubugu))

        layout = QVBoxLayout()
        layout.addWidget(arama_cubugu)
        layout.addWidget(tarayici)

        widget = QWidget()
        widget.setLayout(layout)

        self.sekmeler_widget.addTab(widget, "Yeni Sekme")

        # Yeni sekme açıldığında tarayıcıya sayfa yüklendiğinde title'ı almak için zamanlayıcı başlatılır.
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.update_title(tarayici))
        timer.start(1000)  # Her saniyede bir kontrol edilir.

    def update_title(self, tarayici):
        title = tarayici.page().title()
        index = self.sekmeler_widget.indexOf(tarayici.parentWidget())
        self.sekmeler_widget.setTabText(index, title)

    def url_git(self, arama_cubugu):
        url = arama_cubugu.text()
        if not url.startswith("http"):
            url = "http://" + url
        elif not url.startswith("https"):
            url = "https://" + url
        self.sekmeler_widget.currentWidget().layout().itemAt(1).widget().setUrl(QUrl(url))

    def sekme_kapat(self):
        current_index = self.sekmeler_widget.currentIndex()
        if current_index != -1:
            self.sekmeler_widget.removeTab(current_index)

    def git(self):
        link = "https://github.com/0xc184/"  # Değiştirmek istediğiniz linki buraya yazın
        self.sekmeler_widget.currentWidget().layout().itemAt(1).widget().setUrl(QUrl(link))


if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = WebTarayici()
    pencere.show()
    sys.exit(uygulama.exec_())
