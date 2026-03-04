import os
import yaml
import requests
import json
from datetime import datetime

def run_extract(config_path):
    # 1. Читаем конфиг
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 2. Формируем запрос
    url = f"{config['api']['base_url']}{config['api']['request_template']}"
    params = config['api']['params']
    
    print(f"[*] Extracting World Bank data for variant {config['variant_id']}...")
    
    try:
        # 3. HTTP запрос
        response = requests.get(url, params=params, timeout=config['api']['timeout'])
        response.raise_for_status()
        raw_json = response.json()

        # 4. Сохранение
        # Создаем путь: data/raw/2026-03-04/
        today = datetime.now().strftime("%Y-%m-%d")
        output_dir = os.path.join(config['storage']['raw_dir'], today)
        os.makedirs(output_dir, exist_ok=True)

        filename = f"worldbank_usa_co2_{datetime.now().strftime('%H%M%S')}.json"
        full_path = os.path.join(output_dir, filename)

        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(raw_json, f, ensure_ascii=False, indent=4)

        print(f"[+] Success! Raw data saved to: {full_path}")
        
    except Exception as e:
        print(f"[!] Extract failed: {e}")
