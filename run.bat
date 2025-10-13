@echo off
set PROJECT=Repeater
title %PROJECT%
if "%~1"=="-d" set PROJECT_DIR=%~2 & shift & shift
cd %~dp0\%PROJECT%
%~dp0\.venv\Scripts\nb.exe run
echo Press any key to exit...
pause > nul