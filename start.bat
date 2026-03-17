```batch
@echo off
title Ollama Chat Client
cd /d "%~dp0"

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno
call venv\Scripts\activate

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Ejecutar aplicacion
echo.
echo ===================================
echo ^!^! Ollama Chat Client iniciado ^^!^^!
echo ===================================
echo.
echo IMPORTANTE: Asegúrate de que Ollama esté ejecutándose
echo Ejecuta en otra ventana cmd: ollama serve
echo.
python main.py

pause
```