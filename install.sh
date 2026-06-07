#!/bin/bash
echo "============================================"
echo "  FerryBook - Installer"
echo "============================================"
echo ""
echo "Menginstal dependensi Python..."
pip3 install PySide6 reportlab
echo ""
echo "Instalasi selesai! Menjalankan FerryBook..."
echo ""
python3 main.py
