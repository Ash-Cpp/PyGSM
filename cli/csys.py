"""
csys.py
function: CLI主逻辑
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import core.stream as stream
import core.storage as storage
import core.util as util
import core.models as models

def getVaildChoose(n: int, InputInfo="请输入您的操作:", errorInfo="操作无效!!!") -> int:
    """获取合法控制台输入

    Args:
        n (int): 合法区间范围(1~n)
        InputInfo (str, optional): 输入提示. Defaults to "请输入您的操作:".
        errorInfo (str, optional): 错误提示. Defaults to "操作无效!!!".

    Raises:
        choice: _description_

    Returns:
        int: _description_
    """
    while True:
        try:
            choice = int(input(InputInfo))
            if choice in range(1, n + 1):
                return choice
            raise ValueError
        except ValueError:
            print(errorInfo)

def waitEnter(info = "回车以继续操作...") -> None:
    input(info)

def subShowAll():
    """展示总表
    """
    stream.printStudentsTable(Manager.getSortedList())

def subAdd():
    """添加学生模块
    """
    addLoopFlag = [ True ]
    print("按下[Ctrl+C]即可退出添加")
    while addLoopFlag[0]:
        try:
            sid = input("请输入学生学号:")
            name = input("请输入学生姓名:")
            g1, g2, g3 = map(float, input("请分别输入语数英成绩(按照逗号分隔):").split(","))
            student = models.Student(name, sid, {
                "语文" : g1,
                "数学" : g2,
                "英语" : g3
            })
            Manager.add(student)
            print("添加成功!!!")
            stream.printStudent(student)
            FHandler.saveToFile()
        except KeyboardInterrupt:
            print("您终止了操作")
            subBack(addLoopFlag)
        except ValueError as e:
            print(e)
            subBack(addLoopFlag)

def subRemove():
    removeOptions = ["指定学号删除", "指定姓名删除(同名也会删除)"]
    removeLoopFlag = [ True ]
    print("按下[Ctrl+C]即可退出删除")
    stream.printOptions(removeOptions)
    while removeLoopFlag[0]:    
        try:
            op = getVaildChoose(2, "当前在'删除'菜单,请输入您的操作:")
            if op == 1:
                sid = input("请输入您想删除学生的学号:")
                Manager.removeBySid(sid)
            else:
                name = input("请输入您想删除学生的姓名")
                Manager.removeByName(name)
            print("删除成功!!!")
            FHandler.saveToFile()
        except KeyboardInterrupt:
            print("您终止了操作")
            subBack(removeLoopFlag)
        except ValueError as e:
            print(e)
            subBack(removeLoopFlag)

def subUpdate():
    updateLoopFlag = [ True ]
    print("按下[Ctrl+C]即可退出更新")
    while updateLoopFlag[0]:
        try:
            sid = input("请输入您想更新学生的学号:")
            student = Manager.selectBySid(sid)
            print("有以下记录")
            stream.printStudent(student)
            while True:
                subject, newVal = input("请输入想修改的科目与新的分数(逗号分开):").split(",")
                Manager.updateGrade(sid, subject, float(newVal))
                print("更新成功!!!")
                stream.printStudent(student)
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print("您终止了操作")
            subBack(updateLoopFlag)

def subQuery():
    pass

def subBack(LoopFlagPtr: list):
    LoopFlagPtr[0] = False

def subCURD():
    curdOptions = ["增加学生信息", "删除学生信息", "更改学生信息", 
               "查询学生信息", "查看总表", "清空历史记录",
               "切换至图形界面", "返回上级菜单", "退出系统"]
    curdLoopFlag = [ True ]
    
    curdRouter = {
        1: lambda: expectCall(subAdd, False),
        2: lambda: expectCall(subRemove, False),
        3: lambda: expectCall(subUpdate, False),
        4: lambda: expectCall(subQuery, False),
        5: lambda: expectCall(subShowAll, False),
        6: lambda: expectCall(lambda: subClearHistory(curdOptions), False),
        7: lambda: expectCall(subToggleGUI),
        8: lambda: expectCall(lambda: subBack(curdLoopFlag), False),
        9: lambda: expectCall(subExit, False)
    }
    subClearHistory(curdOptions)
    while curdLoopFlag[0]:
        try:
           op = getVaildChoose(len(curdRouter), "当前在'增删改查'菜单,请输入您的操作:")
           if curdRouter[op]():
               subClearHistory(curdOptions)
        except KeyboardInterrupt:
            print("您终止了操作")

def subClearHistory(options: list[str] = []):
    """清空操作记录并且打印新菜单

    Args:
        options (list[str]): 需要打印的菜单 
    """
    stream.clearConsole()
    stream.printOptions(options)

def subSetting():
    pass

def subToggleGUI():
    util.launchIndependent(PROJECT_ROOT / "gui" / "gsys.pyw", False)
    subExit()

def subExit(exitCode = 0):
    sys.exit(exitCode)

def expectCall(func: callable, expectVal: bool = True) -> bool:
    """
    期望调用(我也不知道叫什么,自己想出来的设计模式...)
    Args:
        func (callable): 回调函数
        expectVal (bool, optional): 期望返回值. Defaults to True.

    Returns:
        bool: _description_
    """
    func()
    return expectVal

def cliMainLoop() -> None:
    global Manager
    global FHandler
    FHandler = storage.FileHandler(PROJECT_ROOT / "data" / "studentsInfo.json")
    Manager =  FHandler.manager

    mainOptions = ["查看总表", "增删改查", "清空操作记录", 
                   "设置", "切换至图形界面", "退出系统"]
    stream.printOptions(mainOptions)
    mainRouter = {
        1: lambda: expectCall(subShowAll, False),
        2: lambda: expectCall(subCURD),
        3: lambda: expectCall(lambda: subClearHistory(mainOptions), False),
        4: lambda: expectCall(subSetting),
        5: lambda: expectCall(subToggleGUI),
        6: lambda: expectCall(subExit)
    } # 主路由
    while True:
        try:
           op = getVaildChoose(len(mainRouter), "当前在'主'菜单,请输入您的操作:")
           if mainRouter[op]():
               subClearHistory(mainOptions)
        except KeyboardInterrupt:
            print("您终止了操作")
            subExit(0)

if __name__ == "__main__":
    cliMainLoop()