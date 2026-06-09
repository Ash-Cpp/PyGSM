"""
main.py
function: 实现界面选择与主循环逻辑
"""
from pathlib import Path
from core.models import loadJson
import core.util as util

PROJECT_ROOT = Path(__file__).resolve().parent

def main() -> None:
    try:
        config = loadJson(str(PROJECT_ROOT / "config.json"))
        startMode = config["defaultMode"]
        if startMode == "auto":
            startMode = config["lastMode"]
    except:
        print("配置文件异常")
        return
    if startMode == "cli":
        util.launchIndependent(str(PROJECT_ROOT / "cli" / "csys.py"), True)
    elif startMode == "gui":
        util.launchIndependent(str(PROJECT_ROOT / "gui" / "gsys.pyw"), False)
    else:
        print("配置文件异常")
    
if __name__ == "__main__":
    main()
