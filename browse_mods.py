import urllib
import urllib2
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QUrl, SIGNAL
from PyQt4.QtWebKit import QWebView, QWebPage


WEBSITE_ADDRESS = "http://beta.kerbalstuff.com"


class BrowseMods(QtGui.QVBoxLayout):
    def __init__(self, QWidget=None):
        QtGui.QVBoxLayout.__init__(self, QWidget)
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
            download_file(downloadUrl, "raw_mods/mod.zip")


def download_file(url, file_name=None):
    #url = "http://download.thinkbroadband.com/10MB.zip"
    if file_name is None:
        file_name = url.split('/')[-1] + ".zip"

    urllib.urlretrieve(url, file_name)
