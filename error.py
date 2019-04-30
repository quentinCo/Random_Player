import sys

def error_handler():
    info = sys.exc_info()
    return "{}. {}, line {}".format(info[0], info[1], info[2].tb_lineno)
