import pandas as pd
import os
import json
from datetime import datetime

def run_transform(raw_file_path, output_folder):
    print(f"[*] Начинаем трансформацию файла: {raw_file_path}")
    
    with open(raw_file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    if isinstance(raw_data, list) and len(raw_data) > 1:
        df = pd.json_normalize(raw_data[1])

        cols = {'date': 'year', 'value': 'value', 'countryiso3code': 'country_iso3'}
        df_clean = df[list(cols.keys())].copy()
        df_clean.rename(columns=cols, inplace=True)

        df_clean = df_clean.dropna(subset=['value'])
        df_clean['year'] = df_clean['year'].astype(int)

        os.makedirs(output_folder, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_folder, f"normalized_co2_{ts}.csv")
        
        df_clean.to_csv(output_path, index=False)
        print(f"[+] Данные нормализованы и сохранены: {output_path}")
    else:
        print("[!] В файле нет валидных данных для обработки.")

if __name__ == "__main__":
    pass
