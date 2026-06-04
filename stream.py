"""
stream.py
function: IO流处理
"""
from models import Student
from tabulate import tabulate
import os
def clearConsole():
    os.system("cls") # Python3.5后弃用
def printMenu():
    options = [
        "查看成绩总榜",
        "增加学生信息",
        "移除学生信息",
        "更改学生信息",
        "切换至GUI版本",
        "设置"
        "退出管理系统"
    ]
    i = 1
    menu = []
    header = ["操作序号", "操作说明"]
    for op in options:
        row = [
            str(i),
            f"{op}"
        ]
        menu.append(row)
        i += 1
    print(tabulate(menu, headers=header, tablefmt="rounded_grid", stralign="center", numalign="center"))
def printStudentsTable(students: list[Student]):
    header =  ["排名", "学号", "姓名", "语文", "数学", "英语", "平均分", "总分"]
    tabelData = []
    i = 1
    for s in students:
        row = [
            str(i),
            s.sid,
            s.name,
            f"{s['语文']:g}",
            f"{s['数学']:g}",
            f"{s['英语']:g}",
            f"{s.average:.2f}"
            f"{s.sum:g}",
        ]
        i += 1
        tabelData.append(row)
    print(tabulate(tabelData, headers=header, tablefmt="rounded_grid", stralign="center", numalign="center"))

def testStream():
    import storage as storage
    fh = storage.FileHandler()
    manager = fh.loadFromFile()
    printMenu()
    printStudentsTable(manager.getSortedList())
    
    
if __name__ == "__main__":
    testStream()
