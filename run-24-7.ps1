$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$logDir = Join-Path $PSScriptRoot "logs"
$supervisorPidFile = Join-Path $PSScriptRoot "supervisor.pid"
$botPidFile = Join-Path $PSScriptRoot "bot.pid"

if (!(Test-Path -LiteralPath $python)) {
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    Add-Content -Path (Join-Path $logDir "bot-supervisor.log") -Value "$(Get-Date -Format s) Python environment is missing."
    throw "Python environment is missing. Run setup again."
}

New-Item -ItemType Directory -Force -Path $logDir | Out-Null
Set-Content -Path $supervisorPidFile -Value $PID

while ($true) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path (Join-Path $logDir "bot-supervisor.log") -Value "$stamp Starting CHESS LOUNGE bot..."

    $outLog = Join-Path $logDir "bot-output.log"
    $errLog = Join-Path $logDir "bot-error.log"
    $process = Start-Process -FilePath $python -ArgumentList "bot.py" -WorkingDirectory $PSScriptRoot -PassThru -NoNewWindow -RedirectStandardOutput $outLog -RedirectStandardError $errLog
    Set-Content -Path $botPidFile -Value $process.Id
    $process.WaitForExit()

    $exitCode = $process.ExitCode
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path (Join-Path $logDir "bot-supervisor.log") -Value "$stamp Bot stopped with exit code $exitCode. Restarting in 10 seconds..."

    Start-Sleep -Seconds 10
}
