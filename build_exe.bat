
@echo on
REM Build Windows EXE
pip install pyinstaller
pyinstaller --onefile --windowed --icon assets/icon.ico recipe_app.py
 

