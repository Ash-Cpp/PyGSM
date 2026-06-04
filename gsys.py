from PyQt6.QtWidgets import *

import sys
import util
import mainwindow
import storage

def toggleToCLI():
    util.launchIndependent("./csys.py", True)
    sys.exit(0)

def guiMainLoop() -> None:
    pass
    app = QApplication(sys.argv)
    window = mainwindow.MainWindow(app, manager=storage.FileHandler().loadFromFile())
    window.show()
    app.exec()

if __name__ == "__main__":
    guiMainLoop()