@echo off
cd /d "%~dp0"
title CHESS LOUNGE BOT - IMAGE BOARD VERSION
echo Starting CHESS LOUNGE bot...
echo Board style: IMAGE BOARD VERSION
echo Keep this window open while you want the bot online.
echo.
if not exist .venv\Scripts\python.exe (
  echo The bot environment is missing. Please reinstall the project dependencies.
  pause
  exit /b 1
)
.venv\Scripts\python.exe bot.py
echo.
echo The bot stopped. Read the message above for details.
pause
