from flask import Flask, render_template, jsonify
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/demand-forecast')
def demand_forecast():
    # Redirect to Flask app or show message
    return "Please use the Flask app for predictions. Predictions are now handled by appPred.py"

if __name__ == '__main__':
    app.run(debug=True)

st.markdown("""
<style>

/* Remove default Streamlit padding */
.block-container {
    padding-top: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}

/* Remove extra space above first element */
.css-18e3th9 {
    padding-top: 0rem;
}

</style>
""", unsafe_allow_html=True)





st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>

/* -------- Global -------- */
section {
    padding: 80px 60px;
}

/* -------- Navbar -------- */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 60px;
    border-bottom: 1px solid #e0e0e0;
    background: #f7f6f3;
}
.nav-links a {
    margin: 0 18px;
    text-decoration: none;
    color: #111;
    font-weight: 500;
}
.contact-btn {
    padding: 8px 18px;
    border: 1px solid #111;
    border-radius: 4px;
    font-weight: 600;
}

/* -------- Hero -------- */
.hero {
    position: relative;
    padding: 140px 60px;
    color: white;
    border-radius: 0;
}
.hero-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.6);
}
.hero-content {
    position: relative;
    z-index: 2;
}
.hero h1 {
    font-size: 56px;
    font-weight: 800;
}
.hero p {
    font-size: 22px;
    margin-top: 10px;
}
.hero button {
    margin-top: 25px;
    padding: 14px 28px;
    background: #1f77b4;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
}

/* -------- About Section -------- */
.about-tag {
    color: #1f77b4;
    font-weight: 700;
    letter-spacing: 1px;
    font-size: 14px;
}
.about-text {
    font-size: 17px;
    line-height: 1.6;
}

/* -------- Feature Cards -------- */
.card {
    background: white;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    overflow: hidden;
    transition: all 0.3s ease;
""", unsafe_allow_html=True)

# --------------------------------------------------
# Hero Section
# --------------------------------------------------
st.markdown(f"""
<div class="hero" style="
    background-image: url('data:image/png;base64,{hero_img}');
    background-size: cover;
    background-position: center;
">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <h1>Predicting power needs</h1>
        <p>Enhancing efficiency for Telangana</p>
        <button>VIEW SERVICES</button>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# About Section
# --------------------------------------------------
st.markdown("<section>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="about-tag">PREDICTIVE ENERGY MANAGEMENT</div>', unsafe_allow_html=True)
    st.header("Empowering Telangana’s power supply")
    st.markdown("""
    <div class="about-text">
    NeuraGrid revolutionizes electricity demand forecasting in Telangana by
    integrating traditional forecasting techniques with advanced deep learning models.
    The system leverages real-time SLDC data, weather patterns, and population trends
    to enhance accuracy, maintain grid stability, and reduce energy wastage.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("[Get in touch](#)")

with col2:
    st.image("assets/about.png", use_container_width=True)

st.markdown("</section>", unsafe_allow_html=True)

# --------------------------------------------------
# Features Section
# --------------------------------------------------
st.markdown('<section class="features">', unsafe_allow_html=True)

st.markdown("#### PREDICTIVE DEMAND ANALYTICS")
st.header("Optimize energy use with precision")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(f"""
    <div class="card">
        <div class="card-img" style="
            background-image: url('data:image/png;base64,{img1}');
        "></div>
        <div class="card-body">
            <h4>Demand prediction model</h4>
            <p>Forecasting of short-term electricity demand.</p>
            <a href="#">Learn more →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown(f"""
    <div class="card">
        <div class="card-img" style="
            background-image: url('data:image/png;base64,{img2}');
        "></div>
        <div class="card-body">
            <h4>Weather impact analysis</h4>
            <p>Visualize how weather affects electricity demand.</p>
            <a href="#">Learn more →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown(f"""
    <div class="card">
        <div class="card-img" style="
            background-image: url('data:image/png;base64,{img3}');
        "></div>
        <div class="card-body">
            <h4>Real-time demand insights</h4>
            <p>Access up-to-date electricity demand statistics.</p>
            <a href="#">Learn more →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
