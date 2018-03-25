import sys, os

python = sys.executable
os.execl(python, python, * sys.argv)
