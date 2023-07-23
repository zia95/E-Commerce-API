param([string]$VEnvName='venv')

Set-Alias pyint -Value $PyInterpreter

Write-Output '===> Settings up venv...'
python.exe -m venv $VEnvName

if(-not $?) { Write-Error "Failed to setup venv..."; exit 1 }

$loc = Get-Location

Set-Location ".\$VEnvName\Scripts"
./Activate.ps1

if(-not $?) { Write-Error "Failed to activate venv: $VEnvName ..."; exit 2 }

Set-Location $loc
Write-Output '===> Installing packages....'
python.exe -m pip install -r .\requirements.txt

if(-not $?) { Write-Error "Failed to install packages..."; exit 3 }

Write-Output '===> Starting webapi srv'
uvicorn main:app