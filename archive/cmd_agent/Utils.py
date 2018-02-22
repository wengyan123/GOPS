from time import strftime, localtime


def getLocaltime():
    return strftime("%a, %d %b %Y %H:%M:%S", localtime())

