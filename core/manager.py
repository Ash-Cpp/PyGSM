"""
manager.py: 数据管理器
"""
import json
from core.models import Student

class GradeManager:
    """学生管理器
    """
    FLUSH_CNT = 3 # 更新频率标准,达到标准才有资格更新

    def __init__(self):
        self.__studentsBySid: dict[str, Student] = { }
        self.__studentsByName: dict[str, dict[str, Student]] = { }
        self.__sortFlag = True
        self.__sortedList = []
        self.__cnt = 0 # 更新计数
    
    @property
    def cnt(self) -> int:
        return self.__cnt
    
    @cnt.setter
    def cnt(self, value: int) -> None:
        self.__cnt = value
    
    def forceFlush(self) -> None:
        """强制触发下一次写入
        """
        self.__cnt = self.FLUSH_CNT
    
    def add(self, student: Student) -> None:
        """添加一个学生对象

        Args:
            student (Student): 待添加的学生 

        Raises:
            ValueError: 已经存在该学号的学生
        """
        if student.sid in self.__studentsBySid:
            raise ValueError(f"学号为{student.sid}的学生已经存在")
        self.__studentsBySid[student.sid] = student
        if student.name not in self.__studentsByName:
            self.__studentsByName[student.name] = { }
        self.__studentsByName[student.name][student.sid] = student
        self.__sortFlag = True
        self.__cnt += 1

    def removeBySid(self, sid: str) -> None:
        """移除指定学号的学生

        Args:
            sid (str): 学号 

        Raises:
            KeyError: 不存在这样的学生
        """
        if sid in self.__studentsBySid:
            name = self.__studentsBySid[sid].name
            del self.__studentsByName[name][sid]
            if not self.__studentsByName[name]:
                del self.__studentsByName[name]
            del self.__studentsBySid[sid]
            self.__sortFlag = True
            self.__cnt += 1
        else:
            raise KeyError(f"不存在学号为{sid}的学生")

    def removeByName(self, name: str) -> None:
        """移除指定姓名的学生

        Args:
            name (str): 姓名 

        Raises:
            KeyError: 不存在这样的学生 
        """
        if name in self.__studentsByName:
            for inner in list(self.__studentsByName[name].keys()):
                self.removeBySid(inner)
            self.__sortFlag = True
            self.__cnt += 1
        else:
            raise KeyError(f"不存在姓名为{name}的学生")
        
    def selectBySid(self, sid: str) -> Student:
        """查找指定学号的学生

        Args:
            sid (str): 学号 

        Raises:
            KeyError: 不存在这样的学生 

        Returns:
            Student: 符合要求的学生
        """
        if sid in self.__studentsBySid:
            return self.__studentsBySid[sid]
        else:
            raise KeyError(f"未查找到学号为{sid}的学生")
        
    def selectByName(self, name: str) -> dict:
        """查找指定姓名的学生

        Args:
            name (str): 姓名

        Raises:
            KeyError: 不存在这样的学生

        Returns:
            dict: 返回这样的学生字典(因为姓名可以重复),[sid,Student]
        """
        if name in self.__studentsByName:
            return self.__studentsByName[name]
        else:
            raise KeyError(f"未查找到姓名为{name}的学生")
    
    def updateGrades(self, sid: str, newGrades: dict[str, float]) -> None:
        """更新/覆盖原来的成绩表

        Args:
            sid (str): 需要覆盖成绩的学生 
            newGrades (dict[str, float]): 更新后的成绩 
        """
        target = self.selectBySid(sid)
        for subject, newVal in newGrades.items():
            target.update(subject, newVal)
        self.__sortFlag = True
        self.__cnt += self.FLUSH_CNT
    
    def __sortList(self) -> None:
        """排序学生列表,懒更新
        """
        if self.__sortFlag:
            # 按照总分从大到小排序,总分一样就按照学号排序
            students = self.__studentsBySid.values()
            self.__sortedList = sorted(students, key=lambda stu: (-stu.sum,stu.sid))
            self.__sortFlag = False
            self.__cnt += self.FLUSH_CNT

    def getSortedList(self) -> list[Student]:
        """获取排序后的学生列表
        Returns:
            list[Student]: 排序后的学生列表
        """
        self.__sortList()
        return self.__sortedList
        
    def updateGrade(self, sid: str, subject: str, newVal: float) -> None:
        """更新指定学生的指定科目成绩

        Args:
            sid (str): 学生学号
            subject (str): 科目名称
            newVal (float): 新的成绩
        """
        target = self.selectBySid(sid)
        target.update(subject, newVal)
        self.__cnt += self.FLUSH_CNT
        self.__sortFlag = True

    def toJson(self) -> str:
        """将学生数据序列化为JSON字符串

        Returns:
            str: JSON格式的字符串
        """
        self.__sortList()
        studentsDict = {}
        for student in self.__studentsBySid.values():
            studentsDict |= student.toDict()
        return json.dumps(studentsDict, ensure_ascii=False, indent=4)