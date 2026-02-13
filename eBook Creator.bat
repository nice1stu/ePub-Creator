@echo off
title eBook Creator Launcher
echo Launching Universal eBook Creator...
:: 'pythonw' launches without a console window. 
:: If it doesn't work, change 'pythonw' to 'python'
start "" pythonw main_gui.py
exit