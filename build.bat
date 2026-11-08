@echo off
REM Builds a single-file Windows executable using PyInstaller.
REM Make sure you have Python installed and available as `py` or `python`.

py -3 -m pip install -r requirements.txt

REM Ensure Mangment 2.html is located next to app.py for bundling.
REM The --add-data syntax for Windows is: "source;dest"
py -3 -m PyInstaller --onefile --windowed --add-data "Mangment 2.html;." --name "CloudBase_ERP" app.py

necho Build finished. The single exe will be at dist\CloudBase_ERP.exe
pause
