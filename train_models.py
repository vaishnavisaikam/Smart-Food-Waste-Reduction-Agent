import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("data/food_wastage.csv")

df.columns = df.columns.str.strip()

# -----------------------------
# 2. Features and Target
# -----------------------------
X = df.drop("Wastage Food Amount", axis=1)
y = df["Wastage Food Amount"]

# Convert categorical data into numbers
X = pd.get_dummies(X, drop_first=True)

# -----------------------------
# 3. Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# 4. Define Models
# -----------------------------
models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        random_state=42
    ),

    "MLP Regressor": MLPRegressor(
        hidden_layer_sizes=(100, 50),
        max_iter=1000,
        random_state=42
    )
}

# -----------------------------
# 5. Train and Evaluate
# -----------------------------
results = {}

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(y_test, predictions)

    results[name] = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2   : {r2:.2f}")

# -----------------------------
# 6. Display Results
# -----------------------------
print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

for name, metrics in results.items():

    print(f"\n{name}")
    print(f"MAE  : {metrics['MAE']:.2f}")
    print(f"RMSE : {metrics['RMSE']:.2f}")
    print(f"R2   : {metrics['R2']:.2f}")

# -----------------------------
# 7. Select Best Model
# -----------------------------
best_model_name = min(
    results,
    key=lambda x: results[x]["RMSE"]
)

best_model = models[best_model_name]

print("\n" + "=" * 60)
print(f"BEST MODEL: {best_model_name}")
print("=" * 60)

# -----------------------------
# 8. Save Best Model
# -----------------------------
joblib.dump(best_model, "models/waste_model.pkl")

# Save feature columns
joblib.dump(X.columns.tolist(), "models/feature_columns.pkl")

print("\nBest model saved successfully!")
print("File: models/waste_model.pkl")