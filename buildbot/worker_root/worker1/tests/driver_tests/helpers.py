import operator

def checkStdOut(stdout,checkString):
    if any(checkString in s for s in stdout):
        return 0

def checkStr(stdout,checkString):
    if checkString in stdout:
        return 0
