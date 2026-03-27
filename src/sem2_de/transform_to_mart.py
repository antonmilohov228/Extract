import pandas as pd
import os
import glob
from datetime import datetime

def get_latest_file(directory_path):
    files = glob.glob(os.path.join(directory_path, "*.csv"))
    if not files:
        raise FileNotFoundError(f"В папке {directory_path} нет CSV файлов для обработки.")

    return max(files, key=os.path.getctime)

def calculate_kpi(df):
    df = df.sort_values('year', ascending=True)
    df['prev_value'] = df['value'].shift(1)
    df['abs_change'] = df['value'] - df['prev_value']
    df['growth_rate_pct'] = (df['abs_change'] / df['prev_value']) * 100
    df['growth_rate_pct'] = df['growth_rate_pct'].round(2)
    df['abs_change'] = df['abs_change'].round(4)
    df = df.sort_values('year', ascending=False)
    
    return df

norm_dir = os.path.join("..", "data", "normalized", "usa_co2_emissions")
ref_path = os.path.join("..", "reference", "countries.csv")
mart_dir = os.path.join("..", "data", "mart", "usa_co2_emissions")

print("Шаг 1. Поиск свежих данных...")
latest_norm_file = get_latest_file(norm_dir)
print(f"Берем в работу файл: {latest_norm_file}")
df_norm = pd.read_csv(latest_norm_file)

print("Шаг 2. Загрузка справочника...")
df_ref = pd.read_csv(ref_path)

print("Шаг 3. Объединение (JOIN)...")
df_mart = df_norm.merge(
    df_ref[['iso3', 'name', 'region']], 
    left_on='country_iso3', 
    right_on='iso3', 
    how='left'
)

df_mart = df_mart.drop(columns=['iso3'])
df_mart = df_mart.rename(columns={'name': 'country_name'})

print("Шаг 4. Расчет KPI метрик...")
df_mart = calculate_kpi(df_mart)

print("Шаг 5. Сохранение витрины (Mart)...")
os.makedirs(mart_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(mart_dir, f"mart_usa_co2_{timestamp}.csv")

df_mart.to_csv(output_path, index=False)

print(f"\nУспех! Витрина готова. Файл лежит тут:\n{output_path}")
