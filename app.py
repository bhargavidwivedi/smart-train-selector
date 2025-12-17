
# app.py

import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import plotly.graph_objects as go

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, "final_train_dataset_with_routes.csv")
MODEL_PATH = os.path.join(BASE_DIR, "train_confirmation_bundle.pkl")

df = pd.read_csv(CSV_PATH)
bundle = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Train Selector",
    page_icon="🚆",
    layout="centered"
)

# ---------------------------------------------------------
# GLOBAL STYLES – COPILOT-STYLE PREMIUM DASHBOARD
# ---------------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #020617;
    margin: 0;
    padding: 0;
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Main app background + subtle vignette */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, rgba(56,189,248,0.06), transparent 55%),
                radial-gradient(circle at bottom, rgba(129,140,248,0.05), transparent 60%),
                #020617;
}

/* Remove default padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* HEADER AREA */
.header-shell {
    position: relative;
    border-radius: 20px;
    padding: 26px 24px 20px 24px;
    margin-bottom: 18px;
    background: radial-gradient(circle at top, rgba(56,189,248,0.12), rgba(15,23,42,0.98));
    border: 1px solid rgba(148,163,184,0.35);
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 40px rgba(37,99,235,0.5);
    overflow: hidden;
}

/* Soft halo behind header */
.header-shell::before {
    content: "";
    position: absolute;
    inset: -40%;
    background:
        radial-gradient(circle at top, rgba(56,189,248,0.22), transparent 55%),
        radial-gradient(circle at center, rgba(129,140,248,0.16), transparent 60%);
    opacity: 0.7;
    z-index: -1;
}

/* Thin glowing border shimmer */
.header-shell::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(120deg,
        rgba(56,189,248,0.0),
        rgba(56,189,248,0.35),
        rgba(45,212,191,0.25),
        rgba(129,140,248,0.35),
        rgba(56,189,248,0.0)
    );
    opacity: 0.35;
    mix-blend-mode: screen;
    animation: border-pulse 9s linear infinite;
    pointer-events: none;
}

/* Title */
.big-title {
    font-size: 40px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #22c1c3, #818cf8);
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 6px;
}

/* AI subtitle */
.ai-subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 16px;
    opacity: 0.9;
    margin-top: 0px;
}

/* Decorative AI divider */
.ai-divider {
    width: 220px;
    height: 1px;
    margin: 14px auto 4px auto;
    position: relative;
    background: linear-gradient(90deg,
        rgba(15,23,42,0),
        rgba(56,189,248,0.7),
        rgba(45,212,191,0.7),
        rgba(129,140,248,0.7),
        rgba(15,23,42,0)
    );
    opacity: 0.85;
}

.ai-divider::before {
    content: "";
    position: absolute;
    top: -2px;
    left: 50%;
    width: 56px;
    height: 5px;
    border-radius: 999px;
    transform: translateX(-50%);
    background: radial-gradient(circle, rgba(148,163,184,0.9), transparent 70%);
    opacity: 0.9;
}

/* Subheader caption under divider */
.header-caption {
    text-align: center;
    font-size: 13px;
    color: #94a3b8;
    margin-top: 6px;
}

/* INFO CARDS WRAPPER */
.info-row {
    display: flex;
    justify-content: center;
    gap: 18px;
    margin: 18px auto 8px auto;
    max-width: 980px;
}

/* Individual info card */
.info-card {
    flex: 1;
    min-width: 0;
    border-radius: 18px;
    padding: 14px 16px 13px 16px;
    background: linear-gradient(135deg,
            rgba(15,23,42,0.9),
            rgba(15,23,42,0.92)
        ),
        radial-gradient(circle at top left, rgba(56,189,248,0.18), transparent 55%);
    border: 1px solid rgba(148,163,184,0.45);
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 24px rgba(15,23,42,0.7);
    position: relative;
    overflow: hidden;
}

/* Neon-like top edge highlight */
.info-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 6%;
    right: 6%;
    height: 2px;
    background: linear-gradient(90deg,
        rgba(56,189,248,0.0),
        rgba(56,189,248,0.85),
        rgba(45,212,191,0.7),
        rgba(129,140,248,0.85),
        rgba(56,189,248,0.0)
    );
    opacity: 0.75;
}

/* Soft ambient glow band */
.info-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top,
        rgba(56,189,248,0.25),
        transparent 60%);
    opacity: 0;
    transition: opacity 0.25s ease-out;
}

/* Hover - very subtle */
.info-card:hover::after {
    opacity: 0.18;
}

.info-icon {
    font-size: 18px;
    margin-bottom: 3px;
}

.info-title {
    font-size: 13px;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 2px;
}

.info-text {
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.3;
}

/* JOURNEY CARD */
.journey-shell {
    margin-top: 18px;
    margin-bottom: 10px;
    border-radius: 20px;
    padding: 18px 18px 20px 18px;
    max-width: 980px;
    margin-left: auto;
    margin-right: auto;
    background:
        linear-gradient(145deg,
            rgba(15,23,42,0.94),
            rgba(15,23,42,0.98)),
        radial-gradient(circle at top right,
            rgba(56,189,248,0.18),
            transparent 60%);
    border: 1px solid rgba(148,163,184,0.5);
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 40px rgba(15,23,42,1);
    position: relative;
    overflow: hidden;
}

/* Soft gradient border shimmer around journey card */
.journey-shell::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    background: conic-gradient(
        from 180deg,
        rgba(56,189,248,0.2),
        rgba(45,212,191,0.15),
        rgba(129,140,248,0.2),
        rgba(56,189,248,0.2)
    );
    opacity: 0.23;
    mix-blend-mode: screen;
    z-index: -2;
}

.journey-shell::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(circle at top,
        rgba(56,189,248,0.09),
        transparent 55%);
    opacity: 0.95;
    z-index: -1;
}

/* Journey.title */
.journey-title {
    font-size: 16px;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 6px;
}

/* Journey subtitle line */
.journey-subtitle {
    font-size: 12px;
    color: #9ca3af;
    margin-bottom: 14px;
}

/* FIELD LABELS */
.stSelectbox label, .stDateInput label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}

/* Glowing focus outline for selectboxes/date */
[data-testid="stSelectbox"] > div:focus-within,
[data-testid="stDateInput"] > div:focus-within {
    box-shadow: 0 0 0 1px rgba(56,189,248,0.7),
                0 0 0 4px rgba(56,189,248,0.25);
    border-radius: 12px;
}

/* Predict button container */
.predict-btn-wrapper {
    margin-top: 10px;
}

/* Predict button styling */
.predict-btn-wrapper button {
    width: 100%;
    padding: 12px;
    border-radius: 14px;
    background: linear-gradient(90deg,
        #38bdf8,
        #22c1c3,
        #818cf8
    );
    color: #020617 !important;
    font-weight: 700;
    border: none;
    box-shadow:
        0 0 20px rgba(56,189,248,0.55),
        0 0 40px rgba(15,23,42,1);
    transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
}

.predict-btn-wrapper button:hover {
    transform: translateY(-1px);
    filter: brightness(1.07);
    box-shadow:
        0 0 24px rgba(56,189,248,0.9),
        0 0 50px rgba(15,23,42,1);
}

/* RESULTS CARD WRAPPER */
.results-shell {
    margin-top: 18px;
    max-width: 980px;
    margin-left: auto;
    margin-right: auto;
}

/* Train card */
.train-card {
    margin-top: 10px;
    background:
        linear-gradient(145deg,
            rgba(15,23,42,0.98),
            rgba(15,23,42,0.96)),
        radial-gradient(circle at top left,
            rgba(56,189,248,0.16),
            transparent 55%);
    border-radius: 18px;
    padding: 16px 18px 14px 18px;
    border: 1px solid rgba(148,163,184,0.55);
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 24px rgba(15,23,42,0.9);
    position: relative;
    overflow: hidden;
}

/* Neon-like left edge for train card */
.train-card::before {
    content: "";
    position: absolute;
    top: 6%;
    bottom: 6%;
    left: 0;
    width: 2px;
    background: linear-gradient(180deg,
        rgba(56,189,248,0.0),
        rgba(56,189,248,0.9),
        rgba(45,212,191,0.8),
        rgba(129,140,248,0.9),
        rgba(56,189,248,0.0)
    );
    opacity: 0.9;
}

/* Subtle pulse on train card border */
.train-card::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(circle at top,
        rgba(56,189,248,0.18),
        transparent 60%);
    opacity: 0;
    transition: opacity 0.25s ease-out;
}

.train-card:hover::after {
    opacity: 0.16;
}

.train-title {
    font-size: 18px;
    font-weight: 600;
    color: #e5e7eb;
}

/* BEST badge */
.best-badge {
    display: inline-block;
    background: linear-gradient(120deg, #22c55e, #4ade80);
    padding: 4px 10px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 11px;
    color: #022c22;
    margin-top: 4px;
}

/* Animated progress ring */
.progress-ring {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background:
        conic-gradient(#38bdf8 calc(var(--p)*1%), #0b1220 0);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 8px auto 6px auto;
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 20px rgba(56,189,248,0.42);
}

.progress-ring-inner {
    text-align: center;
    color: #f9fafb;
    font-weight: 700;
}

.progress-ring-inner-main {
    font-size: 20px;
}

.progress-ring-inner-label {
    font-size: 11px;
    font-weight: 500;
    opacity: 0.85;
}

/* Footer */
.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 32px;
    padding-bottom: 16px;
    font-size: 12px;
}

/* Vignette and subtle grid feel on page edges */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        radial-gradient(circle at top left, rgba(15,23,42,0.75), transparent 55%),
        radial-gradient(circle at top right, rgba(15,23,42,0.9), transparent 60%),
        radial-gradient(circle at bottom, rgba(15,23,42,0.75), transparent 60%);
    mix-blend-mode: multiply;
    opacity: 0.9;
    z-index: -1;
}

/* Border shimmer animation */
@keyframes border-pulse {
    0% { transform: translate3d(-10%, 0, 0); opacity: 0.4; }
    50% { transform: translate3d(10%, 0, 0); opacity: 0.7; }
    100% { transform: translate3d(-10%, 0, 0); opacity: 0.4; }
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER AREA
# ---------------------------------------------------------
st.markdown('<div class="header-shell">', unsafe_allow_html=True)
st.markdown('<div class="big-title">Smart Train Selector</div>', unsafe_allow_html=True)
st.markdown('<div class="ai-subtitle">Tell me your journey details and I’ll recommend trains with the highest ticket confirmation chances.</div>', unsafe_allow_html=True)
st.markdown('<div class="ai-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="header-caption">AI-powered, data-driven suggestions tailored for Indian Railways routes.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# INFO CARDS – FILL SPACE INTELLIGENTLY
# ---------------------------------------------------------
st.markdown('<div class="info-row">', unsafe_allow_html=True)

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">🤖</div>
            <div class="info-title">AI-Powered Prediction</div>
            <div class="info-text">
                Learns from past waitlists, delays, and seasonal patterns to rank trains for you.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">📊</div>
            <div class="info-title">Realistic Confirmation Probability</div>
            <div class="info-text">
                Each score reflects how likely your ticket is to confirm before your journey date.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_info3:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">🇮🇳</div>
            <div class="info-title">Optimized for Indian Railways</div>
            <div class="info-text">
                Trained on real Indian routes, classes, and congestion behavior across major corridors.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD DATA & MODEL
# ---------------------------------------------------------
CSV_PATH = r"C:\\Users\\Aditya Dwivedi\\OneDrive\\Desktop\\IRCTC PROJECT\\smart-train-selector\\final_train_dataset_with_routes.csv"
df = pd.read_csv(CSV_PATH)

df.columns = df.columns.str.strip().str.lower()
for col in ["source", "destination", "train_type", "class", "train_name"]:
    df[col] = df[col].astype(str).str.strip()

MODEL_PATH = r"C:\\Users\\Aditya Dwivedi\\OneDrive\\Desktop\\IRCTC PROJECT\\smart-train-selector\\train_confirmation_bundle.pkl"
model_bundle = joblib.load(MODEL_PATH)

model = model_bundle["model"]
train_type_le = model_bundle["train_type_le"]
class_mapping = model_bundle["class_mapping"]

# ---------------------------------------------------------
# JOURNEY DETAILS – GLASS CARD WITH ICON FIELDS
# ---------------------------------------------------------
st.markdown('<div class="journey-shell">', unsafe_allow_html=True)
st.markdown('<div class="journey-title">Journey Details</div>', unsafe_allow_html=True)
st.markdown('<div class="journey-subtitle">Describe your trip and I’ll compare trains by safety and confirmation probability.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    user_class = st.selectbox("🎟️ Class", sorted(df["class"].unique()))

with col2:
    source = st.selectbox("📍 Source Station", sorted(df["source"].unique()))

with col3:
    destination = st.selectbox("🚉 Destination Station", sorted(df["destination"].unique()))

journey_date = st.date_input("📅 Journey Date", datetime.today())

st.markdown('<div class="predict-btn-wrapper">', unsafe_allow_html=True)
predict_btn = st.button("✨ Predict Best Trains")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PREDICTION LOGIC
# ---------------------------------------------------------
def get_top_trains(df_route, user_class_value):
    user_class_encoded = class_mapping[user_class_value]

    df_local = df_route.copy()
    df_local["long_route"] = (df_local["duration_hours"] > 24).astype(int)
    df_local["wl_ratio"] = df_local.apply(
        lambda row: row["wl_position"] / {"SL": 100, "3A": 72, "2A": 48}.get(row["class"], 100),
        axis=1
    )
    df_local["delay_risk"] = (df_local["avg_delay_min"] > 30).astype(int)
    df_local["booking_urgency"] = pd.cut(
        df_local["days_before_journey"],
        bins=[-1, 3, 15, 365],
        labels=[0, 1, 2]
    ).astype(int)
    df_local["congestion_per_halt"] = df_local["route_congestion"] / df_local["halts"]
    df_local["train_type_enc"] = train_type_le.transform(df_local["train_type"])
    df_local["class_enc"] = df_local["class"].map(class_mapping)

    features = [
        "train_type_enc", "class_enc", "halts", "duration_hours",
        "train_frequency", "days_before_journey", "weekday", "is_weekend",
        "festival_flag", "route_congestion", "wl_position", "avg_delay_min",
        "delay_risk", "long_route", "wl_ratio", "booking_urgency",
        "congestion_per_halt"
    ]

    X = df_local[features]
    df_local["pred_prob"] = model.predict_proba(X)[:, 1]

    filtered = df_local[df_local["class_enc"] == user_class_encoded]
    filtered = filtered.sort_values(by="pred_prob", ascending=False)
    filtered = filtered.drop_duplicates(subset=["train_no", "train_name"], keep="first")

    return filtered.sort_values(by="pred_prob", ascending=False)

# ---------------------------------------------------------
# GAUGE CHART – SUBTLE, PREMIUM COLORS
# ---------------------------------------------------------
def probability_gauge(prob, key):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        number={'suffix': '%', 'font': {'color': '#e5e7eb'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#64748b'},
            'bgcolor': '#020617',
            'bordercolor': '#020617',
            'bar': {'color': "#38bdf8"},
            'steps': [
                {'range': [0, 45], 'color': '#111827'},
                {'range': [45, 75], 'color': '#1f2937'},
                {'range': [75, 100], 'color': '#1d4ed8'}
            ],
        },
        title={'text': "Confirmation Chance", 'font': {'color': '#9ca3af', 'size': 12}}
    ))
    fig.update_layout(
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig, use_container_width=True, key=key)

# ---------------------------------------------------------
# FILTER ROUTE
# ---------------------------------------------------------
route_df = df[
    (df["source"].str.lower() == source.lower()) &
    (df["destination"].str.lower() == destination.lower())
]

# ---------------------------------------------------------
# DISPLAY RESULTS – INSIDE PREMIUM WRAPPER
# ---------------------------------------------------------
st.markdown('<div class="results-shell">', unsafe_allow_html=True)

if predict_btn:
    if route_df.empty:
        st.warning("No trains found for this route.")
    else:
        top_trains = get_top_trains(route_df, user_class)

        if top_trains.empty:
            st.warning("No trains found for this class.")
        else:
            st.markdown("#### 🚆 Recommended trains for your journey")

            for idx, row in top_trains.iterrows():
                is_best = idx == top_trains.index[0]
                probability_value = row.pred_prob * 100

                st.markdown(
                    f"""
                    <div class="train-card">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px;">
                            <div style="flex:1;">
                                <div class="train-title">{row.train_name} ({row.train_no})</div>
                                <div style="font-size:12px; color:#9ca3af; margin-top:2px;">
                                    From <b>{row.source}</b> to <b>{row.destination}</b> · Class <b>{row['class']}</b>
                                </div>
                                <div style="font-size:11px; color:#6b7280; margin-top:4px;">
                                    Halts: {row.halts} · Avg delay: {int(row.avg_delay_min)} min · WL position: {int(row.wl_position)}
                                </div>
                                {f'<span class="best-badge">BEST MATCH</span>' if is_best else ''}
                            </div>
                            <div style="width:130px; text-align:center;">
                                <div class="progress-ring" style="--p:{probability_value:.0f}">
                                    <div class="progress-ring-inner">
                                        <div class="progress-ring-inner-main">{probability_value:.0f}%</div>
                                        <div class="progress-ring-inner-label">Chance</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                probability_gauge(row.pred_prob, key=f"gauge_{row.train_no}_{idx}")

                if row.pred_prob >= 0.75:
                    st.success("High confirmation chance – strongly recommended.")
                elif row.pred_prob >= 0.45:
                    st.warning("Moderate confirmation chance – consider as a backup option.")
                else:
                    st.info("Low confirmation chance – book only if flexible with plans.")

                st.divider()

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown('<div class="footer">Smart Train Selector · AI-powered decision assistant for Indian Railways journeys</div>', unsafe_allow_html=True)
# app.py

import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import plotly.graph_objects as go

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Train Selector",
    page_icon="🚆",
    layout="centered"
)

# ---------------------------------------------------------
# GLOBAL STYLES – COPILOT-STYLE PREMIUM DASHBOARD
# ---------------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #020617;
    margin: 0;
    padding: 0;
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Main app background + subtle vignette */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, rgba(56,189,248,0.06), transparent 55%),
                radial-gradient(circle at bottom, rgba(129,140,248,0.05), transparent 60%),
                #020617;
}

/* Remove default padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* HEADER AREA */
.header-shell {
    position: relative;
    border-radius: 20px;
    padding: 26px 24px 20px 24px;
    margin-bottom: 18px;
    background: radial-gradient(circle at top, rgba(56,189,248,0.12), rgba(15,23,42,0.98));
    border: 1px solid rgba(148,163,184,0.35);
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 40px rgba(37,99,235,0.5);
    overflow: hidden;
}

/* Soft halo behind header */
.header-shell::before {
    content: "";
    position: absolute;
    inset: -40%;
    background:
        radial-gradient(circle at top, rgba(56,189,248,0.22), transparent 55%),
        radial-gradient(circle at center, rgba(129,140,248,0.16), transparent 60%);
    opacity: 0.7;
    z-index: -1;
}

/* Thin glowing border shimmer */
.header-shell::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(120deg,
        rgba(56,189,248,0.0),
        rgba(56,189,248,0.35),
        rgba(45,212,191,0.25),
        rgba(129,140,248,0.35),
        rgba(56,189,248,0.0)
    );
    opacity: 0.35;
    mix-blend-mode: screen;
    animation: border-pulse 9s linear infinite;
    pointer-events: none;
}

/* Title */
.big-title {
    font-size: 40px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #22c1c3, #818cf8);
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 6px;
}

/* AI subtitle */
.ai-subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 16px;
    opacity: 0.9;
    margin-top: 0px;
}

/* Decorative AI divider */
.ai-divider {
    width: 220px;
    height: 1px;
    margin: 14px auto 4px auto;
    position: relative;
    background: linear-gradient(90deg,
        rgba(15,23,42,0),
        rgba(56,189,248,0.7),
        rgba(45,212,191,0.7),
        rgba(129,140,248,0.7),
        rgba(15,23,42,0)
    );
    opacity: 0.85;
}

.ai-divider::before {
    content: "";
    position: absolute;
    top: -2px;
    left: 50%;
    width: 56px;
    height: 5px;
    border-radius: 999px;
    transform: translateX(-50%);
    background: radial-gradient(circle, rgba(148,163,184,0.9), transparent 70%);
    opacity: 0.9;
}

/* Subheader caption under divider */
.header-caption {
    text-align: center;
    font-size: 13px;
    color: #94a3b8;
    margin-top: 6px;
}

/* INFO CARDS WRAPPER */
.info-row {
    display: flex;
    justify-content: center;
    gap: 18px;
    margin: 18px auto 8px auto;
    max-width: 980px;
}

/* Individual info card */
.info-card {
    flex: 1;
    min-width: 0;
    border-radius: 18px;
    padding: 14px 16px 13px 16px;
    background: linear-gradient(135deg,
            rgba(15,23,42,0.9),
            rgba(15,23,42,0.92)
        ),
        radial-gradient(circle at top left, rgba(56,189,248,0.18), transparent 55%);
    border: 1px solid rgba(148,163,184,0.45);
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 24px rgba(15,23,42,0.7);
    position: relative;
    overflow: hidden;
}

/* Neon-like top edge highlight */
.info-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 6%;
    right: 6%;
    height: 2px;
    background: linear-gradient(90deg,
        rgba(56,189,248,0.0),
        rgba(56,189,248,0.85),
        rgba(45,212,191,0.7),
        rgba(129,140,248,0.85),
        rgba(56,189,248,0.0)
    );
    opacity: 0.75;
}

/* Soft ambient glow band */
.info-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top,
        rgba(56,189,248,0.25),
        transparent 60%);
    opacity: 0;
    transition: opacity 0.25s ease-out;
}

/* Hover - very subtle */
.info-card:hover::after {
    opacity: 0.18;
}

.info-icon {
    font-size: 18px;
    margin-bottom: 3px;
}

.info-title {
    font-size: 13px;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 2px;
}

.info-text {
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.3;
}

/* JOURNEY CARD */
.journey-shell {
    margin-top: 18px;
    margin-bottom: 10px;
    border-radius: 20px;
    padding: 18px 18px 20px 18px;
    max-width: 980px;
    margin-left: auto;
    margin-right: auto;
    background:
        linear-gradient(145deg,
            rgba(15,23,42,0.94),
            rgba(15,23,42,0.98)),
        radial-gradient(circle at top right,
            rgba(56,189,248,0.18),
            transparent 60%);
    border: 1px solid rgba(148,163,184,0.5);
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 40px rgba(15,23,42,1);
    position: relative;
    overflow: hidden;
}

/* Soft gradient border shimmer around journey card */
.journey-shell::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    background: conic-gradient(
        from 180deg,
        rgba(56,189,248,0.2),
        rgba(45,212,191,0.15),
        rgba(129,140,248,0.2),
        rgba(56,189,248,0.2)
    );
    opacity: 0.23;
    mix-blend-mode: screen;
    z-index: -2;
}

.journey-shell::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(circle at top,
        rgba(56,189,248,0.09),
        transparent 55%);
    opacity: 0.95;
    z-index: -1;
}

/* Journey.title */
.journey-title {
    font-size: 16px;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 6px;
}

/* Journey subtitle line */
.journey-subtitle {
    font-size: 12px;
    color: #9ca3af;
    margin-bottom: 14px;
}

/* FIELD LABELS */
.stSelectbox label, .stDateInput label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}

/* Glowing focus outline for selectboxes/date */
[data-testid="stSelectbox"] > div:focus-within,
[data-testid="stDateInput"] > div:focus-within {
    box-shadow: 0 0 0 1px rgba(56,189,248,0.7),
                0 0 0 4px rgba(56,189,248,0.25);
    border-radius: 12px;
}

/* Predict button container */
.predict-btn-wrapper {
    margin-top: 10px;
}

/* Predict button styling */
.predict-btn-wrapper button {
    width: 100%;
    padding: 12px;
    border-radius: 14px;
    background: linear-gradient(90deg,
        #38bdf8,
        #22c1c3,
        #818cf8
    );
    color: #020617 !important;
    font-weight: 700;
    border: none;
    box-shadow:
        0 0 20px rgba(56,189,248,0.55),
        0 0 40px rgba(15,23,42,1);
    transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
}

.predict-btn-wrapper button:hover {
    transform: translateY(-1px);
    filter: brightness(1.07);
    box-shadow:
        0 0 24px rgba(56,189,248,0.9),
        0 0 50px rgba(15,23,42,1);
}

/* RESULTS CARD WRAPPER */
.results-shell {
    margin-top: 18px;
    max-width: 980px;
    margin-left: auto;
    margin-right: auto;
}

/* Train card */
.train-card {
    margin-top: 10px;
    background:
        linear-gradient(145deg,
            rgba(15,23,42,0.98),
            rgba(15,23,42,0.96)),
        radial-gradient(circle at top left,
            rgba(56,189,248,0.16),
            transparent 55%);
    border-radius: 18px;
    padding: 16px 18px 14px 18px;
    border: 1px solid rgba(148,163,184,0.55);
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 24px rgba(15,23,42,0.9);
    position: relative;
    overflow: hidden;
}

/* Neon-like left edge for train card */
.train-card::before {
    content: "";
    position: absolute;
    top: 6%;
    bottom: 6%;
    left: 0;
    width: 2px;
    background: linear-gradient(180deg,
        rgba(56,189,248,0.0),
        rgba(56,189,248,0.9),
        rgba(45,212,191,0.8),
        rgba(129,140,248,0.9),
        rgba(56,189,248,0.0)
    );
    opacity: 0.9;
}

/* Subtle pulse on train card border */
.train-card::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(circle at top,
        rgba(56,189,248,0.18),
        transparent 60%);
    opacity: 0;
    transition: opacity 0.25s ease-out;
}

.train-card:hover::after {
    opacity: 0.16;
}

.train-title {
    font-size: 18px;
    font-weight: 600;
    color: #e5e7eb;
}

/* BEST badge */
.best-badge {
    display: inline-block;
    background: linear-gradient(120deg, #22c55e, #4ade80);
    padding: 4px 10px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 11px;
    color: #022c22;
    margin-top: 4px;
}

/* Animated progress ring */
.progress-ring {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background:
        conic-gradient(#38bdf8 calc(var(--p)*1%), #0b1220 0);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 8px auto 6px auto;
    box-shadow:
        0 0 0 1px rgba(15,23,42,1),
        0 0 20px rgba(56,189,248,0.42);
}

.progress-ring-inner {
    text-align: center;
    color: #f9fafb;
    font-weight: 700;
}

.progress-ring-inner-main {
    font-size: 20px;
}

.progress-ring-inner-label {
    font-size: 11px;
    font-weight: 500;
    opacity: 0.85;
}

/* Footer */
.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 32px;
    padding-bottom: 16px;
    font-size: 12px;
}

/* Vignette and subtle grid feel on page edges */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        radial-gradient(circle at top left, rgba(15,23,42,0.75), transparent 55%),
        radial-gradient(circle at top right, rgba(15,23,42,0.9), transparent 60%),
        radial-gradient(circle at bottom, rgba(15,23,42,0.75), transparent 60%);
    mix-blend-mode: multiply;
    opacity: 0.9;
    z-index: -1;
}

/* Border shimmer animation */
@keyframes border-pulse {
    0% { transform: translate3d(-10%, 0, 0); opacity: 0.4; }
    50% { transform: translate3d(10%, 0, 0); opacity: 0.7; }
    100% { transform: translate3d(-10%, 0, 0); opacity: 0.4; }
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER AREA
# ---------------------------------------------------------
st.markdown('<div class="header-shell">', unsafe_allow_html=True)
st.markdown('<div class="big-title">Smart Train Selector</div>', unsafe_allow_html=True)
st.markdown('<div class="ai-subtitle">Tell me your journey details and I’ll recommend trains with the highest ticket confirmation chances.</div>', unsafe_allow_html=True)
st.markdown('<div class="ai-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="header-caption">AI-powered, data-driven suggestions tailored for Indian Railways routes.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# INFO CARDS – FILL SPACE INTELLIGENTLY
# ---------------------------------------------------------
st.markdown('<div class="info-row">', unsafe_allow_html=True)

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">🤖</div>
            <div class="info-title">AI-Powered Prediction</div>
            <div class="info-text">
                Learns from past waitlists, delays, and seasonal patterns to rank trains for you.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">📊</div>
            <div class="info-title">Realistic Confirmation Probability</div>
            <div class="info-text">
                Each score reflects how likely your ticket is to confirm before your journey date.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_info3:
    st.markdown("""
        <div class="info-card">
            <div class="info-icon">🇮🇳</div>
            <div class="info-title">Optimized for Indian Railways</div>
            <div class="info-text">
                Trained on real Indian routes, classes, and congestion behavior across major corridors.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD DATA & MODEL
# ---------------------------------------------------------
CSV_PATH = r"C:\\Users\\Aditya Dwivedi\\OneDrive\\Desktop\\IRCTC PROJECT\\smart-train-selector\\final_train_dataset_with_routes.csv"
df = pd.read_csv(CSV_PATH)

df.columns = df.columns.str.strip().str.lower()
for col in ["source", "destination", "train_type", "class", "train_name"]:
    df[col] = df[col].astype(str).str.strip()

MODEL_PATH = r"C:\\Users\\Aditya Dwivedi\\OneDrive\\Desktop\\IRCTC PROJECT\\smart-train-selector\\train_confirmation_bundle.pkl"
model_bundle = joblib.load(MODEL_PATH)

model = model_bundle["model"]
train_type_le = model_bundle["train_type_le"]
class_mapping = model_bundle["class_mapping"]

# ---------------------------------------------------------
# JOURNEY DETAILS – GLASS CARD WITH ICON FIELDS
# ---------------------------------------------------------
st.markdown('<div class="journey-shell">', unsafe_allow_html=True)
st.markdown('<div class="journey-title">Journey Details</div>', unsafe_allow_html=True)
st.markdown('<div class="journey-subtitle">Describe your trip and I’ll compare trains by safety and confirmation probability.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    user_class = st.selectbox("🎟️ Class", sorted(df["class"].unique()))

with col2:
    source = st.selectbox("📍 Source Station", sorted(df["source"].unique()))

with col3:
    destination = st.selectbox("🚉 Destination Station", sorted(df["destination"].unique()))

journey_date = st.date_input("📅 Journey Date", datetime.today())

st.markdown('<div class="predict-btn-wrapper">', unsafe_allow_html=True)
predict_btn = st.button("✨ Predict Best Trains")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PREDICTION LOGIC
# ---------------------------------------------------------
def get_top_trains(df_route, user_class_value):
    user_class_encoded = class_mapping[user_class_value]

    df_local = df_route.copy()
    df_local["long_route"] = (df_local["duration_hours"] > 24).astype(int)
    df_local["wl_ratio"] = df_local.apply(
        lambda row: row["wl_position"] / {"SL": 100, "3A": 72, "2A": 48}.get(row["class"], 100),
        axis=1
    )
    df_local["delay_risk"] = (df_local["avg_delay_min"] > 30).astype(int)
    df_local["booking_urgency"] = pd.cut(
        df_local["days_before_journey"],
        bins=[-1, 3, 15, 365],
        labels=[0, 1, 2]
    ).astype(int)
    df_local["congestion_per_halt"] = df_local["route_congestion"] / df_local["halts"]
    df_local["train_type_enc"] = train_type_le.transform(df_local["train_type"])
    df_local["class_enc"] = df_local["class"].map(class_mapping)

    features = [
        "train_type_enc", "class_enc", "halts", "duration_hours",
        "train_frequency", "days_before_journey", "weekday", "is_weekend",
        "festival_flag", "route_congestion", "wl_position", "avg_delay_min",
        "delay_risk", "long_route", "wl_ratio", "booking_urgency",
        "congestion_per_halt"
    ]

    X = df_local[features]
    df_local["pred_prob"] = model.predict_proba(X)[:, 1]

    filtered = df_local[df_local["class_enc"] == user_class_encoded]
    filtered = filtered.sort_values(by="pred_prob", ascending=False)
    filtered = filtered.drop_duplicates(subset=["train_no", "train_name"], keep="first")

    return filtered.sort_values(by="pred_prob", ascending=False)

# ---------------------------------------------------------
# GAUGE CHART – SUBTLE, PREMIUM COLORS
# ---------------------------------------------------------
def probability_gauge(prob, key):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        number={'suffix': '%', 'font': {'color': '#e5e7eb'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#64748b'},
            'bgcolor': '#020617',
            'bordercolor': '#020617',
            'bar': {'color': "#38bdf8"},
            'steps': [
                {'range': [0, 45], 'color': '#111827'},
                {'range': [45, 75], 'color': '#1f2937'},
                {'range': [75, 100], 'color': '#1d4ed8'}
            ],
        },
        title={'text': "Confirmation Chance", 'font': {'color': '#9ca3af', 'size': 12}}
    ))
    fig.update_layout(
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig, use_container_width=True, key=key)

# ---------------------------------------------------------
# FILTER ROUTE
# ---------------------------------------------------------
route_df = df[
    (df["source"].str.lower() == source.lower()) &
    (df["destination"].str.lower() == destination.lower())
]

# ---------------------------------------------------------
# DISPLAY RESULTS – INSIDE PREMIUM WRAPPER
# ---------------------------------------------------------
st.markdown('<div class="results-shell">', unsafe_allow_html=True)

if predict_btn:
    if route_df.empty:
        st.warning("No trains found for this route.")
    else:
        top_trains = get_top_trains(route_df, user_class)

        if top_trains.empty:
            st.warning("No trains found for this class.")
        else:
            st.markdown("#### 🚆 Recommended trains for your journey")

            for idx, row in top_trains.iterrows():
                is_best = idx == top_trains.index[0]
                probability_value = row.pred_prob * 100

                st.markdown(
                    f"""
                    <div class="train-card">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px;">
                            <div style="flex:1;">
                                <div class="train-title">{row.train_name} ({row.train_no})</div>
                                <div style="font-size:12px; color:#9ca3af; margin-top:2px;">
                                    From <b>{row.source}</b> to <b>{row.destination}</b> · Class <b>{row['class']}</b>
                                </div>
                                <div style="font-size:11px; color:#6b7280; margin-top:4px;">
                                    Halts: {row.halts} · Avg delay: {int(row.avg_delay_min)} min · WL position: {int(row.wl_position)}
                                </div>
                                {f'<span class="best-badge">BEST MATCH</span>' if is_best else ''}
                            </div>
                            <div style="width:130px; text-align:center;">
                                <div class="progress-ring" style="--p:{probability_value:.0f}">
                                    <div class="progress-ring-inner">
                                        <div class="progress-ring-inner-main">{probability_value:.0f}%</div>
                                        <div class="progress-ring-inner-label">Chance</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                probability_gauge(row.pred_prob, key=f"gauge_{row.train_no}_{idx}")

                if row.pred_prob >= 0.75:
                    st.success("High confirmation chance – strongly recommended.")
                elif row.pred_prob >= 0.45:
                    st.warning("Moderate confirmation chance – consider as a backup option.")
                else:
                    st.info("Low confirmation chance – book only if flexible with plans.")

                st.divider()

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown('<div class="footer">Smart Train Selector · AI-powered decision assistant for Indian Railways journeys</div>', unsafe_allow_html=True)

