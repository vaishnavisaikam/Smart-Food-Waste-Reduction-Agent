from predictor import predict_waste


def run_food_waste_agent(
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
    # Get prediction from ML model
    predicted_waste = predict_waste(
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
    )

    # Determine waste risk
    if predicted_waste <= 10:
        risk = "LOW"

        recommendation = (
            "Food quantity looks reasonable. "
            "Continue with the planned preparation and monitor actual consumption."
        )

        action = (
            "Maintain the current preparation quantity "
            "and track leftover food."
        )

    elif predicted_waste <= 25:
        risk = "MEDIUM"

        recommendation = (
            "Moderate food waste is expected. "
            "Consider reducing preparation quantity slightly "
            "and monitor customer demand."
        )

        action = (
            "Reduce preparation by around 10% and prepare additional food "
            "only if demand increases."
        )

    else:
        risk = "HIGH"

        recommendation = (
            "High food waste is expected. "
            "Reduce preparation quantity significantly "
            "and monitor demand closely."
        )

        action = (
            "Reduce preparation by around 20% and avoid preparing excess food "
            "until customer demand is confirmed."
        )

    # Food-specific suggestion
    if food_type == "Vegetables":
        storage_tip = (
            "Store vegetables under suitable refrigerated conditions "
            "to maintain freshness."
        )

    elif food_type == "Fruits":
        storage_tip = (
            "Store fruits appropriately and prioritize items "
            "with shorter shelf life."
        )

    elif food_type == "Dairy":
        storage_tip = (
            "Maintain proper refrigeration and use dairy products "
            "according to their shelf life."
        )

    elif food_type == "Meat":
        storage_tip = (
            "Maintain proper refrigeration or freezing "
            "to reduce spoilage."
        )

    else:
        storage_tip = (
            "Store the food under suitable conditions "
            "and monitor leftovers."
        )

    return {
        "predicted_waste": round(predicted_waste, 2),
        "risk": risk,
        "recommendation": recommendation,
        "action": action,
        "storage_tip": storage_tip
    }