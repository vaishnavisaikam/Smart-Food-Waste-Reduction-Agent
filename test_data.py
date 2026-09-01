import pandas as pd

df = pd.read_csv("data/food_wastage.csv")

print(df.shape)
print(df.columns)
print(df.head())