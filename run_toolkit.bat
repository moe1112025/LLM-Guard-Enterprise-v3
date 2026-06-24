@echo off
title LLM-GUARD v3 Enterprise Launcher
cls

echo ========================================================
echo        LLM-GUARD v3.0: ENTERPRISE LAUNCHER ENGINE
echo ========================================================
echo.

where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Error: Ollama is NOT installed on this machine!
    echo [!] Opening official download page for you...
    start https://ollama.com/download/windows
    echo [!] Please install Ollama from the browser, then restart this script.
    pause
    exit
)

echo [*] Checking Ollama Daemon Status...
powershell -Command "$conn = New-Object System.Net.Sockets.TcpClient; $async = $conn.BeginConnect('127.0.0.1', 11434, $null, $null); Timer = [System.Diagnostics.Stopwatch]::StartNew(); while (!$async.IsCompleted -and $Timer.ElapsedMilliseconds -lt 1000) { Start-Sleep -m 100 }; if ($conn.Connected) { $conn.Close(); exit 0 } else { exit 1 }"

if %errorlevel% neq 0 (
    echo [*] Ollama Server is offline. Launching daemon instance actively...
    start /b ollama serve >nul 2>&1
    
    echo [*] Waiting for Ollama node to initialize and bind port 11434...
    :wait_loop
    timeout /t 2 /nobreak >nul
    powershell -Command "$conn = New-Object System.Net.Sockets.TcpClient; $async = $conn.BeginConnect('127.0.0.1', 11434, $null, $null); Start-Sleep -m 500; if ($conn.Connected) { $conn.Close(); exit 0 } else { exit 1 }"
    if %errorlevel% neq 0 goto wait_loop
)

echo [✓] Ollama Core Infrastructure is ONLINE!
echo.

echo [*] Verifying Local Judge Engine Capacity (llama3)...
echo [!] Note: If this is the first run, it will download the model weights automatically.
ollama pull llama3

echo.
echo ========================================================
echo        STARTING ENTERPRISE CORE METRICS PIPELINE
echo ========================================================
echo.

python main.py

echo.
echo [✓] Execution Completed Successfully.
pause