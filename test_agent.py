from agent import run_food_waste_agent


result = run_food_waste_agent(
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


print("\n🤖 FOOD WASTE AI AGENT")
print("------------------------------")
print("Predicted Waste:", result["predicted_waste"])
print("Waste Risk:", result["risk"])
print("Recommendation:", result["recommendation"])