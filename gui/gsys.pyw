import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from PyQt6.QtWidgets import *

import core.util as util
import core.mainwindow as mainwindow
import core.storage as storage

def toggleToCLI():
    util.launchIndependent(PROJECT_ROOT / "cli" / "csys.py", True)
    sys.exit(0)

def guiMainLoop() -> None:
    pass
    app = QApplication(sys.argv)
    fh = storage.FileHandler(PROJECT_ROOT / "data" / "studentsInfo.json")
    window = mainwindow.MainWindow(app, manager=fh.manager)
    window.show()
    app.exec()

if __name__ == "__main__":
    guiMainLoop()
