import pandas as pd
import os
import glob
from datetime import datetime


def run_mart_pipeline():
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_script_path))

    norm_path = os.path.join(project_root, "data", "normalized", "usa_co2_emissions")
    ref_path = os.path.join(project_root, "reference", "countries.csv")
    mart_dir = os.path.join(project_root, "data", "mart", "usa_co2_emissions")

    files = glob.glob(os.path.join(norm_path, "*.csv"))
    if not files:
        print(f"[!] ОШИБКА: В папке {norm_path} нет CSV файлов.")
        return
    latest_file = max(files, key=os.path.getctime)

    df = pd.read_csv(latest_file)
    ref = pd.read_csv(ref_path, sep=None, engine='python')

    potential_names = ['iso3', 'name', 'region']
    ref.columns = potential_names[:len(ref.columns)]

    print(f"[*] Итоговые колонки в справочнике: {list(ref.columns)}")

    if 'countryiso3code' in df.columns:
        df = df.rename(columns={'countryiso3code': 'country_iso3'})
    if 'date' in df.columns:
        df = df.rename(columns={'date': 'year'})

    df_mart = df.merge(
        ref,
        left_on='country_iso3',
        right_on='iso3',
        how='left'
    )

    if 'iso3' in df_mart.columns:
        df_mart = df_mart.drop(columns=['iso3'])

    df_mart = df_mart.sort_values('year')
    df_mart['prev_val'] = df_mart['value'].shift(1)

    df_mart['abs_change'] = (df_mart['value'] - df_mart['prev_val']).round(4)

    df_mart['growth_rate_pct'] = 0.0
    mask = df_mart['prev_val'] != 0
    df_mart.loc[mask, 'growth_rate_pct'] = ((df_mart['abs_change'] / df_mart['prev_val']) * 100).round(2)

    df_mart = df_mart.drop(columns=['prev_val']).sort_values('year', ascending=False)

    os.makedirs(mart_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(mart_dir, f"mart_co2_usa_{timestamp}.csv")

    df_mart.to_csv(save_path, index=False)
    print(f"[+] ГОТОВО! Витрина создана:\n{save_path}")


run_mart_pipeline()
