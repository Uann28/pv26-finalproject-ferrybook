@echo off
echo ============================================
echo   FerryBook - Installer
echo ============================================
echo.
echo Menginstal dependensi Python...
pip install PySide6 reportlab
echo.
echo Instalasi selesai! Menjalankan FerryBook...
echo.
python main.py
pause
