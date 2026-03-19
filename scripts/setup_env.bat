@echo off
cd /d "%~dp0"

set ENV_NAME=sem2_env

echo [1/3] Проверка Conda...
call conda --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Conda не найдена. Убедись, что Anaconda/Miniconda установлена и добавлена в PATH.
    pause
    exit /b 1
)

echo [2/3] Создание/Обновление окружения: %ENV_NAME%...
call conda create -n %ENV_NAME% python=3.10 -y --quiet
call conda run -n %ENV_NAME% python -m pip install pandas requests pyyaml

echo [3/3] Проверка установки...
call conda run -n %ENV_NAME% python -c "import pandas; print('Pandas version:', pandas.__version__)"

echo ========================================
echo [OK] Все готово! Используй 'conda activate %ENV_NAME%'
echo ========================================
pause

pause
