# app.py
import sys
from pathlib import Path
import streamlit as st
from fuzzywuzzy import process

# Add the src directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from recommender import run_pipeline
from constants import DATA_PATH, DEFAULT_RECO_N
from data_loader import load_dataset

# Page config
st.set_page_config(page_title="Scent4All Recommender", layout="centered")

# Load dataset just once
@st.cache_data
def load_perfume_names(path: str):
    df = load_dataset(path)
    return df["Perfume"].sort_values().tolist()

st.title("🌸 Scent4All - Perfume Recommender")
st.markdown("Discover perfumes similar to your favorites using notes and accords!")

perfume_list = load_perfume_names(DATA_PATH)

# UI Elements
query = st.text_input("Search for a perfume", placeholder="Type a perfume name...")
matched = process.extractOne(query, perfume_list) if query else None

if matched and matched[1] >= 80:
    st.caption(f"🔎 Did you mean: **{matched[0]}**?")
    selected_perfume = matched[0]
else:
    selected_perfume = None

top_n = st.slider("Number of recommendations", 1, 10, DEFAULT_RECO_N)

if st.button("🔍 Show Recommendations") and selected_perfume:
    with st.spinner("Analyzing scent profiles..."):
        results = run_pipeline(DATA_PATH, selected_perfume, top_n)

    if results.empty:
        st.warning(f"No recommendations found for: {selected_perfume}")
    else:
        st.success(f"🎯 Top {top_n} recommendations for '{selected_perfume}':")
        st.dataframe(results, use_container_width=True)
