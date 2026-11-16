@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3 generar_trucos.py
if errorlevel 1 (
  echo.
  echo No se pudo ejecutar. Prueba: python generar_trucos.py
)
echo.
pause
