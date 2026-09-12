@echo off
cd /d "%~dp0"
echo Installing CHESS LOUNGE bot auto-start...
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$startup = [Environment]::GetFolderPath('Startup'); $target = Join-Path (Get-Location) 'start-24-7-hidden.vbs'; $shortcutPath = Join-Path $startup 'CHESS LOUNGE Discord Bot.lnk'; $shell = New-Object -ComObject WScript.Shell; $shortcut = $shell.CreateShortcut($shortcutPath); $shortcut.TargetPath = Join-Path $env:SystemRoot 'System32\wscript.exe'; $shortcut.Arguments = '\"' + $target + '\"'; $shortcut.WorkingDirectory = Get-Location; $shortcut.Description = 'Start CHESS LOUNGE Discord Bot keep-alive runner'; $shortcut.Save(); Write-Host 'Startup shortcut created:' $shortcutPath"
echo.
echo Starting the bot now...
start "" wscript.exe "%~dp0start-24-7-hidden.vbs"
echo.
echo Done. The bot will auto-start when you log in to Windows.
echo Your PC must stay on and connected to internet for the bot to stay online.
pause
