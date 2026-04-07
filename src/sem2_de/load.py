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


def load_to_postgres(df, db_url, table_name):
    engine = create_engine(db_url)

    # Блок with engine.begin() автоматически делает commit при успехе
    with engine.begin() as conn:
        df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
        print(f"[+] Данные ({len(df)} строк) успешно загружены в таблицу: {table_name}")


def run_load_pipeline():
    # Строка подключения к базе. Формат: postgresql+psycopg2://пользователь:пароль@хост:порт/имя_базы
    db_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    table_name = "mart_world_bank_co2"

    file_path = get_latest_mart_file()
    print(f"[*] Читаем свежую витрину: {os.path.basename(file_path)}")

    df = pd.read_csv(file_path)
    load_to_postgres(df, db_url, table_name)


run_load_pipeline()