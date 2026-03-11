@echo off
:: Move to the project root directory (one level up from /scripts)
cd /d "%~dp0.."

set ENV_NAME=week1_env

echo [STEP 1/3] Checking Conda...
call conda --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Conda is not found. Use 'Anaconda Prompt'!
    pause
    exit /b 1
)

echo [STEP 2/3] Preparing environment: %ENV_NAME%...
:: Check if the environment already exists
call conda info --envs | findstr /c:"%ENV_NAME%" >nul
if errorlevel 1 (
    echo Creating new environment...
    call conda create -n %ENV_NAME% python=3.10 -y
) else (
    echo Environment already exists. Skipping creation.
)

echo [STEP 3/3] Installing requirements and testing...
:: Run commands inside the environment
call conda run -n %ENV_NAME% python -m pip install -r requirements.txt
call conda run -n %ENV_NAME% python broken_env.py

if errorlevel 1 (
    echo ========================================
    echo [ERROR] SMOKE TEST FAILED!
    echo ========================================
) else (
    echo ========================================
    echo [OK] EVERYTHING IS READY!
    echo ========================================
)

pause
