"""
main.py
function: 实现界面选择与主循环逻辑
"""
from models import loadJson
import sys

def cliMainLoop() -> None:
    print("cliMainLoop")

def guiMainLoop() -> None:
    pass
    print("guiMainLoop")

def main() -> None:
    try:
        config = loadJson("./config.json")
        startMode = config["defaultMode"]
        if startMode == "auto":
            startMode = config["lastMode"]
        if startMode == "cli":
            cliMainLoop()
        elif startMode == "gui":
                guiMainLoop()
        else:
            raise
    except:
        print("config.json不存在或已被非法修改")
    
if __name__ == "__main__":
    main()