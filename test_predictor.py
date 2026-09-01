from predictor import predict_waste

waste = predict_waste(
    food_type="Meat",
    number_of_guests=300,
    event_type="Corporate",
    quantity_of_food=320,
    storage_conditions="Refrigerated",
    purchase_history="Regular",
    seasonality="Summer",
    preparation_method="Buffet",
    geographical_location="Urban",
    pricing="Moderate"
)

print("Predicted Food Waste:", waste)