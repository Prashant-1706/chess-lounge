@echo off
echo Removing CHESS LOUNGE bot auto-start...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$shortcutPath = Join-Path ([Environment]::GetFolderPath('Startup')) 'CHESS LOUNGE Discord Bot.lnk'; if (Test-Path $shortcutPath) { Remove-Item $shortcutPath -Force; Write-Host 'Removed:' $shortcutPath } else { Write-Host 'No Startup shortcut found.' }"
echo Done.
pause
