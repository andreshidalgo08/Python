import sys, os

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

restart()
