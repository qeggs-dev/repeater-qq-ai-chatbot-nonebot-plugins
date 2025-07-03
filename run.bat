@echo off
title Repeater
set PROJECT_DIR=Repeater
if "%~1"=="-d" set PROJECT_DIR=%~2 & shift & shift
cd %~dp0\%PROJECT_DIR%
%~dp0\venv\Scripts\nb.exe run
echo Press any key to exit...
pause > nul