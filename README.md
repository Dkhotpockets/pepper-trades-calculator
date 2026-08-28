# 🌶️ Pepper Trades Community Hub

A unified web-based toolkit and ecosystem hub designed for hot pepper cultivators, lacto-fermentation hobbyists, and peer-to-peer traders. Built with Python, Streamlit, and a Supabase PostgreSQL backend.

---

## ⚡ Complete Setup & Execution Instructions (Local Development)

Execute these exact terminal commands in your local environment to clone, configure dependencies, set up database keys, and launch the application:

### Step 1: Clone Repository & Navigate Into Directory

```bash
git clone https://github.com/Dkhotpockets/pepper-trades-calculator.git
cd trades-calculator

```

### Step 2: Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate

```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt

```

### Step 4: Create and Configure Local Secrets Directory

Streamlit requires a local TOML file to securely inject database keys during development. Create the hidden directory and configuration file:

```bash
mkdir -p .streamlit
nano .streamlit/secrets.toml

```

Paste your exact Supabase credentials into `secrets.toml`:

```toml
[supabase]
url = "https://snwbzsdikfemqqileswl.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNud2J6c2Rpa2ZlbXFxaWxlc3dsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc4NzEzMTYsImV4cCI6MjEwMzQ0NzMxNn0.X2oxgC6onLNKAbo5msdqRj2lN18tKzuXM-BeB_vLFoY"

```

### Step 5: Launch the Local Web Application

```bash
streamlit run app.py

```

Open the provided Local URL (`http://localhost:8501`) in your web browser.

---

## 🖥️ How to Use the Application (Tool Breakdown)

Once loaded in your browser, the interface organizes all operations into five accessible tabs:

1. **Brine Calculator Tab:**
* Select your ferment style (Mash vs. Submersion).
* Enter your produce and water weights in grams.
* Adjust the salt percentage slider (1.5% to 5.0%) to instantly calculate the exact non-iodized salt required.


2. **Acid Engine Tab:**
* Input your current mash pH and target safety threshold (< 4.6).
* Enter mash volume and select acid source (white or apple cider vinegar) to project required vinegar dosing.


3. **Seed Catalog Tab:**
* **Browse Catalog:** Filter existing database records by heat profile (Superhot, Hot, Mild, Medium) and view strain line details.
* **List New Strain:** Use the built-in form to register new genetic lines, species, isolation techniques, and phenotype notes straight into the Supabase PostgreSQL database.


4. **Recipe Archiver Tab:**
* Fill out recipe titles, heat profiles, fermentation durations, ingredient lists, and instructions.
* Instantly generate formatted Markdown output ready to share with community members.


5. **Shipping Estimator Tab:**
* Select item class (seeds vs. bottled hot sauce) and package weight.
* Choose user-friendly geographic distances (Local to Coast-to-Coast) to calculate total shipping costs and generate carrier tracking references.



---

## 🚀 Pushing Updates to GitHub (Deployment)

When you make changes to the code, you need to sync them to GitHub so they deploy to your live web app. Run these commands in your terminal:

```bash
git add .
git commit -m "Describe your updates here"
git push origin main

```

---

## 🏗️ Technical Architecture & Tech Stack

* **Frontend Framework (`Streamlit`):** Python-based reactive UI rendering mobile-friendly web views natively.
* **Database Persistence (`Supabase / PostgreSQL`):** Secure relational database handling real-time CRUD operations for seed lineages.
* **Secrets Management (`Streamlit Secrets`):** TOML-based key separation (`st.secrets`) protecting API tokens across local and cloud environments.
