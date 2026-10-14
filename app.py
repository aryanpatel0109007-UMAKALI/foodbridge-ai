import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(page_title="FoodBridge AI", page_icon="🍲", layout="wide")


# FoodBridge AI - Visual Enhancements
st.markdown("""
<style>
.foodbridge-gallery {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin: 18px 0 24px 0;
}
.foodbridge-card {
    background: white;
    border: 1px solid #dcebe0;
    border-radius: 18px;
    padding: 12px;
    box-shadow: 0 6px 20px rgba(20, 90, 50, 0.07);
    text-align: center;
    transition: transform 0.2s ease;
}
.foodbridge-card:hover {
    transform: translateY(-4px);
}
.foodbridge-card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 12px;
}
.foodbridge-card h4 {
    color: #176440;
    margin: 12px 0 5px 0;
}
.foodbridge-card p {
    color: #62766a;
    font-size: 14px;
    margin-bottom: 4px;
}
@media (max-width: 650px) {
    .foodbridge-gallery {
        grid-template-columns: 1fr;
    }
}
</style>
, unsafe_allow_html=True)
```

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(180deg, #f2f8f2 0%, #ffffff 55%, #eef7f0 100%);
    color: #183b2a;
    font-family: 'Inter', sans-serif;
}
.block-container {
    max-width: 1220px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #174b32 !important;
    font-weight: 800 !important;
}
.hero {
    background: linear-gradient(125deg, #103b2b, #16764b 60%, #42a66a);
    padding: 42px 38px;
    border-radius: 26px;
    margin: 8px 0 26px 0;
    color: white;
    box-shadow: 0 18px 45px rgba(16, 75, 45, .18);
}
.hero .tag {
    color: #c7f7d5;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 14px;
}
.hero h1 {
    color: white !important;
    font-size: clamp(30px, 4vw, 46px);
    line-height: 1.15;
    margin: 0 0 14px 0;
}
.hero p {
    color: #e3f7e9;
    font-size: 16px;
    line-height: 1.8;
    max-width: 720px;
    margin: 0;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #deeadf;
    border-radius: 19px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(23, 75, 50, .06);
}
div[data-testid="stMetricLabel"] {
    color: #647c6b;
    font-weight: 600;
}
div[data-testid="stMetricValue"] {
    color: #16764b;
    font-weight: 800;
}
div[data-testid="stForm"] {
    background: white;
    border: 1px solid #dce9dd;
    border-radius: 22px;
    padding: 26px;
    box-shadow: 0 10px 35px rgba(23, 75, 50, .055);
}
.stTextInput input, .stNumberInput input {
    border-radius: 11px;
    min-height: 43px;
}
.stButton button, .stFormSubmitButton button,
.stDownloadButton button {
    background: linear-gradient(110deg, #16764b, #23945d);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 46px;
    font-weight: 700;
    transition: .2s ease;
}
.stButton button:hover, .stFormSubmitButton button:hover,
.stDownloadButton button:hover {
    background: #105637;
    color: white;
    border: none;
    transform: translateY(-1px);
}
div[data-testid="stAlert"] {
    border-radius: 14px;
}
div[data-testid="stDataFrame"] {
    background: white;
    border: 1px solid #deeadf;
    border-radius: 16px;
    overflow: hidden;
}
hr {
    border-color: #dfebdf;
}
@media (max-width: 700px) {
    .block-container { padding: 1rem; }
    .hero { padding: 27px 22px; border-radius: 20px; }
}
</style>
""", unsafe_allow_html=True)


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


st.markdown("""
<div class="hero">
    <div class="tag">SDG 02 · ZERO HUNGER</div>
    <h1>🍃 FoodBridge AI</h1>
    <p>Good food deserves a second chance. Connect surplus food
    with community needs, record donations and explore an AI-powered
    priority demonstration — one meal at a time.</p>
</div>
""", unsafe_allow_html=True)

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
