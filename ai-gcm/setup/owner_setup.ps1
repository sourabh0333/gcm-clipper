# Kaatclip one-time setup for the owner. Double-click "Setup Kaatclip.cmd" in ai-gcm.
# Every step is free. Each one can be skipped and the script run again later; values already set are kept.
# Keys are typed here, on the laptop, and saved only in ai-gcm\.env (never committed, never sent anywhere).

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot          # ai-gcm
$EnvFile = Join-Path $Root ".env"
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Port = 8770

function Read-EnvFile {
    $values = [ordered]@{}
    if (Test-Path $EnvFile) {
        foreach ($line in [IO.File]::ReadAllLines($EnvFile)) {
            if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$') { $values[$Matches[1]] = $Matches[2].Trim() }
        }
    }
    return $values
}

function Set-EnvValue([string]$Key, [string]$Value) {
    # Replaces the key's line or adds it; other lines (and comments) stay as they are. UTF-8 without BOM,
    # because a BOM would hide the first key from the app.
    $lines = New-Object System.Collections.Generic.List[string]
    if (Test-Path $EnvFile) { $lines.AddRange([IO.File]::ReadAllLines($EnvFile)) }
    $found = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "^\s*$Key\s*=") { $lines[$i] = "$Key=$Value"; $found = $true }
    }
    if (-not $found) { $lines.Add("$Key=$Value") }
    [IO.File]::WriteAllLines($EnvFile, $lines, (New-Object System.Text.UTF8Encoding($false)))
}

function Ask([string]$Question, [string]$Current) {
    $hint = if ($Current) { " (Enter keeps the current one)" } else { " (Enter skips)" }
    $answer = Read-Host "$Question$hint"
    if ([string]::IsNullOrWhiteSpace($answer)) { return $Current }
    return $answer.Trim()
}

function Ask-Secret([string]$Question, [bool]$HasOne) {
    $hint = if ($HasOne) { " (Enter keeps the current one)" } else { " (Enter skips)" }
    $secure = Read-Host "$Question$hint" -AsSecureString
    $plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
    return $plain.Trim()
}

function Find-Tailscale {
    $cmd = Get-Command tailscale -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $exe = "C:\Program Files\Tailscale\tailscale.exe"
    if (Test-Path $exe) { return $exe }
    return $null
}

Write-Host ""
Write-Host "=== Kaatclip setup ===" -ForegroundColor Yellow
Write-Host "Three free steps: Telegram, the phone address (Tailscale), Google sign-in. Skip any with Enter."
$envNow = Read-EnvFile

# --- 1. Telegram ---------------------------------------------------------------------------------------
Write-Host ""
Write-Host "1/3  Telegram messages" -ForegroundColor Cyan
Write-Host "     In Telegram, open @BotFather, send /newbot, name it Kaatclip, pick a username ending in 'bot'."
Write-Host "     BotFather replies with a token like 123456789:AA...  Paste it here (it stays hidden)."
$token = Ask-Secret "     Bot token" ([bool]$envNow["TELEGRAM_BOT_TOKEN"])
if ($token) {
    if ($token -notmatch '^\d+:[A-Za-z0-9_-]{30,}$') { Write-Host "     That doesn't look like a bot token; skipped." -ForegroundColor Red }
    else { Set-EnvValue "TELEGRAM_BOT_TOKEN" $token; Write-Host "     Saved." -ForegroundColor Green }
}

# --- 2. Phone address with Tailscale Funnel ------------------------------------------------------------
Write-Host ""
Write-Host "2/3  A fixed https:// address for your phone (Tailscale Funnel, free)" -ForegroundColor Cyan
$go = Read-Host "     Set it up now? (y/n)"
if ($go -match '^[yY]') {
    $ts = Find-Tailscale
    if (-not $ts) {
        Write-Host "     Installing Tailscale from Microsoft's winget (Windows asks for permission)..."
        winget install --id Tailscale.Tailscale --exact --source winget
        $ts = Find-Tailscale
        if (-not $ts) { Write-Host "     Tailscale didn't install. Run this setup again after installing it from tailscale.com." -ForegroundColor Red }
    }
    if ($ts) {
        Write-Host "     Sign in to Tailscale in the browser window that opens (your Google account is fine)."
        & $ts up
        Write-Host "     Turning on Funnel for port $Port. If Tailscale prints a link to enable Funnel, open it, click Enable, then come back."
        & $ts funnel --bg $Port
        $status = & $ts status --json | ConvertFrom-Json
        $name = $status.Self.DNSName.TrimEnd(".")
        if ($name) {
            $url = "https://$name"
            Set-EnvValue "AIGCM_PUBLIC_URL" $url
            Write-Host "     Your phone address: $url" -ForegroundColor Green
        }
    }
}

# --- 3. Google sign-in ---------------------------------------------------------------------------------
Write-Host ""
Write-Host "3/3  Google sign-in" -ForegroundColor Cyan
$envNow = Read-EnvFile
$public = $envNow["AIGCM_PUBLIC_URL"]
Write-Host "     Follow docs\Google sign-in setup.md (10 minutes). Use these redirect URIs:"
Write-Host "        http://localhost:$Port/auth/google/callback"
if ($public) { Write-Host "        $public/auth/google/callback" }
$open = Read-Host "     Open the Google Cloud console now? (y/n)"
if ($open -match '^[yY]') { Start-Process "https://console.cloud.google.com/auth/clients" }
$clientId = Ask "     Client ID" $envNow["GOOGLE_CLIENT_ID"]
if ($clientId -and $clientId -ne $envNow["GOOGLE_CLIENT_ID"]) {
    if ($clientId -notmatch '\.apps\.googleusercontent\.com$') { Write-Host "     That doesn't look like a Google client ID; skipped." -ForegroundColor Red }
    else { Set-EnvValue "GOOGLE_CLIENT_ID" $clientId; Write-Host "     Saved." -ForegroundColor Green }
}
$secret = Ask-Secret "     Client secret" ([bool]$envNow["GOOGLE_CLIENT_SECRET"])
if ($secret) { Set-EnvValue "GOOGLE_CLIENT_SECRET" $secret; Write-Host "     Saved." -ForegroundColor Green }
$owner = Ask "     Your Google email (you become the owner)" $envNow["AIGCM_ADMINS"]
if ($owner -and $owner -ne $envNow["AIGCM_ADMINS"]) {
    if ($owner -notmatch '^[^@\s]+@[^@\s]+\.[^@\s]+$') { Write-Host "     That doesn't look like an email; skipped." -ForegroundColor Red }
    else {
        Set-EnvValue "AIGCM_ADMINS" $owner.ToLower()
        Write-Host "     Saved. Bringing your earlier streams and swipes into your account..."
        & $Python -m aigcm.manage import-jobs --owner $owner
    }
}
if (-not (Read-EnvFile)["AIGCM_PUBLIC_URL"]) { Set-EnvValue "AIGCM_PUBLIC_URL" "http://localhost:$Port" }

# --- Build the web app if needed, then start ----------------------------------------------------------
if (-not (Test-Path (Join-Path $Root "web\dist\index.html"))) {
    Write-Host ""
    Write-Host "Building the web app (first time only)..."
    Push-Location (Join-Path $Root "web")
    npm install --no-audit --no-fund
    npm run build
    Pop-Location
}

Write-Host ""
Write-Host "Setup done. Starting Kaatclip..." -ForegroundColor Yellow
& (Join-Path $PSScriptRoot "start.ps1")
Write-Host ""
Read-Host "Press Enter to close this window"
