import argparse
import json
import os
import pandas as pd
from datetime import datetime
from extract import run_extract
from transform_to_mart import run_mart_pipeline
from load import load_to_postgres, get_latest_mart_file

def get_state(state_path):
    if os.path.exists(state_path):
        with open(state_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"watermark_year": 0, "last_run": None}

def save_state(state_path, state):
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)

def run_pipeline(config_path, mode):
    print(f"[*] Старт ETL пайплайна. Режим: {mode}")
    state_path = os.path.join("data", "state.json")
    state = get_state(state_path)
    
    run_extract(config_path)
    run_mart_pipeline()
    
    mart_file = get_latest_mart_file()
    df_mart = pd.read_csv(mart_file)
    
    db_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    table_name = "mart_world_bank_co2"
    
    if mode == "incremental":
        watermark = state.get("watermark_year", 0)
        df_mart = df_mart[df_mart['year'] > watermark]
        if df_mart.empty:
            print("[*] Нет новых данных. Watermark актуален.")
            return
            
    load_to_postgres(df_mart, db_url, table_name, mode)
    
    max_year = int(df_mart['year'].max())
    state["watermark_year"] = max_year
    state["last_run"] = datetime.now().isoformat()
    state["mode"] = mode
    save_state(state_path, state)
    print(f"[+] Пайплайн успешно завершен. Текущий Watermark: {max_year}")

parser = argparse.ArgumentParser()
parser.add_argument("--config", required=True)
parser.add_argument("--mode", choices=["full", "incremental"], default="full")
args = parser.parse_args()

run_pipeline(args.config, args.mode)
