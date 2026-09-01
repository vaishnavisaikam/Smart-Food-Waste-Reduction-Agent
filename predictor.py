import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/waste_model.pkl")

# Load the exact feature columns used during training
feature_columns = joblib.load("models/feature_columns.pkl")


def predict_waste(
    food_type,
    number_of_guests,
    event_type,
    quantity_of_food,
    storage_conditions,
    purchase_history,
    seasonality,
    preparation_method,
    geographical_location,
    pricing
):
    # Create input data
    input_data = pd.DataFrame([{
        "Type of Food": food_type,
        "Number of Guests": number_of_guests,
        "Event Type": event_type,
        "Quantity of Food": quantity_of_food,
        "Storage Conditions": storage_conditions,
        "Purchase History": purchase_history,
        "Seasonality": seasonality,
        "Preparation Method": preparation_method,
        "Geographical Location": geographical_location,
        "Pricing": pricing
    }])

    # Convert categorical values into numerical columns
    input_data = pd.get_dummies(input_data, drop_first=True)

    # Match training columns exactly
    input_data = input_data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # Predict waste
    prediction = model.predict(input_data)[0]

    # Prevent negative prediction
    prediction = max(0, prediction)

    return round(prediction, 2)