@echo off
cd /d "%~dp0"
echo Stopping CHESS LOUNGE bot auto-run processes...
if exist bot.pid (
  for /f %%p in (bot.pid) do taskkill /PID %%p /F >nul 2>nul
)
if exist supervisor.pid (
  for /f %%p in (supervisor.pid) do taskkill /PID %%p /F >nul 2>nul
)
echo.
echo If the bot is still online, restart your PC or close any remaining bot terminal.
pause
