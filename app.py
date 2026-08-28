import streamlit as st
import math

# Configure mobile-friendly page layout
st.set_page_config(page_title="Pepper Trades Community Hub", layout="centered")
st.title("🌶️ Pepper Trades Community Hub")
st.markdown("Tools for safe lacto-fermentation, acidification, and genetic tracking.")

# Create clean mobile navigation tabs (Added Seed Genetics tab)
tab1, tab2, tab3 = st.tabs(["Brine & Salt Calculator", "Acidification Engine", "Seed & Genetics Catalog"])

with tab1:
    st.markdown("**Lacto-Fermentation Brine Calculator**")
    st.write("Calculate the exact salt weight needed for your pepper mash or submersed ferments.")
    
    ferment_type = st.radio("Ferment Style:", ["Mash (No Added Water)", "Submersion (Added Water)"])
    produce_weight = st.number_input("Produce Weight (grams)", min_value=0, value=1000)
    
    water_weight = 0
    if ferment_type == "Submersion (Added Water)":
        water_weight = st.number_input("Water Weight (grams)", min_value=0, value=500)
        
    target_salt = st.slider("Target Salt Percentage (%)", min_value=1.5, max_value=5.0, value=3.0, step=0.1)
    
    if st.button("Calculate Salt"):
        total_weight = produce_weight + water_weight
        salt_needed = total_weight * (target_salt / 100)
        st.success(f"**Required Salt: {salt_needed:.1f} grams**")
        st.info(f"Total Batch Weight: {total_weight}g")

with tab2:
    st.markdown("**Acidification Math Engine**")
    st.write("Project the required acid volume to reach safe shelf-stability (target pH < 4.6).")
    
    current_ph = st.number_input("Current Mash pH", min_value=0.0, max_value=14.0, value=5.2, step=0.1)
    target_ph = st.number_input("Target pH (Safety Threshold)", min_value=2.0, max_value=4.5, value=3.8, step=0.1)
    mash_volume = st.number_input("Total Mash Volume (ml)", min_value=0, value=1000)
    
    acid_type = st.selectbox("Acid Source", ["Standard White Vinegar (5% Acetic)", "Apple Cider Vinegar (5% Acetic)"])
    buffer_coefficient = st.slider("Mash Density Buffer", min_value=1.0, max_value=20.0, value=10.0, help="Denser vegetable matter requires a higher multiplier to overcome natural buffering capacity.")
    
    if st.button("Calculate Acid Drop"):
        if target_ph >= current_ph:
            st.warning("Target pH must be lower than current pH.")
        else:
            h_current = 10 ** (-current_ph)
            h_target = 10 ** (-target_ph)
            h_diff = h_target - h_current
            acid_molarity_factor = 0.83 
            base_ml_required = (h_diff / acid_molarity_factor) * mash_volume * 1000
            final_dose = base_ml_required * buffer_coefficient
            st.success(f"**Add approximately {final_dose:.1f} ml of {acid_type}**")
            st.caption("Always verify final batch with a calibrated pH meter before bottling.")

with tab3:
    st.markdown("**Seed Lineage & Genetics Catalog**")
    st.write("Browse rare cultivars, generation stability, and isolation techniques shared by members.")
    
    # Mock data structure (this will pull from your Supabase database later)
    sample_catalog = [
        {"Strain": "Reaper x Primo", "Species": "C. chinense", "Generation": "F4", "Isolation": "Bagged Blossom", "Heat": "Superhot"},
        {"Strain": "Ghost Pepper (Smooth)", "Species": "C. chinense", "Generation": "Open Pollinated", "Isolation": "Isolated Box", "Heat": "Superhot"},
        {"Strain": "Aji Lemon Drop", "Species": "C. baccatum", "Generation": "Stable", "Isolation": "Open", "Heat": "Medium"}
    ]
    
    heat_filter = st.selectbox("Filter by Heat Level", ["All", "Superhot", "Medium"])
    
    for item in sample_catalog:
        if heat_filter == "All" or item["Heat"] == heat_filter:
            with st.expander(f"{item['Strain']} ({item['Generation']})"):
                st.write(f"**Species:** {item['Species']}")
                st.write(f"**Isolation Method:** {item['Isolation']}")
                st.write(f"**Heat Profile:** {item['Heat']}")
