"""
storage.py
function: 负责数据的读写与持久化
"""
from manager import *
from models import *
class FileHandler:
    def __init__(self, filename: str = "./data/studentsInfo.json"):
        self.filename = filename
    
    def loadFromFile(self) -> GradeManager:
        data = loadJson(self.filename)
        manager = GradeManager()
        for sid, info in data.items():
            name = info["name"]
            grades = info["grades"]
            manager.add(Student(name, sid, grades))
        return manager
    def saveToFile(self, manager: GradeManager) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(manager.toJson())

def testStorage():
    fh = FileHandler()
    manager = fh.loadFromFile()
    s = Student("李四", "252906040143", {
        "语文" : 20,
        "数学" : 30,
        "英语" : 33})
    manager.add(s)
    print(manager.toJson())
    fh.saveToFile(manager)

if __name__ == "__main__":
    testStorage()