"""
main.py
function: 实现界面选择与主循环逻辑
"""
from core.models import loadJson
import core.util as util
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
        util.launchIndependent("./cli/csys.py", True)
    elif startMode == "gui":
        util.launchIndependent("./gui/gsys.pyw", False)
    else:
        print("配置文件异常")
    
if __name__ == "__main__":
    main()