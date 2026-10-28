@echo off
echo ========================================================
echo   Starting CSIT 349 Portfolio & Autobiography App
echo ========================================================
echo.

where streamlit >nul 2>nul
if %errorlevel% == 0 (
    streamlit run app.py
) else (
    "%LOCALAPPDATA%\Python\bin\python.exe" -m streamlit run app.py
)
pause
