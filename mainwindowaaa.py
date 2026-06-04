from PyQt6.QtWidgets import *
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()
    def initUI(self):
        self.resize(600, 300)
        self.setWindowTitle("Python学生成绩管理系统(By Ash)")