# -*- coding: utf-8 -*-

"""
pip install pyinstaller
pyinstaller -F -w WinPollManager.py
"""
from PyInstaller.__main__ import run

if __name__ == '__main__':
    print("start build updater ...")
    params = ['updater.py', '-F', '-c', '--icon=updater.ico']
    run(params)
    print("start build monitor ...")
    params = ["monitor.py", "-F", "-c", "--icon=monitor.ico"]
    run(params)

