import pandas as pd
import os

file_name = "out.csv"
df_new = pd.DataFrame({"id": [1, 2], "v": [10, 20]})

def write_idempotent():
    if os.path.exists(file_name):
        df_exist = pd.read_csv(file_name)
        df_combined = pd.concat([df_exist, df_new])
        df_combined = df_combined.drop_duplicates(subset=["id"], keep="last")
        df_combined.to_csv(file_name, index=False)
    else:
        df_new.to_csv(file_name, index=False)

write_idempotent()
print(f"[*] Строк в файле после запуска: {len(pd.read_csv(file_name))}")
