"""
util.py: 工具模块
"""
import sys
import subprocess
from pathlib import Path

def launchIndependent(scriptName: str, hasConsole: bool = True) -> None:
    """启动独立子进程

    Args:
        scriptName (str): 需要执行的程序名称
        hasConsole (bool, optional): 是否需要控制台. Defaults to True.
    """
    current_executable = Path(sys.executable)
    if hasConsole:
        if current_executable.name.lower() == "pythonw.exe":
            executable = current_executable.with_name("python.exe")
        else:
            executable = current_executable
        cmd = [str(executable), scriptName]
        if sys.platform == "win32":
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(cmd)
    else:
        if current_executable.name.lower() == "python.exe":
            executable = current_executable.with_name("pythonw.exe")
        else:
            executable = current_executable
        cmd = [str(executable), scriptName]
        subprocess.Popen(cmd)