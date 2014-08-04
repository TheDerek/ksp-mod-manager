from PyQt4 import QtGui
import sys

from PyQt4.QtCore import QSettings, QString
from PyQt4.QtGui import QWidget, QVBoxLayout, QLabel, QLineEdit

from browse_mods import BrowseMods
from src.url_install import URLInstall


def main():
    app = QtGui.QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout(window)

    gamedata_label = QLabel()
    gamedata_label.setText("GameData Location:")
    layout.addWidget(gamedata_label)

    settings = QSettings("AppSettings", "Strings")
    loc = settings.value("GameDataLocation", type=QString)

    gamedata_edit = QLineEdit()
    if loc is not None:
        gamedata_edit.setText(loc)
    layout.addWidget(gamedata_edit)

    tabs = QtGui.QTabWidget()

    tab1 = QtGui.QWidget()
    tab2 = QtGui.QWidget()
    tab3 = QtGui.QWidget()

    #Resize width and height
    tabs.resize(1000, 700)

    #Move QTabWidget to x:300,y:300
    tabs.move(QtGui.QApplication.desktop().screen().rect().center() - tabs.rect().center())

    #Set Layout for Tabs
    tab1.setLayout(BrowseMods(gamedata_edit))
    tab2.setLayout(URLInstall(gamedata_edit))

    tabs.addTab(tab1, "Install From Kerbal Stuff")
    tabs.addTab(tab2, "Install From URL")
    tabs.addTab(tab3, "Manage Instances")

    layout.addWidget(tabs)

    window.setWindowTitle("Kerbal Mod Launcher")
    window.show()
    #tabs.setWindowTitle("Kerbal Mod Launcher")
    #tabs.show()

    close = app.exec_()

    print("Saving settings")
    settings.setValue("GameDataLocation", gamedata_edit.text())
    del settings

    sys.exit(close)
    #sys.exit(app.exec_())


if __name__ == '__main__':
    main()

