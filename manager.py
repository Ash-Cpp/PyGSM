"""
manager.py
function: 数据管理器
"""
import json
from models import Student
class GradeManager:
    def __init__(self):
        self.__studentsBySid: dict[str, Student] = { }
        self.__studentsByName: dict[str, dict[str, Student]] = { }
    
    def add(self, student: Student) -> None:

        if student.sid in self.__studentsBySid:
            raise ValueError(f"学号为{student.sid}的学生已经存在") 
        self.__studentsBySid[student.sid] = student
        if student.name not in self.__studentsByName:
            self.__studentsByName[student.name] = { }
        self.__studentsByName[student.name][student.sid] = student
    
    def removeBySid(self, sid: str) -> None:
        if sid in self.__studentsBySid:

            name = self.__studentsBySid[sid].name
            del self.__studentsByName[name][sid]
            # 如果删除了最后一个,把key=name全删掉
            if not self.__studentsByName[name]:
                del self.__studentsByName[name]
            del self.__studentsBySid[sid]

        else:
            raise KeyError(f"不存在学号为{sid}的学生")
    
    def removeByName(self, name: str) -> None:
        if name in self.__studentsByName:
            for inner in list(self.__studentsByName[name].keys()):
                self.removeBySid(inner)
        else:
            raise KeyError(f"不存在姓名为{name}的学生")
    
    def selectBySid(self, sid: str) -> Student:
        if sid in self.__studentsBySid:
            return self.__studentsBySid[sid]
        else:
            raise KeyError(f"未查找到学号为{sid}的学生")
        
    def selectByName(self, name: str) -> dict:
        if name in self.__studentsByName:
            return self.__studentsByName[name]
        else:
            raise KeyError(f"未查找到姓名为{name}的学生")
    
    def updateGrades(self, sid: str, newGrades: dict[str, float]) -> None:
        target = self.selectBySid(sid)
        for subject, newVal in newGrades.items():
            target.update(subject, newVal)
    
    def getSortedList(self) -> list[Student]:
        # 按照总分从大到小排序,总分一样就按照学号排序
        students = self.__studentsBySid.values()
        return sorted(students, key=lambda stu: (-stu.sum,stu.sid))
    
    def updateGrade(self, sid: str, subject: str, newVal: float) -> None:
        target = self.selectBySid(sid)
        target.update(subject, newVal) 
    def toJson(self) -> str:
        studentsDict = {}
        for student in self.__studentsBySid.values():
            studentsDict |= student.toDict()
        return json.dumps(studentsDict, ensure_ascii=False, indent=4)