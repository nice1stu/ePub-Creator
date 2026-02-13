@echo off
title eBook Creator Launcher
echo Launching Universal eBook Creator...
:: We use 'python' instead of 'pythonw' to see errors
:: We removed 'start' and 'exit' so the window stays open
py main_gui.py
pause