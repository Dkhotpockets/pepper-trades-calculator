import streamlit as st
import math
import random
import string
from supabase import create_client

# Initialize Supabase connection using Streamlit secrets
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = init_connection()

# Configure mobile-friendly page layout
st.set_page_config(page_title="Pepper Trades Community Hub", layout="centered")
st.title("🌶️ Pepper Trades Community Hub")
st.markdown("Ecosystem hub for hot sauce crafting, safety standards, genetics, and trade logistics.")

# Navigation Tabs for All Tools
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Brine Calculator", 
    "Acid Engine", 
    "Seed Catalog", 
    "Recipe Archiver", 
    "Shipping Estimator"
])

# --- TAB 1: BRINE CALCULATOR ---
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

# --- TAB 2: ACIDIFICATION ENGINE ---
with tab2:
    st.markdown("**Acidification Math Engine**")
    st.write("Project the required acid volume to reach safe shelf-stability (target pH < 4.6).")
    
    current_ph = st.number_input("Current Mash pH", min_value=0.0, max_value=14.0, value=5.2, step=0.1)
    target_ph = st.number_input("Target pH (Safety Threshold)", min_value=2.0, max_value=4.5, value=3.8, step=0.1)
    mash_volume = st.number_input("Total Mash Volume (ml)", min_value=0, value=1000)
    
    acid_type = st.selectbox("Acid Source", ["Standard White Vinegar (5% Acetic)", "Apple Cider Vinegar (5% Acetic)"])
    buffer_coefficient = st.slider("Mash Density Buffer", min_value=1.0, max_value=20.0, value=10.0, help="Denser vegetable matter requires a higher multiplier.")
    
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

# --- TAB 3: SEED CATALOG ---
with tab3:
    st.markdown("**Seed Lineage & Genetics Catalog**")
    st.write("Browse rare cultivars, generation stability, and isolation techniques shared by members.")
    
    cat_sub1, cat_sub2 = st.tabs(["Browse Catalog", "List New Strain"])
    
    with cat_sub1:
        try:
            response = supabase.table("strains").select("*").execute()
            live_catalog = response.data
        except Exception as e:
            st.error(f"Could not load database records: {e}")
            live_catalog = []

        heat_filter = st.selectbox("Filter by Heat Level", ["All", "Superhot", "Hot", "Mild", "Medium"])
        
        if not live_catalog:
            st.info("No strains logged in the database yet.")
        else:
            for item in live_catalog:
                heat_lvl = item.get("heat_level", "Unknown")
                if heat_filter == "All" or heat_lvl.lower() == heat_filter.lower():
                    with st.expander(f"{item.get('strain_name')} ({item.get('generation')})"):
                        st.write(f"**Species:** {item.get('species')}")
                        st.write(f"**Isolation Method:** {item.get('isolation_type')}")
                        st.write(f"**Heat Profile:** {heat_lvl}")
                        if item.get('description'):
                            st.write(f"**Notes:** {item.get('description')}")
                            
    with cat_sub2:
        st.markdown("### Register a Genetic Line")
        with st.form("strain_form"):
            strain_name = st.text_input("Strain Name / Cross (e.g., Reaper x Primo)")
            species = st.selectbox("Species", ["Capsicum chinense", "Capsicum annuum", "Capsicum baccatum", "Capsicum pubescens", "Wild/Other"])
            generation = st.text_input("Generation / Stability (e.g., F4, Open Pollinated)")
            isolation_type = st.selectbox("Isolation Technique", ["Bagged Blossom", "Isolated Box/Tent", "Open Pollinated", "Hand Pollinated"])
            heat_level = st.selectbox("Heat Profile", ["Superhot", "Hot", "Medium", "Mild"])
            description = st.text_area("Phenotype Notes & Characteristics")
            
            if st.form_submit_button("Submit to Database"):
                if not strain_name or not generation:
                    st.warning("Please fill out required fields.")
                else:
                    try:
                        supabase.table("strains").insert({
                            "strain_name": strain_name,
                            "species": species,
                            "generation": generation,
                            "isolation_type": isolation_type,
                            "heat_level": heat_level,
                            "description": description
                        }).execute()
                        st.success(f"Successfully added '{strain_name}'!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to insert record: {e}")

# --- TAB 4: RECIPE ARCHIVER ---
with tab4:
    st.markdown("**Community Recipe Archiver**")
    st.write("Submit and format hot sauce recipes, ferment durations, and ingredient pairings.")
    
    with st.form("recipe_form"):
        r_title = st.text_input("Recipe Title (e.g., Smoked Ghost Mash)")
        r_heat = st.selectbox("Heat Profile", ["Superhot", "Hot", "Medium", "Mild"], key="r_heat")
        r_duration = st.text_input("Fermentation Duration (e.g., 3 weeks)")
        r_ingredients = st.text_area("Ingredients List")
        r_instructions = st.text_area("Step-by-Step Instructions")
        r_author = st.text_input("Author / Member Name", value="Community Member")
        
        if st.form_submit_button("Archive Recipe"):
            if not r_title or not r_ingredients:
                st.warning("Please provide a title and ingredients.")
            else:
                st.success(f"Recipe '{r_title}' successfully structured and archived!")
                st.markdown(f"### Preview Markdown Output\n```markdown\n# {r_title}\n* **Author:** {r_author}\n* **Heat:** {r_heat}\n* **Duration:** {r_duration}\n\n## Ingredients\n{r_ingredients}\n\n## Instructions\n{r_instructions}\n```")

# --- TAB 5: SHIPPING ESTIMATOR ---
with tab5:
    st.markdown("**Logistics & Shipping Cost Estimator**")
    st.write("Estimate package rates and generate tracking references for trade items.")
    
    s_type = st.selectbox("Item Class", ["seeds", "sauce"])
    s_weight = st.number_input("Package Weight (oz)", min_value=1.0, value=8.0)
    s_zone = st.slider("Shipping Distance Zone", min_value=1, max_value=5, value=2)
    s_carrier = st.selectbox("Carrier", ["USPS", "UPS"])
    
    if st.button("Calculate Shipping & Generate Tracking"):
        base_rate = 4.50 if s_type == "seeds" else 8.50
        weight_surcharge = (s_weight / 16.0) * 3.00
        zone_multiplier = 1.0 + (s_zone * 0.1)
        total_cost = round((base_rate + weight_surcharge) * zone_multiplier, 2)
        
        prefix = "1Z" if s_carrier == "UPS" else "9400"
        tracking_num = prefix + ''.join(random.choices(string.digits, k=16))
        
        st.success(f"**Estimated Shipping Cost: ${total_cost:.2f}**")
        st.info(f"**Generated Tracking Reference:** `{tracking_num}` ({s_carrier})")
