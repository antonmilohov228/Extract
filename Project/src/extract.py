import os
import yaml
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def extract_data():
    config = load_config('configs/variant_XX.yml') 
    api_url = config['api']['endpoint']
    
    api_token = os.getenv('API_TOKEN')
    headers = {
        "Authorization": f"Bearer {api_token}" if api_token else ""
    }

    print(f"Запрос к {api_url}...")

    try:
        response = requests.get(
            api_url, 
            params=config['api']['params'], 
            headers=headers,
            timeout=config['api']['timeout']
        )
        
        response.raise_for_status()
        data = response.json()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"raw_data_{timestamp}.json"
        save_path = os.path.join(config['storage']['raw_dir'], filename)

        os.makedirs(config['storage']['raw_dir'], exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Успех! Данные сохранены в {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")

if __name__ == "__main__":
    extract_data()
