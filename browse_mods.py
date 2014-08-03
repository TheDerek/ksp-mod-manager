import urllib
import urllib2
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QUrl, SIGNAL
from PyQt4.QtGui import QLineEdit, QLabel, QMessageBox
from PyQt4.QtWebKit import QWebView, QWebPage
from file_deploy_util import download_file, install_from_url, DictError


WEBSITE_ADDRESS = "http://beta.kerbalstuff.com"


class BrowseMods(QtGui.QVBoxLayout):
    def __init__(self, gamedata_edit, QWidget=None):
        QtGui.QVBoxLayout.__init__(self, QWidget)
        self.gamedata_edit = gamedata_edit

        web_view = QWebView()
        web_view.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        web_view.connect(web_view, SIGNAL("linkClicked(const QUrl&)"), self.link_clicked)
        web_view.load(QUrl(WEBSITE_ADDRESS))
        self.addWidget(web_view)

    def link_clicked(self, url):
        if "download" in url.encodedPath():
            downloadUrl = WEBSITE_ADDRESS + str(url.encodedPath())
            print("Download detected")
            print("Download URL: " + downloadUrl)
            try:
                install_from_url(downloadUrl, str(self.gamedata_edit.text()))
            except DictError as e:
                print(e.value)
                QMessageBox(QMessageBox.Information, "Error", e.value, QMessageBox.Yes).exec_()
            #download_file(downloadUrl, "raw_mods/mod.zip")



