# Semester 2 Data Engineering Project (starter)

## Быстрый старт (локально)
1) Создайте venv (Windows PowerShell):
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Установите зависимости:
```powershell
pip install -r requirements.txt
```

3) Проверьте, что Python видит пакет:
```powershell
python -c "import sem2_de; print('ok')"
```

## Запуск (пример)
```powershell
python -m sem2_de.cli --help
python -m sem2_de.cli extract --config ..\configs\variant_01.yml
```

## Что надо сделать вам
- Прочитать свой config в папке ../configs
- Реализовать extract/transform/load под свой source_type
- Добавить проверки качества (dq)
- Сделать ноутбук с EDA и визуализацией
