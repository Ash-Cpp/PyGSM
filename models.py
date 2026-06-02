"""
models.py
function: 提供对数据操作的接口
"""
import json
def loadJson(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        res = json.load(f)
    return res
"""
学生类, 支持多列数据支持, 但对不支持的关键字会抛出异常
"""
class Student:
    def __init__(self, name: str, sid: str, grades: dict):
        self.name = name
        self.sid = sid
        self.__grades = grades.copy()
        self.__sum = sum(grades.values())
        self.__subCnt = len(grades)
        self.__average = self.__sum / self.__subCnt

    @property
    def sum(self) -> float:
        return float(self.__sum)
    
    @property
    def average(self) -> float:
        return float(self.__average)
    
    def __getitem__(self, key) -> float:
        return float(self.__grades[key])
    
    def __setitem__(self, key, value) -> None:
        if key not in self.__grades:
            raise KeyError("未出现该科目")
        self.update(key, value)

    def update(self, subject: str, newVal: any):
        oldVal = self.__grades[subject]
        delta = newVal - oldVal
        self.__grades[subject] = newVal
        self.__sum += delta
        self.__average += delta / self.__subCnt
    def toDict(self) -> dict:
        return {
            self.sid: {
                "name" : self.name,
                "grades" : self.__grades,
            }
        }
    def toJson(self) -> str:
        return json.dumps(self.toDict(), ensure_ascii=False, indent=4)
    def values(self):
        return self.__grades.values()

def models_test():
    pass
    s1 = Student("韩某", "252912345678", {"语文": 90, "数学": 130, "英语": 96})
    print("Test for models.py")
    print(f"Sum grade of s1 is { s1.sum:g}")
    print(f"Average grade of s1 is { s1.average:.2f}")
    s1.update("英语", 97)
    s1["语文"] = 91
    print(f"Updated...")
    print(f"Sum grade of s1 is { s1.sum:g}")
    print(f"Average grade of s1 is { s1.average:.2f}")
    print(s1["语文"], s1["数学"], s1["英语"])
    print(s1.toJson())


if __name__ == "__main__":
    models_test()