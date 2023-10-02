param([string]$VEnvName='venv', [switch]$Run)

[int]$ERROR_FAILED_TO_CREATE_VENV = 1
[int]$ERROR_FAILED_TO_ACTIVATE_VENV = 2
[int]$ERROR_FAILED_TO_INSTALL_PACKAGES = 3

if($Run -eq $false)
{
    Write-Output '===> Settings up venv...'
    python.exe -m venv $VEnvName
    
    if(-not $?) { Write-Error "Failed to setup venv..."; exit $ERROR_FAILED_TO_CREATE_VENV }
    
    
    $loc = Get-Location
    
    Set-Location ".\$VEnvName\Scripts"
    ./Activate.ps1
    
    if(-not $?) { Write-Error "Failed to activate venv: $VEnvName ..."; exit $ERROR_FAILED_TO_ACTIVATE_VENV }
    
    Set-Location $loc
    
    
    Write-Output '===> Installing packages....'
    python.exe -m pip install -r .\requirements.txt
    
    if(-not $?) { Write-Error "Failed to install packages..."; exit $ERROR_FAILED_TO_INSTALL_PACKAGES }
}
else 
{
    $loc = Get-Location
    
    Set-Location ".\$VEnvName\Scripts"
    ./Activate.ps1
    
    if(-not $?) { Write-Error "Failed to activate venv: $VEnvName ..."; exit $ERROR_FAILED_TO_ACTIVATE_VENV }
    
    Set-Location $loc
    
    Write-Output '===> Starting webapi srv'
    uvicorn main:app
}