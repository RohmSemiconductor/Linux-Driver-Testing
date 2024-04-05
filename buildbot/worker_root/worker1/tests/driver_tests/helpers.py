import operator

def checkStdOut(stdout,checkString):
#    for x in stdout:
#        result = stdout.find(checkString)
#        if (result != -1):
#            return 0
#    if (result == -1):
#        return 1

    if any(checkString in s for s in stdout):
        return 0
        
