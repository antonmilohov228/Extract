import pandas as pd
from sqlalchemy import create_engine

# Настройки подключения
db_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
engine = create_engine(db_url)

def run_check(title, query):
    print(f"\n=== {title} ===")
    try:
        # Используем pandas для удобного вывода таблицы
        result = pd.read_sql(query, engine)
        print(result)
    except Exception as e:
        print(f"Ошибка при выполнении: {e}")

# Запускаем проверки по одной
run_check("1. Общее количество строк", "SELECT count(*) FROM mart_world_bank_co2;")

run_check("2. Минимальный и максимальный год",
          "SELECT min(year) AS min_year, max(year) AS max_year FROM mart_world_bank_co2;")

run_check("3. Проверка на пустые значения (NULL)",
          "SELECT count(*) FROM mart_world_bank_co2 WHERE year IS NULL OR value IS NULL;")

run_check("4. Поиск дубликатов по годам",
          "SELECT year, count(*) FROM mart_world_bank_co2 GROUP BY year HAVING count(*) > 1;")

run_check("5. Топ-3 года по росту выбросов",
          "SELECT year, growth_rate_pct FROM mart_world_bank_co2 ORDER BY growth_rate_pct DESC LIMIT 3;")