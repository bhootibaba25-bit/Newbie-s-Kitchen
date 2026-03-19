import streamlit as st
import sqlite3
import random
from datetime import datetime, date

# --- 1. UI THEME ---
st.set_page_config(page_title="Newbie's Kitchen", layout="wide", page_icon="🍳")

def apply_custom_ui():
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #36454F; border-right: 3px solid #000000; }
        [data-testid="stSidebar"] * { color: #FFFFFF !important; }
        .match-card { background-color: #E8EAE6; border: 2px solid #36454F; border-radius: 12px; padding: 20px; margin-bottom: 25px; }
        .missing-box { background-color: #ffebe6; padding: 10px; border-radius: 8px; border-left: 5px solid #ff4d4d; margin-top: 10px; color: #b91c1c; font-weight: bold; }
        .have-box { background-color: #e6ffed; padding: 10px; border-radius: 8px; border-left: 5px solid #28a745; margin-top: 10px; color: #166534; font-weight: bold; }
        .percentage-text { font-size: 24px; font-weight: bold; color: #36454F; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    # Create Tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (name TEXT, ingredients TEXT, cuisine TEXT, img TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, expiry DATE, qty TEXT)''')
    
    # Check Recipe Count
    cursor.execute("SELECT count(*) FROM recipes")
    if cursor.fetchone()[0] < 50:
        cursor.execute("DELETE FROM recipes")
        r_list = [
            ('Sandwich', 'bread,butter,cheese,tomato,cucumber', 'Global', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af'),
            ('Omelette', 'egg,onion,chili,salt', 'Global', 'https://images.unsplash.com/photo-1510629954389-c1e0da47d4ec'),
            ('Poha', 'poha,onion,peanuts,turmeric,mustard', 'Maharashtrian', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
            ('Maggi', 'maggi,water,onion,chili', 'Instant', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624'),
            ('Pasta', 'pasta,tomato,garlic,cheese', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Dosa', 'batter,potato,oil,onion', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Pav Bhaji', 'pav,butter,potato,peas,tomato', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Tea', 'milk,tea,sugar,ginger', 'Beverage', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
            ('Coffee', 'milk,coffee,sugar', 'Beverage', 'https://images.unsplash.com/photo-1541167760496-162955ed8a9f'),
            ('Khichadi', 'rice,dal,ghee,turmeric', 'Healthy', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
            ('Misal Pav', 'sprouts,pav,onion,tomato,farsan', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Vada Pav', 'pav,potato,garlic,gram flour', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Aloo Paratha', 'flour,potato,butter,curd', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Brown Rice', 'rice,water,salt', 'Healthy', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Lemonade', 'lemon,water,sugar,mint', 'Beverage', 'https://images.unsplash.com/photo-1523472721958-978152f4d69b'),
            ('Egg Bhurji', 'egg,onion,tomato,chili', 'Indian', 'https://images.unsplash.com/photo-1510629954389-c1e0da47d4ec'),
            ('Fruit Salad', 'apple,banana,grapes,honey', 'Healthy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd')
        ]
        # Fill to 55 recipes
        while len(r_list) < 55:
            r_list.append((f"Recipe {len(r_list)+1}", "salt,water", "Global", "https://images.unsplash.com/photo-1547592166-23ac45744acd"))
        cursor.executemany("INSERT INTO recipes VALUES (?,?,?,?)", r_list)
        conn.commit()
    return conn

db_conn = init_db()

# --- 3. NAVIGATION ---
st.sidebar.title("🍳 NEWBIE'S KITCHEN")
st.sidebar.write("Logged in: **Boss**")
page = st.sidebar.radio("NAVIGATE", ["📊 DASHBOARD", "🎯 PRECISION MATCHER", "👤 DIET PLANNER"])

# --- DASHBOARD (WITH EXPIRY & INDIVIDUAL DELETE) ---
if page == "📊 DASHBOARD":
    st.title("🏡 Smart Kitchen Dashboard")
    with st.expander("➕ Add New Item to Stock"):
        c1, c2, c3 = st.columns(3)
        it = c1.text_input("Item Name")
        qt = c2.text_input("Qty (e.g. 2kg)")
        ex = c3.date_input("Expiry Date", min_value=date.today())
        if st.button("Add to Pantry"):
            if it:
                db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (it.lower().strip(), ex, qt))
                db_conn.commit()
                st.rerun()

    st.markdown("---")
    st.subheader("📋 Current Stock & Expiry Alerts")
    items = db_conn.cursor().execute("SELECT rowid, item, expiry, qty FROM pantry ORDER BY expiry ASC").fetchall()
    
    if not items:
        st.info("Pantry is empty, Boss!")
    else:
        for s in items:
            days = (datetime.strptime(s[2], '%Y-%m-%d').date() - date.today()).days
            color = "🔴" if days < 3 else "🟢"
            c_a, c_b, c_c = st.columns([3, 2, 1])
            c_a.write(f"{color} **{s[1].upper()}** ({s[3]})")
            c_b.write(f"Expires in: **{days} days**")
            if c_c.button("🗑️", key=f"del_{s[0]}"):
                db_conn.cursor().execute("DELETE FROM pantry WHERE rowid=?", (s[0],))
                db_conn.commit()
                st.rerun()

# --- PRECISION MATCHER (RESTORED % LOGIC) ---
elif page == "🎯 PRECISION MATCHER":
    st.title("🎯 Smart Precision Matcher")
    p_data = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in p_data}
    
    if not p_set:
        st.warning("Pantry is empty! Add items on the Dashboard.")
    else:
        st.write(f"Your Stock: **{', '.join(p_set).upper()}**")
        recipes = db_conn.cursor().execute("SELECT name, ingredients, cuisine, img FROM recipes").fetchall()
        
        for r in recipes:
            r_name, r_ing, r_cuis, r_img = r # Fixed Unpacking
            ing_list = [i.strip().lower() for i in r_ing.split(',') if i.strip()]
            have = [i for i in ing_list if i in p_set]
            missing = [i for i in ing_list if i not in p_set]
            
            if ing_list:
                pct = int((len(have) / len(ing_list)) * 100)
                if pct > 0:
                    st.markdown(f'<div class="match-card">', unsafe_allow_html=True)
                    col_i, col_t = st.columns([1, 2])
                    col_i.image(r_img, use_container_width=True)
                    with col_t:
                        st.markdown(f"### {r_name} ({r_cuis})")
                        st.markdown(f'<span class="percentage-text">{pct}% Match</span>', unsafe_allow_html=True)
                        st.progress(pct/100)
                        st.markdown(f'<div class="have-box">✅ HAVE: {", ".join(have)}</div>', unsafe_allow_html=True)
                        if missing:
                            st.markdown(f'<div class="missing-box">❌ MISSING: {", ".join(missing)}</div>', unsafe_allow_html=True)
                        else:
                            st.success("You have everything, Boss!")
                    st.markdown('</div>', unsafe_allow_html=True)

# --- DIET PLANNER (WEIGHT & HEIGHT) ---
elif page == "👤 DIET PLANNER":
    st.title("👤 Body & Nutrition Profile")
    st.markdown('<div class="match-card">', unsafe_allow_html=True)
    c_w, c_h = st.columns(2)
    w = c_w.number_input("Weight (kg)", 30, 200, 70)
    h = c_h.number_input("Height (cm)", 100, 250, 175)
    
    bmi = round(w / ((h/100)**2), 1)
    st.markdown(f"### Your BMI: **{bmi}**")
    
    cal = (10 * w) + (6.25 * h) - (5 * 25) + 5
    st.info(f"Target Intake: **{int(cal)} Calories/Day**")
    st.success(f"Target Protein: **{int(w * 1.6)}g/Day**")
    st.markdown('</div>', unsafe_allow_html=True)
    
