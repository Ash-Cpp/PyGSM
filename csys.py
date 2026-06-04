"""
csys.py
function: CLI主逻辑
"""
from models import loadJson
import storage as storage
import sys
import util as util
from stream import *
import subprocess
def cliMainLoop() -> None:
    manager = storage.FileHandler("./data/studentsInfo.json").loadFromFile()
    flag = True
    printMenu()
    while True:
        op = input("请输入您的操作:")
        clearConsole()
        if op == "1":
            printMenu()
            printStudentsTable(manager.getSortedList())
            flag = not flag
        elif op == "5":
            util.launchIndependent("./gsys.py", False)
            sys.exit(0)
        elif op == "6":
            sys.exit(0)
        else:
            printMenu()
            print("操作无效!!!")
if __name__ == "__main__":
    cliMainLoop()