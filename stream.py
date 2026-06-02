"""
stream.py
function: IO流处理
"""
from models import Student
from tabulate import tabulate
def printStudentsTable(students: list[Student]):
    header =  ["排名", "学号", "姓名", "语文", "数学", "英语", "平均分", "总分"]
    tabelData = []
    i = 1
    for s in students:
        row = [
            str(i),
            s.sid,
            s.name,
            f"{s["语文"]:g}",
            f"{s["数学"]:g}",
            f"{s["英语"]:g}",
            f"{s.average:.2f}"
            f"{s.sum:g}",
        ]
        i += 1
        tabelData.append(row)
    print(tabulate(tabelData, headers=header, tablefmt="grid", stralign="center", numalign="center"))

def testStream():
    import storage
    fh = storage.FileHandler()
    manager = fh.loadFromFile()
    printStudentsTable(manager.getSortedList())
    
    
if __name__ == "__main__":
    testStream()
