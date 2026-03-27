import pandas as pd
import os

df_norm = pd.read_csv("../data/normalized/usa_co2_emissions/normalized_co2_latest.csv")

ref_data = pd.DataFrame({
    'country_iso3': ['USA'],
    'country_name': ['United States'],
    'region': ['North America']
})

df_mart = df_norm.merge(ref_data, on='country_iso3', how='left')

df_mart = df_mart.sort_values('year')
df_mart['prev_value'] = df_mart['value'].shift(1)
df_mart['abs_change'] = df_mart['value'] - df_mart['prev_value']
df_mart['growth_rate_pct'] = (df_mart['abs_change'] / df_mart['prev_value']) * 100

output_path = "../data/mart/usa_co2_annual_mart.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_mart.to_csv(output_path, index=False)
