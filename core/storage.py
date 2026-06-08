"""
storage.py: 负责数据的读写与持久化
"""

from core.manager import *
from core.models import *
import atexit
class ConfigHanlde:
    def __init__(self, config: str = "../config.json"):
        data = loadJson(config)
        self.__defaultMode = data["defaultMode"]
        self.__lastMode = data["lastMode"]
        self.__config = config
    
    def saveToFile(self) -> None:
        with open(self.__config, "w", encoding="utf-8") as f:
            f.write(json.dumps({
                "defaultMode" : self.__defaultMode,
                "lastMode": self.__lastMode
            }))

    @property
    def defaultMode(self) -> str:
        return self.__defaultMode

    def setDefaultMode(self, mode: str = "auto") -> None:
        """启动模式设置

        Args:
            mode (str, optional): auto/gui/cli. Defaults to "auto".
        """
        self.__defaultMode = mode
        self.saveToFile()
    
    def setLastMode(self, mode: str = "cli") -> None:
        """上次打开的界面

        Args:
            mode (str, optional): cli/gui. Defaults to "cli".
        """
        self.__lastMode = mode
        self.saveToFile()

        
class FileHandler:
    def __init__(self, filename: str = "../data/studentsInfo.json"):
        self.filename = filename
        data = loadJson(self.filename)
        self.manager = GradeManager()
        for sid, info in data.items():
            name = info["name"]
            grades = info["grades"]
            self.manager.add(Student(name, sid, grades))
        atexit.register(self.safeExiting) # 安全操作

    def safeExiting(self) -> None:
        """伪析构
        """
        self.manager.cnt = self.manager.FLUSH_CNT
        self.saveToFile()

    def saveToFile(self) -> None:
        """保存到文件
        """
        if self.manager.cnt >= self.manager.FLUSH_CNT:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(self.manager.toJson())
            self.manager.cnt = 0