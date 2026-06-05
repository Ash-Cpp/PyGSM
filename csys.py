"""
csys.py
function: CLI主逻辑
"""
from models import loadJson
from stream import *
import storage as storage
import sys
import util
import subprocess
# 简单获取合法数字输入
def getVaildChoose(n, inPrompt = "请输入您的操作:", errPrompt = "操作无效") -> int:
    while True:
        try:
            choice = int(input(inPrompt))
            if choice in range(1, n + 1):
                return choice
            else:
                print(errPrompt)
        except ValueError:
            print(errPrompt)
# 查找模块
def searchLoop() -> None:
    printOptions(["通过学号查询", "通过姓名查询", "展示总表", "退出"])
    while True:
        choice = getVaildChoose(4)
        if choice == 1:
            print("通过学号查询")
            sid = input("请输入您想查询的学号:")
            try:
                result = manager.selectBySid(sid)
                print("查询成功,共有1条记录")
                printStudent(result)
            except KeyError as ke:
                print(ke)
        elif choice == 2:
            print("通过姓名查询")
            name = input("请输入您想查询的姓名:")
            try:
                result = manager.selectByName(name)
                print(f"查询成功,共有{len(result)}条记录")
                printStudentsTable(result.values())
            except KeyError as ke:
                print(ke)
        elif choice == 3:
            printStudentsTable(manager.getSortedList())
        else:
            break

# 辅助函数,省去重复清空的操作
def enterSubMoudle(func: function):
    clearConsole()
    func()
    clearConsole()
    printMenu()

# 主逻辑循环
def cliMainLoop() -> None:
    global manager
    manager = storage.FileHandler("./data/studentsInfo.json").loadFromFile()
    printMenu()
    while True:
        op = getVaildChoose(7)
        if op == 1:
            clearConsole()
            printMenu()
            printStudentsTable(manager.getSortedList())
        elif op == 5:
            enterSubMoudle(searchLoop)
        elif op == 6: 
            util.launchIndependent("./gsys.py", False)
            sys.exit(0)
        elif op == 7:
            sys.exit(0)

if __name__ == "__main__":
    cliMainLoop()