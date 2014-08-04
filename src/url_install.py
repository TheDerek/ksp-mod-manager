from PyQt4 import QtGui

from PyQt4.QtGui import QLabel, QPushButton, QTextEdit, QMessageBox

from src.file_deploy_util import install_from_url, DictError


WEBSITE_ADDRESS = "http://beta.kerbalstuff.com"


class URLInstall(QtGui.QVBoxLayout):
    def __init__(self, gamedata_edit, QWidget=None):
        QtGui.QVBoxLayout.__init__(self, QWidget)
        self.gamedata_edit = gamedata_edit

        url_label = QLabel()
        url_label.setText("File URL:")
        self.addWidget(url_label)

        url_edit = QTextEdit()
        self.addWidget(url_edit)

        self.install_button = QPushButton()
        self.install_button.setText("Install From URL")
        self.addWidget(self.install_button)
        self.install_button.clicked.connect(lambda: self.install_clicked(str(url_edit.toPlainText())))

    def install_clicked(self, url):
        print("button clicked")

        #connection = httplib.HTTPConnection(str(url))
        #connection.request('HEAD', '/')
        #response = connection.getresponse()
        #if response.status != 200:
         #   QMessageBox(QMessageBox.Information, "Error", "URL is not valid", QMessageBox.Ok).exec_()

        try:
            install_from_url(url, str(self.gamedata_edit.text()))
        except DictError as e:
            print(e.value)
            QMessageBox(QMessageBox.Information, "Error", e.value, QMessageBox.Ok).exec_()





