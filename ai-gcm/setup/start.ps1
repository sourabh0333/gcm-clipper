# Starts Kaatclip on the laptop: the API with the web app, and the worker that processes streams.
# Each runs in its own minimised window (close a window to stop that part). Running this again while they
# run does nothing harmful: a second API can't take the port, and a second worker waits for the first.

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Port = 8770

function Running([string]$Pattern) {
    @(Get-CimInstance Win32_Process -Filter "name='python.exe'" | Where-Object { $_.CommandLine -match $Pattern }).Count -gt 0
}

# The key that encrypts creators' YouTube tokens: made once, kept in .env, never shown.
Push-Location $Root
try { & $Python -m aigcm.manage token-key | Out-Null } finally { Pop-Location }

if (Running "aigcm\.api") { Write-Host "The API is already running." }
else {
    Start-Process -FilePath $Python -ArgumentList "-m", "aigcm.api", "--port", "$Port" -WorkingDirectory $Root -WindowStyle Minimized
    Write-Host "Started the API and web app."
}
if (Running "aigcm\.worker") { Write-Host "The worker is already running." }
else {
    Start-Process -FilePath $Python -ArgumentList "-m", "aigcm.worker" -WorkingDirectory $Root -WindowStyle Minimized
    Write-Host "Started the worker."
}

$public = $null
$envFile = Join-Path $Root ".env"
if (Test-Path $envFile) {
    foreach ($line in [IO.File]::ReadAllLines($envFile)) { if ($line -match '^\s*AIGCM_PUBLIC_URL\s*=(.*)$') { $public = $Matches[1].Trim() } }
}
Write-Host ""
Write-Host "On this laptop:  http://localhost:$Port" -ForegroundColor Green
if ($public -and $public -like "https://*") { Write-Host "On your phone:   $public" -ForegroundColor Green }
