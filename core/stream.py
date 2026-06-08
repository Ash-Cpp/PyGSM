"""
stream.py: IO流处理
"""
from core.models import Student
from tabulate import tabulate
import os
def clearConsole():
    os.system("cls") # Python3.5后弃用

def printOptions(options: list[str]) -> None:
    """打印选项

    Args:
        options (list[str]): 选项列
    """
    i = 1
    rows = []
    header = ["操作序号", "操作说明"]
    for op in options:
        row = [ str(i), op ]
        i += 1
        rows.append(row)
    print(tabulate(rows, headers=header, tablefmt="rounded_grid", stralign="center",numalign="center"))

def printStudent(student: Student) -> None:
    """打印单个学生的信息

    Args:
        student (Student): 需要打印的学生信息
    """
    header =  ["学号", "姓名", "语文", "数学", "英语", "平均分", "总分"]
    tabelData = [[
        student.sid,
        student.name,
        f"{student['语文']:g}",
        f"{student['数学']:g}",
        f"{student['英语']:g}",
        f"{student.average:.2f}",
        f"{student.sum:g}", 
    ]]
    i = 1
    print(tabulate(tabelData, headers=header, tablefmt="rounded_grid", stralign="center", numalign="center"))

def printStudentsTable(students: list[Student]) -> None:
    """打印学生信息表

    Args:
        students (list[Student]): 需要打印的学生(顺序)表
    """
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
            f"{s.average:.2f}",
            f"{s.sum:g}",
        ]
        i += 1
        tabelData.append(row)
    print(tabulate(tabelData, headers=header, tablefmt="rounded_grid", stralign="center", numalign="center"))