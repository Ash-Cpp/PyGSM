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

def getValidChoose(n: int, inputInfo="请输入您的操作:", errorInfo="操作无效!!!") -> int:
    """获取合法控制台输入

    Args:
        n (int): 合法区间范围(1~n)
        inputInfo (str, optional): 输入提示. Defaults to "请输入您的操作:".
        errorInfo (str, optional): 错误提示. Defaults to "操作无效!!!".
    """
    while True:
        try:
            choice = int(input(inputInfo))
            if choice in range(1, n + 1):
                return choice
            raise ValueError
        except ValueError:
            print(errorInfo)

def subShowAll(options: list[str]):
    """展示总表
    """
    stream.printStudentsTable(Manager.getSortedList())
    if len(Manager.getSortedList()) > 30:
        stream.printOptions(options)

def subAdd():
    """添加学生模块
    """
    addLoopFlag = [ True ]
    print("按下[Ctrl+C]即可退出添加")
    while addLoopFlag[0]:
        try:
            sid = input("请输入学生学号:")
            name = input("请输入学生姓名:")
            raw = input("请分别输入语数英成绩(按照逗号分隔):")
            raw = raw.replace("，", ",").replace(" ", ",")
            g1, g2, g3 = map(float, raw.split(","))
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
    """删除学生模块
    """
    removeOptions = ["指定学号删除", "指定姓名删除(同名也会删除)", "返回"]
    removeLoopFlag = [ True ]
    print("按下[Ctrl+C]即可退出删除")
    stream.printOptions(removeOptions)
    while removeLoopFlag[0]:    
        try:
            op = getValidChoose(3, "当前在'删除'菜单,请输入您的操作:")
            if op == 1:
                sid = input("请输入您想删除学生的学号:")
                Manager.removeBySid(sid)
            elif op == 2:
                name = input("请输入您想删除学生的姓名:")
                Manager.removeByName(name)
            else:
                subBack(removeLoopFlag)
                continue
            FHandler.saveToFile()
            print("删除成功!!!")
            stream.clearConsole()
            stream.printOptions(removeOptions)
        except KeyboardInterrupt:
            print("您终止了操作")
            subBack(removeLoopFlag)
        except ValueError as e:
            print(e)
            subBack(removeLoopFlag)

def subUpdate():
    """更新学生模块
    """
    updateLoopFlag = [ True ]
    print("按下[Ctrl+C]即可退出更新")
    while updateLoopFlag[0]:
        try:
            sid = input("请输入您想更新学生的学号(输入q退出):")
            if sid == "q":
                subBack(updateLoopFlag)
                continue
            student = Manager.selectBySid(sid)
            print("有以下记录")
            stream.printStudent(student)
            while True:
                try:
                    raw = input("请输入想修改的科目与新的分数(逗号分开,输入q退出):")
                    if raw == "q":
                        break
                    raw = raw.replace("，", ",").replace(" ", ",")
                    subject, newVal = raw.split(",")
                    Manager.updateGrade(sid, subject, float(newVal))
                    FHandler.saveToFile()
                    print("更新成功!!!")
                    stream.printStudent(student)
                except ValueError:
                    print("无效输入!!!")
                except KeyError as e:
                    print(e)
        except KeyboardInterrupt:
            print("您终止了操作")
            subBack(updateLoopFlag)
        except Exception as e:
            print(e)

def subQuery():
    """查询学生模块
    """
    queryOptions = ["通过学号查询", "通过姓名查询", "返回"]
    queryLoopFlag = [ True ]

    print("按下[Ctrl+C]即可退出查询")
    stream.printOptions(queryOptions)
    while queryLoopFlag[0]:
        try:
            op = getValidChoose(3, "当前在'查询'菜单',请输入您的操作:")
            if op == 1:
                sid = input("请输入您想要查询学生的学号:")
                res = Manager.selectBySid(sid)
                print("查询到以下记录")
                stream.printStudent(res)
            elif op == 2:
                name = input("请输入您想查询的姓名:")
                res = Manager.selectByName(name)
                print("查询到以下记录")
                stream.printStudentsTable(list(res.values()))
            else:
                subBack(queryLoopFlag)
        except KeyboardInterrupt:
            print("您终止了操作")
            subBack(queryLoopFlag)
        except Exception as e:
            print(e)

def subBack(loopFlagPtr: list):
    """退出当前循环

    Args:
        loopFlagPtr (list): 包装的循环标志
    """
    loopFlagPtr[0] = False

def subCURD():
    """增删改查子菜单
    """
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
           op = getValidChoose(len(curdRouter), "当前在'增删改查'菜单,请输入您的操作:")
           if curdRouter[op]():
               subClearHistory(curdOptions)
        except KeyboardInterrupt:
            print("您终止了操作")
            subClearHistory(curdOptions)

def subClearHistory(options: list[str] = None):
    """清空操作记录并且打印新菜单

    Args:
        options (list[str]): 需要打印的菜单 
    """
    if options is None:
        options = []
    stream.clearConsole()
    stream.printOptions(options)

def subToggleGUI():
    """切换至图形界面
    """
    util.launchIndependent(PROJECT_ROOT / "gui" / "gsys.pyw", False)
    subExit()

def subExit(exitCode=0):
    """退出系统

    Args:
        exitCode (int, optional): 退出码. Defaults to 0.
    """
    sys.exit(exitCode)

def expectCall(func: callable, expectVal: bool = True) -> bool:
    """
    期望调用(我也不知道叫什么,自己想出来的设计模式...)
    Args:
        func (callable): 回调函数
        expectVal (bool, optional): 期望返回值. Defaults to True.
    """
    func()
    return expectVal

def cliMainLoop() -> None:
    global Manager
    global FHandler
    global CHandler
    FHandler = storage.FileHandler(PROJECT_ROOT / "data" / "studentsInfo.json")
    CHandler = storage.ConfigHandle(PROJECT_ROOT / "config.json")
    Manager =  FHandler.manager
    CHandler.setLastMode("cli")

    mainOptions = ["查看总表", "增删改查", "清空操作记录", 
                   "切换至图形界面", "退出系统"]
    stream.printOptions(mainOptions)
    mainRouter = {
        1: lambda: expectCall(subShowAll, False),
        2: lambda: expectCall(subCURD),
        3: lambda: expectCall(lambda: subClearHistory(mainOptions), False),
        4: lambda: expectCall(subToggleGUI),
        5: lambda: expectCall(subExit)
    } # 主路由
    while True:
        try:
           op = getValidChoose(len(mainRouter), "当前在'主'菜单,请输入您的操作:")
           if mainRouter[op]():
               subClearHistory(mainOptions)
        except KeyboardInterrupt:
            print("您终止了操作")
            subClearHistory(mainOptions)

if __name__ == "__main__":
    cliMainLoop()
