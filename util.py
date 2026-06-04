import sys
import subprocess
def launchIndependent(scriptName, hasConsole = True):
    cmd = [sys.executable, scriptName]
    if hasConsole:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)