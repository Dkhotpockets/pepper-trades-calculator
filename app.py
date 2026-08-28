import streamlit as st
import math

# Configure mobile-friendly page layout
st.set_page_config(page_title="Pepper Trades Calculators", layout="centered")
st.title("🌶️ Pepper Trades Calculators")
st.markdown("Community tools for safe lacto-fermentation and acidification.")

# Create clean mobile navigation tabs
tab1, tab2 = st.tabs(["Brine & Salt Calculator", "Acidification Engine"])

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
            # Logarithmic H+ concentration shift
            h_current = 10 ** (-current_ph)
            h_target = 10 ** (-target_ph)
            h_diff = h_target - h_current
            
            # 5% Acetic acid baseline concentration shift estimation
            acid_molarity_factor = 0.83 
            base_ml_required = (h_diff / acid_molarity_factor) * mash_volume * 1000
            
            # Apply organic buffer coefficient
            final_dose = base_ml_required * buffer_coefficient
            
            st.success(f"**Add approximately {final_dose:.1f} ml of {acid_type}**")
            st.caption("Always verify final batch with a calibrated pH meter before bottling.")
