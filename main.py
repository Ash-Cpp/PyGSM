"""
main.py
function: 实现界面选择与主循环逻辑
"""
from models import loadJson
import util
import sys
import subprocess
import platform

def main() -> None:
    try:
        config = loadJson("./config.json")
        startMode = config["defaultMode"]
        if startMode == "auto":
            startMode = config["lastMode"]
    except:
        print("配置文件异常")
    if startMode == "cli":
        util.launchIndependent("./csys.py", True)
    elif startMode == "gui":
        util.launchIndependent("./gsys.py", False)
    else:
        print("配置文件异常")
    
if __name__ == "__main__":
    main()