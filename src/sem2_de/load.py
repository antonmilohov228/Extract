import os
import glob
import pandas as pd
from sqlalchemy import create_engine

def get_latest_mart_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(current_dir))
    mart_dir = os.path.join(root, "data", "mart", "usa_co2_emissions")
    files = glob.glob(os.path.join(mart_dir, "*.csv"))
    if not files:
        raise FileNotFoundError(f"[-] Ошибка: Файлы не найдены в {mart_dir}")
    return max(files, key=os.path.getctime)

def load_to_postgres(df, db_url, table_name, mode="full"):
    engine = create_engine(db_url)
    with engine.begin() as conn:
        if mode == "full":
            df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
            print(f"[+] FULL: Данные ({len(df)} строк) перезаписаны в таблицу {table_name}")
        elif mode == "incremental":
            df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
            print(f"[+] INCREMENTAL: Добавлено {len(df)} новых строк в {table_name}")
