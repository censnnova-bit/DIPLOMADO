@echo off
echo ====================================
echo   Iniciando Proyecto Vue + Tailwind
echo ====================================
echo.
cd /d "%~dp0"
echo Directorio: %CD%
echo.
echo Instalando dependencias...
call npm install
echo.
echo Iniciando servidor de desarrollo...
echo.
call npm run dev
