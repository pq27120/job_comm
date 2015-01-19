__author__ = 'pq'
#!encoding:utf-8
import sys
from cx_Freeze import setup, Executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup(
        name = "工具合集",
        version = "1",
        description = "工具合集",
        executables =[Executable ("frame.py", base = base,icon="images.ico")])