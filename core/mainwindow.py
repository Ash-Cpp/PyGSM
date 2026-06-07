# mainwindow.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, app, manager):
        super().__init__()
        self.app = app
        self.manager = manager  # 接收 GradeManager 实例
        
        # 标记当前主题状态，默认是浅色模式
        self.is_dark_mode = False 
        
        self.initUI()
        
    def initUI(self):
        # 1. 窗口基础配置
        self.setWindowTitle("学生成绩管理系统 - GUI版本")
        self.resize(850, 520)   
        
        # 2. 全局垂直布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)
        
        # 3. 顶部工具栏（标题 + 主题切换按钮）
        top_layout = QHBoxLayout()
        self.title_label = QLabel("学生成绩排行表（按总分降序，学号升序）")
        self.title_label.setObjectName("TitleLabel") # 设置对象名方便QSS单独控制
        
        self.btn_theme = QPushButton("切换到暗色模式 🌙")
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_theme)
        main_layout.addLayout(top_layout)
        
        # 4. 初始化表格并设置自适应
        self.table_widget = QTableWidget()
        self.table_widget.setAlternatingRowColors(True)  # 开启交替行背景色
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table_widget)
        
        # 5. 底部控制区
        btn_layout = QHBoxLayout()
        self.btn_back = QPushButton("返回 CLI 命令行系统 (Op 5)")
        self.btn_exit = QPushButton("退出系统 (Op 6)")
        
        self.btn_back.setObjectName("BtnBack")
        self.btn_exit.setObjectName("BtnExit")
        
        btn_layout.addWidget(self.btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_exit)
        main_layout.addLayout(btn_layout)
        
        # 6. 绑定按钮事件
        self.btn_back.clicked.connect(self.handle_back_to_cli)
        self.btn_exit.clicked.connect(self.handle_exit)
        self.btn_theme.clicked.connect(self.toggle_theme) # 绑定主题切换
        
        # 7. 应用初始的浅色主题并加载数据
        self.apply_theme()
        self.load_students_data()

    def load_students_data(self):
        """数据加载逻辑，保持你要求的 语数英 -> 总分 -> 平均分 顺序"""
        student_list = self.manager.getSortedList()
        
        if not student_list:
            self.table_widget.setColumnCount(1)
            self.table_widget.setHorizontalHeaderLabels(["提示"])
            self.table_widget.setRowCount(1)
            self.table_widget.setItem(0, 0, QTableWidgetItem("暂无学生成绩数据"))
            return

        # 动态获取科目
        first_student = student_list[0]
        sid_key = first_student.sid
        student_info_dict = first_student.toDict().get(sid_key, {})
        subjects = list(student_info_dict.get("grades", {}).keys())
        
        # 组合表头：学号、姓名 -> 具体科目 -> 总分、平均分
        headers = ["学号", "姓名"] + subjects + ["总分", "平均分"]
        
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setRowCount(len(student_list))
        
        for row_idx, student in enumerate(student_list):
            row_data = [student.sid, student.name]
            
            for sub in subjects:
                try:
                    score = student[sub]
                    row_data.append(f"{score:g}")
                except KeyError:
                    row_data.append("-")     
            
            row_data.append(f"{student.sum:g}")
            row_data.append(f"{student.average:.2f}")
            
            for col_idx, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) 
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable) 
                self.table_widget.setItem(row_idx, col_idx, item)

    def toggle_theme(self):
        """在浅色和暗色主题之间切换"""
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.btn_theme.setText("切换到浅色模式 ☀️")
        else:
            self.btn_theme.setText("切换到暗色模式 🌙")
        self.apply_theme()

    def apply_theme(self):
        """精准应用 QSS 样式表"""
        if self.is_dark_mode:
            # ================= 暗色主题样式 (Dark Mode) =================
            dark_qss = """
                QWidget {
                    background-color: #1e1e1e;
                    color: #cfcfcf;
                    font-family: "Segoe UI", "Microsoft YaHei";
                }
                QLabel#TitleLabel {
                    font-size: 15px;
                    font-weight: bold;
                    color: #ecf0f1;
                }
                QTableWidget {
                    background-color: #252526;
                    alternate-background-color: #2d2d30;
                    gridline-color: #3f3f46;
                    border: 1px solid #3f3f46;
                    border-radius: 4px;
                }
                QHeaderView::section {
                    background-color: #333337;
                    color: #f1f1f1;
                    padding: 6px;
                    border: 1px solid #2d2d30;
                    font-weight: bold;
                }
                QTableWidget::item:selected {
                    background-color: #007acc;
                    color: white;
                }
                QPushButton {
                    background-color: #333337;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 6px 14px;
                    color: #f1f1f1;
                }
                QPushButton:hover {
                    background-color: #444449;
                }
                QPushButton#BtnBack {
                    background-color: #114b7a;
                    border: none;
                    font-weight: bold;
                }
                QPushButton#BtnBack:hover {
                    background-color: #165c96;
                }
                QPushButton#BtnExit {
                    background-color: #a93226;
                    border: none;
                    color: white;
                    font-weight: bold;
                }
                QPushButton#BtnExit:hover {
                    background-color: #c0392b;
                }
            """
            self.setStyleSheet(dark_qss)
        else:
            # ================= 浅色主题样式 (Light Mode) =================
            light_qss = """
                QWidget {
                    background-color: #f8f9fa;
                    color: #333333;
                    font-family: "Segoe UI", "Microsoft YaHei";
                }
                QLabel#TitleLabel {
                    font-size: 15px;
                    font-weight: bold;
                    color: #2c3e50;
                }
                QTableWidget {
                    background-color: #ffffff;
                    alternate-background-color: #f2f4f7;
                    gridline-color: #e2e8f0;
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                }
                QHeaderView::section {
                    background-color: #f1f5f9;
                    color: #334155;
                    padding: 6px;
                    border: 1px solid #cbd5e1;
                    font-weight: bold;
                }
                QTableWidget::item:selected {
                    background-color: #3b82f6;
                    color: white;
                }
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    padding: 6px 14px;
                    color: #333333;
                }
                QPushButton:hover {
                    background-color: #f3f4f6;
                }
                QPushButton#BtnBack {
                    background-color: #e0f2fe;
                    border: 1px solid #bae6fd;
                    color: #0369a1;
                    font-weight: bold;
                }
                QPushButton#BtnBack:hover {
                    background-color: #bae6fd;
                }
                QPushButton#BtnExit {
                    background-color: #fee2e2;
                    border: 1px solid #fecaca;
                    color: #dc2626;
                    font-weight: bold;
                }
                QPushButton#BtnExit:hover {
                    background-color: #fecaca;
                }
            """
            self.setStyleSheet(light_qss)

    def handle_back_to_cli(self):
        import core.util as util
        self.close()
        util.launchIndependent("./csys.py", True)
        sys.exit(0)

    def handle_exit(self):
        self.close()
        sys.exit(0)