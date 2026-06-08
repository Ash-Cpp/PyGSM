"""
mainwindow.py: 主窗口
"""
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import core.storage as storage

class MainWindow(QWidget):
    def __init__(self, app, fhandle: storage.FileHandler, manager: storage.GradeManager):
        super().__init__()
        self.app = app
        self.Manager = manager
        self.FHandle = fhandle
        self.dataTable = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyGSM(ByAsh)")
        self.setFixedSize(800, 600)

        MainLayout = QVBoxLayout(self)
        ButtonsLayout = QHBoxLayout(self)

        self.addBtn = QPushButton("添加学生")
        self.removeBtn = QPushButton("删除当前学生")
        self.selectBtn = QPushButton("查找学生")
        self.toggleBtn = QPushButton("切换至CLI界面")

        ButtonsLayout.addWidget(self.addBtn)
        ButtonsLayout.addWidget(self.removeBtn)
        ButtonsLayout.addWidget(self.selectBtn)
        ButtonsLayout.addWidget(self.toggleBtn)

        MainLayout.addLayout(ButtonsLayout)

        self.header = ["排名", "学号", "姓名", "语文", "数学", "英语", "平均分", "总分"]
        self.table = QTableWidget()
        self.table.itemChanged.connect(self.onItemChanged)
        self.flushTable()
        MainLayout.addWidget(self.table)

    def flushTable(self):
        self.table.setRowCount(0)
        self.table.clearContents()
        self.dataTable = []
        i = 1
        for s in self.Manager.getSortedList():
            row = [
                str(i),
                s.sid,
                s.name,
                f"{s['语文']:g}",
                f"{s['数学']:g}",
                f"{s['英语']:g}",
                f"{s.average:.2f}",
                f"{s.sum:g}",
            ]
            i += 1
            self.dataTable.append(row)
        self.table.setColumnCount(len(self.header))
        self.table.setRowCount(len(self.dataTable))
        self.table.setHorizontalHeaderLabels(self.header)
        for rowIdx, rowData in enumerate(self.dataTable):
            for colIdx, val in enumerate(rowData):
                item = QTableWidgetItem(val)
                if colIdx in [0, 1, 2, 6, 7]:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(rowIdx, colIdx, item)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def errorBox(self, info, title="错误提示"):
        QMessageBox.critical(None, title, info)

    def onAdd(self):
        self.table.blockSignals(True)

    def onItemChanged(self, item: QTableWidgetItem):
        col = item.column()
        row = item.row()
        if col in [0, 1, 2, 6, 7]:
            return
        curText = item.text()
        try:
            newVal = float(curText)
            if newVal == float(self.dataTable[row][col]):
                return
            sid = self.dataTable[row][1]
            subject = self.header[col] 
            self.Manager.updateGrade(sid, subject, newVal)
            self.FHandle.saveToFile()
            self.table.blockSignals(True)
            self.flushTable()
            self.table.blockSignals(False)
        except:
            self.errorBox("非数字输入")
            self.table.blockSignals(True)
            item.setText(str(self.dataTable[row][col]))
            self.table.blockSignals(False)