import pandas as pd
from io import StringIO

csv_text = "id;value\n1;10\n2;20\n3;30\n"

print("--- Попытка 1: Ошибка чтения (стандартный sep=',') ---")
df_bad = pd.read_csv(StringIO(csv_text))
print("Dtypes:\n", df_bad.dtypes)
try:
    print(df_bad["value"].mean())
except KeyError:
    print("Ошибка: столбца 'value' не существует, таблица склеилась в одну колонку.\n")

print("--- Попытка 2: Исправленное чтение (sep=';') ---")
df_fixed = pd.read_csv(StringIO(csv_text), sep=";")
print("Dtypes:\n", df_fixed.dtypes)
print("Среднее значение value:", df_fixed["value"].mean())

print("\n--- Тест: Пропуск в данных ---")
csv_text_3 = "id;value\n1;10\n2;\n3;30\n"
df_miss = pd.read_csv(StringIO(csv_text_3), sep=";")
print("Как выглядит таблица с пропуском:\n", df_miss)
print("Dtypes (обрати внимание на float64):\n", df_miss.dtypes)
print("Среднее с учетом пропуска:", df_miss["value"].mean())
