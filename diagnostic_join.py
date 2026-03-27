import pandas as pd

left = pd.DataFrame({
    "id": [1, 1, 2],
    "value": [10, 11, 20]
})

right = pd.DataFrame({
    "id": [1, 1, 2],
    "name": ["United States", "USA_Duplicate", "Canada"]
})

print(f"Строк до join: {len(left)}")

right_fixed = right.drop_duplicates(subset=["id"], keep="first")

merged = left.merge(right_fixed, on="id", how="left", validate="many_to_one")

print(f"Строк после join: {len(merged)}")
print("\nИтоговая таблица без раздувания:")
print(merged)