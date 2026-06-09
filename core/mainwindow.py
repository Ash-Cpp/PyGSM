"""
mainwindow.py: 主窗口
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import core.storage as storage
import core.util as util
from core.models import Student

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

        mainLayout = QVBoxLayout(self)
        buttonsLayout = QHBoxLayout(self)

        self.addBtn = QPushButton("添加学生")
        self.removeBtn = QPushButton("删除当前学生")
        self.selectBtn = QPushButton("查找学生")
        self.toggleBtn = QPushButton("切换至CLI界面")


        buttonsLayout.addWidget(self.addBtn)
        buttonsLayout.addWidget(self.removeBtn)
        buttonsLayout.addWidget(self.selectBtn)
        buttonsLayout.addWidget(self.toggleBtn)

        self.addBtn.clicked.connect(self.onAdd)
        self.toggleBtn.clicked.connect(self.toggleToCLI)
        self.removeBtn.clicked.connect(self.onRemove)
        self.selectBtn.clicked.connect(self.onSelect)

        mainLayout.addLayout(buttonsLayout)

        self.header = ["排名", "学号", "姓名", "语文", "数学", "英语", "平均分", "总分"]
        self.table = QTableWidget()
        self.table.itemChanged.connect(self.onItemChanged)
        self.flushTable()
        mainLayout.addWidget(self.table)
    
    def lightRow(self, row: int):
        """高亮指定行并滚动到该行

        Args:
            row (int): 行索引
        """
        self.table.selectRow(row)
        index = self.table.model().index(row, 0)
        self.table.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtTop)

    def onAdd(self):
        """添加学生
        """
        sid, ok1 = QInputDialog.getText(self, "提示", "输入学生学号")
        if ok1 and sid:
            name, ok2 = QInputDialog.getText(self, "提示", "输入学生姓名")
            if name and ok2:
                try:
                    s = Student(name, sid, grades={
                        "语文": 0,
                        "数学": 0,
                        "英语": 0
                    })
                    self.Manager.add(s)
                    self.FHandle.saveToFile()
                    newRow = self.flushTable(sid)
                    self.turnTo(newRow)
                    self.infoBox("添加成功!!!")
                except Exception as e:
                    self.errorBox(str(e))

    def onRemove(self):
        """删除当前选中的学生
        """
        curRow = self.table.currentRow()
        if curRow != -1:
            sid = self.dataTable[curRow][1]
            try:
                self.Manager.removeBySid(sid)
                self.FHandle.saveToFile()
                self.flushTable()
                self.infoBox("删除成功!!!")
            except Exception as e:
                self.errorBox(str(e))
    
    def onSelect(self):
        """查找学生（支持学号或姓名）
        """
        raw, ok = QInputDialog.getText(self, "提示", "输入学生学号或姓名")
        if ok and raw:
            # 先按学号查找
            for row in range(self.table.rowCount()):
                if self.dataTable[row][1] == raw:
                    self.lightRow(row)
                    return
            # 再按姓名查找
            for row in range(self.table.rowCount()):
                if self.dataTable[row][2] == raw:
                    self.lightRow(row)
                    return
            self.errorBox("未查找到该学生")

    def flushTable(self, sid: str = None) -> int:
        """刷新表格数据

        Args:
            sid (str, optional): 需要高亮的学生学号. Defaults to None.

        Returns:
            int: 高亮行的索引
        """
        self.table.setRowCount(0)
        self.table.clearContents()
        self.dataTable = []
        i = 1
        res = 0
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
            if s.sid == sid:
                res = i
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
        return res - 1

    def infoBox(self, info, title="提示"):
        QMessageBox.information(None, title, info)
    
    def errorBox(self, info, title="错误提示"):
        QMessageBox.critical(None, title, info)

    def turnTo(self, row: int, col: int = 0):
        """跳转到指定单元格

        Args:
            row (int): 行索引
            col (int, optional): 列索引. Defaults to 0.
        """
        self.table.setCurrentCell(row, col)

    def toggleToCLI(self):
        """切换至CLI界面
        """
        util.launchIndependent(PROJECT_ROOT / "cli" / "csys.py", True)
        sys.exit(0)

    def onItemChanged(self, item: QTableWidgetItem):
        """表格编辑回调

        Args:
            item (QTableWidgetItem): 被编辑的单元格
        """
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
            newRank = self.flushTable(sid)
            self.turnTo(newRank, col)
        except:
            self.errorBox("非数字输入")
            self.table.blockSignals(True)
            item.setText(str(self.dataTable[row][col]))
        finally:
            self.table.blockSignals(False)
