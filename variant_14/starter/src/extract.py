import os
import yaml
import requests
import json
from datetime import datetime

def load_config(path="configs/variant_14.yml"):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def extract():
    config = load_config()
    
    url = f"{config['api']['base_url']}{config['api']['endpoint']}"
    params = config['api']['params']
    
    print(f"Запуск Extract для варианта {config['variant_id']}...")
    print(f"Запрос к: {url}")

    try:
        response = requests.get(
            url, 
            params=params, 
            timeout=config['api']['timeout']
        )
        
        response.raise_for_status()
        
        raw_data = response.json()

        raw_dir = config['storage']['raw_dir']
        os.makedirs(raw_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(raw_dir, f"worldbank_usa_co2_{timestamp}.json")

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)

        print(f"Успешно! Сохранено записей: {len(raw_data[1]) if len(raw_data) > 1 else 'N/A'}")
        print(f"Файл: {file_path}")

    except Exception as e:
        print(f"Ошибка при выполнении Extract: {e}")

if __name__ == "__main__":
    extract()
