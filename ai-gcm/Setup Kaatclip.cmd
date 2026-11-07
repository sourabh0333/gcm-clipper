@echo off
rem One-time Kaatclip setup: Telegram, phone address, Google sign-in. Safe to run again.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup\owner_setup.ps1"
