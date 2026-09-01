import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("data/food_wastage.csv")

# Remove unwanted spaces from column names
df.columns = df.columns.str.strip()

# Display basic information
print("Dataset Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDataset Information:")
print(df.info())

# Separate features and target
X = df.drop("Wastage Food Amount", axis=1)
y = df["Wastage Food Amount"]

# Convert categorical columns into numerical values
X = pd.get_dummies(X, drop_first=True)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)

print("\nPreprocessing Completed Successfully!")