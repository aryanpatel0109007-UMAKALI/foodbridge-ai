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
""", unsafe_allow_html=True)


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

/* Hero animation */
.hero {
    animation: heroEntrance 0.8s ease-out both;
}

@keyframes heroEntrance {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Food photo hover effect */
div[data-testid="stImage"] img {
    border-radius: 15px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

div[data-testid="stImage"] img:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 22px rgba(23, 75, 50, 0.16);
}

/* Card hover effect */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(23, 75, 50, 0.10);
}

/* Premium animated hero banner */
.hero {
    position: relative;
    overflow: hidden;
    background-size: 200% 200%;
    animation: heroEntrance 0.8s ease-out both,
               heroGradient 9s ease-in-out infinite;
}

/* Gentle floating title */
.hero h1 {
    animation: titleFloat 3.5s ease-in-out infinite;
}

/* Floating leaf decoration */
.hero::after {
    content: "🌿";
    position: absolute;
    right: 28px;
    bottom: 8px;
    font-size: 76px;
    opacity: 0.20;
    pointer-events: none;
    animation: leafDrift 5s ease-in-out infinite;
}

/* Moving green gradient */
@keyframes heroGradient {
    0%, 100% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
}

/* Floating title animation */
@keyframes titleFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-4px);
    }
}

/* Floating leaf animation */
@keyframes leafDrift {
    0%, 100% {
        transform: rotate(-8deg) translateY(0);
    }
    50% {
        transform: rotate(8deg) translateY(-12px);
    }
}

/* Respect reduced-motion preferences */
@media (prefers-reduced-motion: reduce) {
    .hero, .hero h1, .hero::after {
        animation: none !important;
    }
}


/* Premium FoodBridge hero graphics */
.hero-layout {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    align-items: center;
    gap: 24px;
}

.hero-copy {
    position: relative;
    z-index: 2;
}

.hero-visual {
    position: relative;
    min-height: 275px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-art-svg {
    width: 100%;
    max-width: 350px;
    height: auto;
    overflow: visible;
    filter: drop-shadow(0 15px 22px rgba(0, 45, 20, .16));
    animation: foodArtFloat 4s ease-in-out infinite;
}

.visual-badge {
    position: absolute;
    z-index: 3;
    padding: 11px 15px;
    border-radius: 14px;
    background: #ffffff;
    color: #175c3a;
    font-size: 13px;
    font-weight: 800;
    box-shadow: 0 8px 24px rgba(0, 40, 20, .17);
    animation: badgeFloat 3.5s ease-in-out infinite;
}

.badge-top {
    top: 20px;
    right: 0;
}

.badge-bottom {
    bottom: 15px;
    left: 0;
    animation-delay: .7s;
}

.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 22px;
}

.hero-pill {
    background: rgba(255,255,255,.13);
    border: 1px solid rgba(255,255,255,.25);
    border-radius: 30px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
}

@keyframes foodArtFloat {
    0%, 100% { transform: translateY(0) rotate(-1deg); }
    50% { transform: translateY(-9px) rotate(1deg); }
}

@keyframes badgeFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

@media (max-width: 700px) {
    .hero-layout {
        grid-template-columns: 1fr;
    }

    .hero-visual {
        min-height: 230px;
        margin-top: 10px;
    }

    .hero-art-svg {
        max-width: 290px;
    }

    .badge-top { right: 2px; }
    .badge-bottom { left: 2px; }
}

@media (prefers-reduced-motion: reduce) {
    .hero-art-svg, .visual-badge {
        animation: none !important;
    }
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
  <div class="hero-layout">
    <div class="hero-copy">
      <div class="tag">SDG 02 · ZERO HUNGER</div>
      <h1>🍃 FoodBridge AI</h1>
      <p>
        Good food deserves a second chance. Connect surplus food
        with community needs, record donations and explore an AI-powered
        priority demonstration — one meal at a time.
      </p>
      <div class="hero-pills">
        <span class="hero-pill">🌱 Reduce Food Waste</span>
        <span class="hero-pill">🤝 Help Communities</span>
        <span class="hero-pill">🍲 Share Hope</span>
      </div>
    </div>

    <div class="hero-visual">
      <div class="visual-badge badge-top">💚 Food Hero</div>

      <svg class="hero-art-svg"
           viewBox="0 0 340 280"
           xmlns="http://www.w3.org/2000/svg"
           role="img"
           aria-label="Illustration of a healthy meal">

        <circle cx="170" cy="140" r="117" fill="#b8f0ca" opacity=".30"/>
        <circle cx="170" cy="140" r="91" fill="#ffffff" opacity=".15"/>

        <ellipse cx="170" cy="224" rx="95" ry="15"
                 fill="#073c29" opacity=".22"/>

        <circle cx="170" cy="137" r="87"
                fill="#ffffff" stroke="#d8f0df" stroke-width="5"/>
        <circle cx="170" cy="137" r="70" fill="#eaf8ed"/>

        <path d="M133 100 Q147 85 157 103 L175 151
                 L152 163 L125 119 Z"
              fill="#f49a43"/>
        <path d="M139 111 L158 150 M134 120 L151 134"
              stroke="#ffcf8d" stroke-width="4" stroke-linecap="round"/>

        <circle cx="194" cy="108" r="19" fill="#3c9f59"/>
        <circle cx="213" cy="120" r="17" fill="#55b56b"/>
        <circle cx="192" cy="129" r="18" fill="#2e8648"/>
        <circle cx="202" cy="110" r="6" fill="#8bdaa0"/>

        <circle cx="198" cy="163" r="19" fill="#e75b52"/>
        <circle cx="192" cy="157" r="5" fill="#ffaaa0"/>
        <path d="M197 145 Q201 137 207 142"
              fill="none" stroke="#348a4b"
              stroke-width="4" stroke-linecap="round"/>

        <path d="M126 177 Q141 151 157 178
                 Q143 192 126 177 Z"
              fill="#76c78a"/>
        <path d="M130 177 L151 174"
              stroke="#e8ffeb" stroke-width="2"/>

        <path d="M95 91 Q71 52 105 43 Q131 53 117 80"
              fill="#8adba1" stroke="#d7ffe0" stroke-width="2"/>
        <path d="M105 83 L103 53"
              stroke="#f0fff3" stroke-width="3"/>

        <path d="M231 182 Q266 159 277 184
                 Q264 209 231 182 Z"
              fill="#55bb73"/>
        <path d="M237 184 L268 184"
              stroke="#c7f7d3" stroke-width="2"/>

        <path d="M154 58 Q145 42 157 34
                 M176 54 Q187 37 179 28"
              stroke="#e8fff0" stroke-width="5"
              stroke-linecap="round" fill="none"
              opacity=".8"/>
      </svg>

      <div class="visual-badge badge-bottom">🍲 Share • Care • Connect</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# FoodBridge AI - Food Photos and Cartoon Cards
st.markdown("## 🌱 Share Food, Share Hope")
st.write("Every meal matters. Help reduce food waste and support our community.")

photo1, photo2, photo3 = st.columns(3)

with photo1:
    with st.container(border=True):
        st.image(
            "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
            "?auto=format&fit=crop&w=600&q=80",
            use_container_width=True
        )
        st.subheader("🥗 Fresh Food")
        st.write("Share surplus food instead of wasting it.")

with photo2:
    with st.container(border=True):
        st.markdown(
            "<div style='background:#e8f6ec; border-radius:16px;"
            "padding:30px; text-align:center;'>"
            "<div style='font-size:75px;'>🧑‍🍳</div>"
            "<h3 style='color:#176440;'>Food Hero</h3>"
            "</div>",
            unsafe_allow_html=True
        )
        st.subheader("🤝 Be a Food Hero")
        st.write("Small acts of kindness can make a difference.")

with photo3:
    with st.container(border=True):
        st.image(
            "https://images.unsplash.com/photo-1547592180-85f173990554"
            "?auto=format&fit=crop&w=600&q=80",
            use_container_width=True
        )
        st.subheader("🍲 Share a Meal")
        st.write("Help connect surplus food with community needs.")

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
    
    priority_col1, priority_col2, priority_col3 = st.columns(3)

    high_count = int((df["Demo Priority"] == "High").sum())
    medium_count = int((df["Demo Priority"] == "Medium").sum())
    low_count = int((df["Demo Priority"] == "Low").sum())

    priority_col1.metric("🔴 High Priority", high_count)
    priority_col2.metric("🟡 Medium Priority", medium_count)
    priority_col3.metric("🟢 Low Priority", low_count)

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
