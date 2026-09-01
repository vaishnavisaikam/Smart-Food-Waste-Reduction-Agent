
import streamlit as st
import pandas as pd

from agent import run_food_waste_agent
from report import generate_report
from history import create_database, save_prediction, get_history


# ============================================================
# DATABASE
# ============================================================

create_database()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Food Waste Reduction Agent",
    page_icon="🍛",
    layout="wide"
)


# ============================================================
# QUICK DASHBOARD
# ============================================================

history = get_history()

st.subheader("📊 Quick Dashboard")

total_predictions = len(history)

if total_predictions > 0:

    average_waste = sum(
        float(row[4]) for row in history
    ) / total_predictions

    high_risk_cases = sum(
        1 for row in history
        if row[5] == "HIGH"
    )

    total_cost_saving = sum(
        float(row[7]) for row in history
    )

else:

    average_waste = 0
    high_risk_cases = 0
    total_cost_saving = 0


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔢 Total Predictions",
        total_predictions
    )

with col2:
    st.metric(
        "♻️ Average Waste",
        f"{average_waste:.2f} units"
    )

with col3:
    st.metric(
        "🔴 High Risk Cases",
        high_risk_cases
    )

with col4:
    st.metric(
        "💰 Total Cost Saving",
        f"₹{total_cost_saving:.0f}"
    )


st.divider()


# ============================================================
# MAIN TITLE
# ============================================================

st.title("🍛 Smart Food Waste Reduction Agent")

st.write(
    "Predict food waste and get AI-powered recommendations."
)

st.divider()


# ============================================================
# FOOD DETAILS
# ============================================================

st.header("🍽️ Food Details")

col1, col2 = st.columns(2)


with col1:

    food_type = st.selectbox(
        "Type of Food",
        [
            "Meat",
            "Vegetables",
            "Fruits",
            "Grains",
            "Dairy"
        ]
    )

    number_of_guests = st.number_input(
        "Number of Guests",
        min_value=1,
        value=200
    )

    event_type = st.selectbox(
        "Event Type",
        [
            "Birthday",
            "Corporate",
            "Wedding",
            "Party",
            "Other"
        ]
    )

    quantity_of_food = st.number_input(
        "Quantity of Food",
        min_value=1,
        value=220
    )

    storage_conditions = st.selectbox(
        "Storage Conditions",
        [
            "Refrigerated",
            "Room Temperature",
            "Frozen"
        ]
    )


with col2:

    purchase_history = st.selectbox(
        "Purchase History",
        [
            "Regular",
            "Occasional"
        ]
    )

    seasonality = st.selectbox(
        "Seasonality",
        [
            "Summer",
            "Winter",
            "Spring",
            "Autumn"
        ]
    )

    preparation_method = st.selectbox(
        "Preparation Method",
        [
            "Buffet",
            "Finger Food",
            "Plated"
        ]
    )

    geographical_location = st.selectbox(
        "Geographical Location",
        [
            "Urban",
            "Suburban",
            "Rural"
        ]
    )

    pricing = st.selectbox(
        "Pricing",
        [
            "Low",
            "Moderate",
            "High"
        ]
    )


st.divider()


# ============================================================
# PREDICTION BUTTON
# ============================================================

if st.button(
    "🤖 Predict Food Waste",
    use_container_width=True
):

    # ========================================================
    # RUN AI AGENT
    # ========================================================

    result = run_food_waste_agent(
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


    # ========================================================
    # AI AGENT RESULT
    # ========================================================

    st.subheader("📊 AI Agent Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Predicted Food Waste",
            f"{result['predicted_waste']} units"
        )

    with col2:
        st.metric(
            "Waste Risk",
            result["risk"]
        )


    # ========================================================
    # AI AGENT INSIGHTS
    # ========================================================

    st.divider()

    st.subheader("🤖 AI Agent Insights")


    if result["risk"] == "HIGH":
        reduction_percent = 20

    elif result["risk"] == "MEDIUM":
        reduction_percent = 10

    else:
        reduction_percent = 0


    suggested_quantity = quantity_of_food * (
        1 - reduction_percent / 100
    )


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🍽️ Current Quantity",
            f"{quantity_of_food} units"
        )

    with col2:
        st.metric(
            "📉 Suggested Quantity",
            f"{suggested_quantity:.1f} units"
        )

    with col3:
        st.metric(
            "♻️ Possible Reduction",
            f"{reduction_percent}%"
        )


    # ========================================================
    # COST SAVING
    # ========================================================

    price_per_unit = {
        "Low": 50,
        "Moderate": 100,
        "High": 150
    }

    estimated_price = price_per_unit[pricing]

    quantity_saved = (
        quantity_of_food - suggested_quantity
    )

    estimated_saving = (
        quantity_saved * estimated_price
    )


    st.metric(
        "💰 Estimated Cost Saving",
        f"₹{estimated_saving:.0f}"
    )


    # ========================================================
    # AI RECOMMENDATION
    # ========================================================

    st.divider()

    st.info(
        f"💡 **AI Recommendation:** "
        f"{result['recommendation']}"
    )


    if result["risk"] == "HIGH":

        st.warning(
            "⚠️ High waste risk detected. "
            "Consider significantly reducing the preparation "
            "quantity and reviewing customer demand."
        )

    elif result["risk"] == "MEDIUM":

        st.warning(
            "⚠️ Moderate waste risk detected. "
            "A small reduction in preparation quantity may "
            "help reduce unnecessary food waste."
        )

    else:

        st.success(
            "✅ Low waste risk detected. "
            "The planned quantity appears reasonable."
        )


    # ========================================================
    # SMART ACTION
    # ========================================================

    st.success(
        f"🌱 **Smart Action:** {result['action']}"
    )


    # ========================================================
    # STORAGE TIP
    # ========================================================

    st.info(
        f"🧊 **Storage Tip:** {result['storage_tip']}"
    )


    # ========================================================
    # FOOD WASTE ANALYSIS
    # ========================================================

    st.divider()

    st.subheader("📈 Food Waste Analysis")


    chart_data = pd.DataFrame(
        {
            "Food Quantity": [
                quantity_of_food,
                suggested_quantity
            ],

            "Waste": [
                result["predicted_waste"],
                result["predicted_waste"]
            ]
        },

        index=[
            "Current Plan",
            "AI Suggested Plan"
        ]
    )


    st.bar_chart(chart_data)


    st.caption(
        "The chart compares the current preparation plan "
        "with the AI-suggested quantity and expected food waste."
    )


    # ========================================================
    # ENVIRONMENTAL IMPACT
    # ========================================================

    st.divider()

    st.subheader("🌱 Environmental Impact")


    food_saved = quantity_saved

    estimated_co2_saved = food_saved * 2.5

    estimated_water_saved = food_saved * 1000


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🍽️ Food Saved",
            f"{food_saved:.1f} units"
        )

    with col2:
        st.metric(
            "🌍 Estimated CO₂ Avoided",
            f"{estimated_co2_saved:.1f} kg"
        )

    with col3:
        st.metric(
            "💧 Estimated Water Saved",
            f"{estimated_water_saved:.0f} L"
        )


    st.info(
        "🌱 By following the AI-suggested preparation quantity, "
        "the system can help reduce unnecessary food waste and "
        "its associated environmental impact."
    )


    # ========================================================
    # WHY THIS RISK LEVEL?
    # ========================================================

    st.subheader("🧠 Why This Risk Level?")


    predicted_waste = result["predicted_waste"]


    if result["risk"] == "HIGH":

        st.error(
            f"🔴 The model predicts {predicted_waste} units "
            "of food waste. This indicates a high waste level. "
            "Reducing preparation quantity and closely "
            "monitoring demand is recommended."
        )

    elif result["risk"] == "MEDIUM":

        st.warning(
            f"🟡 The model predicts {predicted_waste} units "
            "of food waste. This falls within the moderate-risk "
            "range. A small reduction in preparation quantity "
            "can help minimize waste."
        )

    else:

        st.success(
            f"🟢 The model predicts {predicted_waste} units "
            "of food waste. This indicates a low waste level "
            "and the planned quantity appears reasonable."
        )


    # ========================================================
    # PDF REPORT
    # ========================================================

    st.divider()

    st.subheader("📄 Food Waste Report")


    pdf_file = generate_report(
        food_type,
        number_of_guests,
        event_type,
        quantity_of_food,
        storage_conditions,
        purchase_history,
        seasonality,
        preparation_method,
        geographical_location,
        pricing,
        result,
        suggested_quantity,
        reduction_percent,
        estimated_saving
    )


    st.download_button(
        label="📥 Download Food Waste Report",
        data=pdf_file,
        file_name="food_waste_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )


    # ========================================================
    # SAVE PREDICTION
    # ========================================================

    save_prediction(
        food_type,
        number_of_guests,
        quantity_of_food,
        result["predicted_waste"],
        result["risk"],
        suggested_quantity,
        estimated_saving
    )


# ============================================================
# PREDICTION HISTORY
# ============================================================

st.divider()

st.subheader("📋 Prediction History")


history = get_history()


if history:

    history_df = pd.DataFrame(
        history,
        columns=[
            "Date",
            "Food Type",
            "Guests",
            "Current Quantity",
            "Predicted Waste",
            "Risk",
            "Suggested Quantity",
            "Cost Saving"
        ]
    )


    st.dataframe(
        history_df,
        use_container_width=True
    )


else:

    st.info(
        "No prediction history available yet."
    )


# ============================================================
# WASTE TREND ANALYSIS
# ============================================================

if history:

    st.divider()

    st.subheader("📈 Waste Trend Analysis")


    trend_data = pd.DataFrame(
        {
            "Prediction": [
                i + 1
                for i in range(len(history))
            ],

            "Predicted Waste": [
                float(row[4])
                for row in reversed(history)
            ]
        }
    )


    trend_data = trend_data.set_index(
        "Prediction"
    )


    st.line_chart(
        trend_data
    )


    st.caption(
        "This chart shows the predicted food waste "
        "across previous predictions."
    )