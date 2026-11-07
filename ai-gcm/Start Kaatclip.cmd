@echo off
rem Starts Kaatclip (API, web app and worker) on this laptop.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup\start.ps1"
pause
