import streamlit as st
import google.generativeai as genai

# === Gemini API Config ===
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# === UI Setup ===
st.set_page_config(page_title="Exoplanet Data Explorer")
st.title("🪐 Exoplanet Data Explorer")
st.write("Explore possible types, characteristics, and habitability of exoplanets based on input parameters.")

# === Input Sliders ===
planet_mass = st.slider("Mass (relative to Earth)", 0.1, 300.0, 1.0)
planet_radius = st.slider("Radius (relative to Earth)", 0.1, 30.0, 1.0)
orbital_period = st.slider("Orbital Period (Earth days)", 0.1, 1000.0, 365.0)
star_temp = st.slider("Host Star Temperature (K)", 2000, 10000, 5778)
distance_star = st.slider("Distance from Star (AU)", 0.01, 10.0, 1.0)
atmosphere = st.selectbox("Atmosphere Present?", ["Yes", "No", "Unknown"])

# === Analyze Button ===
if st.button("Analyze Exoplanet"):
    with st.spinner("Analyzing planetary data..."):
        prompt = f"""
You are an astrophysics model trained on exoplanet data from missions like Kepler and TESS.

Based on the input, estimate:
- Classification: Gas Giant, Ice Giant, Super-Earth, Terrestrial, Mini-Neptune, etc.
- Habitability Likelihood: Likely, Possible, Unlikely
- Confidence Score: % (60–95%)
- Reason: 1 scientific sentence

Inputs:
- Mass: {planet_mass} Earth masses
- Radius: {planet_radius} Earth radii
- Orbital Period: {orbital_period} days
- Host Star Temp: {star_temp} K
- Distance from Star: {distance_star} AU
- Atmosphere: {atmosphere}

Respond in this format:
Classification: <...>  
Habitability: <...>  
Confidence: <...>%  
Reason: <...>
"""

        response = model.generate_content(prompt)
        result = response.text.strip()
        st.subheader("🌌 Planetary Summary")
        st.text(result)
