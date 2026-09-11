@echo off
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
echo.
echo Cai dat xong. Chay run_windows.bat hoac: .venv\Scripts\python.exe app.py
pause
