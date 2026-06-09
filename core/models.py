"""
models.py: 处理数据逻辑
"""
import json

def loadJson(filename: str) -> dict:
    """读取json文件,并且把内容转成字典

    Args:
        filename (str): 文件名称 

    Returns:
        dict: JSON对象对应的字典
    """
    with open(filename, 'r', encoding='utf-8') as f:
        res = json.load(f)
    return res

class Student:
    """学生类
    """
    def __init__(self, name: str, sid: str, grades: dict):
        """构造函数

        Args:
            name (str): 学生姓名 
            sid (str): 学生学号 
            grades (dict): 学生成绩表
        """
        self.name = name
        self.sid = sid
        self.__grades = grades.copy()
        self.__sum = sum(grades.values())
        self.__subCnt = len(grades)
        self.__average = self.__sum / self.__subCnt

    @property
    def sum(self) -> float:
        """学生总成绩

        Returns:
            float: 学生总成绩 
        """
        return float(self.__sum)
    
    @property
    def average(self) -> float:
        """学生平均成绩

        Returns:
            float: 学生平均成绩
        """
        return float(self.__average)
    
    def __getitem__(self, key: str) -> float:
        return float(self.__grades[key])
    
    def __setitem__(self, key, value) -> None:
        if key not in self.__grades:
            raise KeyError("未出现该科目")
        self.update(key, value)

    def update(self, subject: str, newVal: any) -> None:
        """修改指定科目的成绩

        Args:
            subject (str): 科目名称 
            newVal (any): 修改后的值
        """
        if subject not in self.__grades:
            raise KeyError(f"不存在'{subject}'科目")
        oldVal = self.__grades[subject]
        delta = newVal - oldVal
        self.__grades[subject] = newVal
        self.__sum += delta
        self.__average += delta / self.__subCnt
    
    def toDict(self) -> dict:
        """学生信息转成字典

        Returns:
            dict: 对应的字典结果 
        """
        return {
            self.sid: {
                "name" : self.name,
                "grades" : self.__grades,
            }
        }
    
    def toJson(self) -> str:
        """学生信息转成JSON格式

        Returns:
            str: 对应的JSON对象字符串
        """
        return json.dumps(self.toDict(), ensure_ascii=False, indent=4)
    
    def values(self):
        """对外暴露的成绩表接口

        Returns:
            dict_values: 学生成绩值列
        """
        return self.__grades.values()