from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
from browse_mods import BrowseMods


def main():
    app = QtGui.QApplication(sys.argv)
    tabs = QtGui.QTabWidget()

    tab1 = QtGui.QWidget()
    tab2 = QtGui.QWidget()
    tab3 = QtGui.QWidget()

    #Resize width and height
    tabs.resize(1000, 700)

    #Move QTabWidget to x:300,y:300
    tabs.move(QtGui.QApplication.desktop().screen().rect().center() - tabs.rect().center())

    #Set Layout for Tabs
    tab1.setLayout(BrowseMods())

    tabs.addTab(tab1, "Browse Mods")
    tabs.addTab(tab2, "Installed Mods")
    tabs.addTab(tab3, "Manage Instances")

    tabs.setWindowTitle("Kerbal Mod Launcher")
    tabs.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()