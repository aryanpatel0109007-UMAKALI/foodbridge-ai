import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(page_title="FoodBridge AI", page_icon="🍲", layout="wide")

# IMPORTANT: this is a demo model trained on artificial practice data.
# It is not a food-safety assessment or a real-world donation priority model.
training_df = pd.DataFrame({"hours_until_expiry": list(range(1, 16))})
training_df["priority"] = training_df["hours_until_expiry"].apply(
    lambda hours: "High" if hours <= 3 else ("Medium" if hours <= 8 else "Low")
)
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(training_df[["hours_until_expiry"]], training_df["priority"])

if "donations" not in st.session_state:
    st.session_state.donations = []

st.title("🍲 FoodBridge AI — Zero Hunger")
st.write("Register surplus-food donations and view a simple donation dashboard.")
st.warning(
    "Demo only: priority is predicted from artificial practice data. "
    "It does not determine whether food is safe to eat. Do not enter private information."
)

st.subheader("Register a food donation")
with st.form("donation_form", clear_on_submit=True):
    food = st.text_input("Food name", placeholder="e.g. Gujarati Thali")
    location = st.text_input("Location", placeholder="e.g. Kuvasana")
    meals = st.number_input("Number of meals", min_value=0, step=1, value=0)
    hours = st.number_input("Hours until expiry", min_value=0.0, step=1.0, value=0.0)
    submitted = st.form_submit_button("Save donation")

if submitted:
    if not food.strip():
        st.error("Please enter a food name.")
    elif not location.strip():
        st.error("Please enter a location.")
    elif meals <= 0:
        st.error("Enter a number of meals greater than zero.")
    else:
        prediction = model.predict(
            pd.DataFrame({"hours_until_expiry": [float(hours)]})
        )[0]
        st.session_state.donations.append({
            "Food": food.strip(),
            "Meals": int(meals),
            "Hours Until Expiry": float(hours),
            "Location": location.strip(),
            "Demo Priority": prediction,
        })
        st.success(f"Donation added to this app session. Demonstration priority: {prediction}")

st.divider()
st.subheader("Donation dashboard")
df = pd.DataFrame(st.session_state.donations, columns=[
    "Food", "Meals", "Hours Until Expiry", "Location", "Demo Priority"
])
total_donations = len(df)
total_meals = int(df["Meals"].sum()) if not df.empty else 0
col1, col2 = st.columns(2)
col1.metric("Total donations in this session", total_donations)
col2.metric("Total meals recorded", total_meals)

if df.empty:
    st.info("No donations added yet. Enter a donation in the form above to see it here.")
else:
    st.dataframe(df, use_container_width=True, hide_index=True)
    totals_by_location = df.groupby("Location", as_index=True)["Meals"].sum().sort_values(ascending=False)
    st.subheader("Meals recorded by location")
    st.bar_chart(totals_by_location)
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download donations as CSV",
        data=csv_bytes,
        file_name="foodbridge_donations.csv",
        mime="text/csv",
    )

st.caption(
    "Storage note: this beginner deployment keeps donations only in the current browser session. "
    "Download the CSV to keep a copy. A persistent database is needed before real-world use."
)
