import streamlit as st
import sqlite3
import random
from datetime import datetime, date

# --- 1. PREMIUM UI CONFIG ---
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
        .surprise-box { background-color: #36454F; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 30px; border: 2px solid #f59e0b; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. ERROR-PROOF DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # FORCE RESET: If columns don't match, we drop and rebuild
    try:
        cursor.execute("SELECT name, ingredients, cuisine, img FROM recipes LIMIT 1")
    except:
        cursor.execute("DROP TABLE IF EXISTS recipes")
        cursor.execute("DROP TABLE IF EXISTS pantry")

    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (name TEXT, ingredients TEXT, cuisine TEXT, img TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, expiry DATE, qty TEXT)''')
    
    cursor.execute("SELECT count(*) FROM recipes")
    if cursor.fetchone()[0] < 20:
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
            ('Khichadi', 'rice,dal,ghee,turmeric', 'Healthy', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
            ('Aloo Paratha', 'flour,potato,butter,curd', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Misal Pav', 'sprouts,pav,onion,tomato,farsan', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84')
        ]
        # Auto-fill to 55+ recipes
        while len(r_list) < 55:
            r_list.append((f"Recipe {len(r_list)+1}", "salt,water", "Global", "https://images.unsplash.com/photo-1547592166-23ac45744acd"))
        cursor.executemany("INSERT INTO recipes VALUES (?,?,?,?)", r_list)
        conn.commit()
    return conn

db_conn = init_db()

# --- 3. NAVIGATION ---
st.sidebar.title("🍳 NEWBIE'S KITCHEN")
st.sidebar.write("Welcome back, **Boss**")
page = st.sidebar.radio("NAVIGATE", ["📊 DASHBOARD", "🎯 PRECISION MATCHER", "🛒 GROCERY LIST", "👤 DIET PLANNER"])

# --- DASHBOARD ---
if page == "📊 DASHBOARD":
    st.title("🏡 Dashboard")
    with st.expander("➕ Add New Stock Item"):
        c1, c2, c3 = st.columns(3)
        it = c1.text_input("Item")
        qt = c2.text_input("Qty")
        ex = c3.date_input("Expiry", min_value=date.today())
        if st.button("Save"):
            db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (it.lower().strip(), ex, qt))
            db_conn.commit()
            st.rerun()

    st.subheader("📋 Current Stock")
    items = db_conn.cursor().execute("SELECT rowid, item, expiry, qty FROM pantry ORDER BY expiry ASC").fetchall()
    for s in items:
        days = (datetime.strptime(s[2], '%Y-%m-%d').date() - date.today()).days
        c_a, c_b = st.columns([4, 1])
        c_a.write(f"**{s[1].upper()}** ({s[3]}) | Expires in: {days} days")
        if c_b.button("🗑️", key=f"del_{s[0]}"):
            db_conn.cursor().execute("DELETE FROM pantry WHERE rowid=?", (s[0],))
            db_conn.commit()
            st.rerun()

# --- PRECISION MATCHER + SURPRISE ME ---
elif page == "🎯 PRECISION MATCHER":
    st.title("🎯 Smart Precision Matcher")
    p_data = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in p_data}
    recipes = db_conn.cursor().execute("SELECT name, ingredients, cuisine, img FROM recipes").fetchall()

    # SURPRISE ME FEATURE
    st.markdown('<div class="surprise-box">', unsafe_allow_html=True)
    st.subheader("🎲 Surprise Me!")
    if st.button("Tailor a Random Meal"):
        valid = [r for r in recipes if any(i in r[1].lower() for i in p_set)]
        if valid:
            res = random.choice(valid)
            st.balloons()
            st.success(f"Boss, today you should cook: {res[0]}!")
            st.image(res[3], width=300)
        else: st.warning("No matches found for your current stock.")
    st.markdown('</div>', unsafe_allow_html=True)

    if not p_set: st.warning("Pantry is empty!")
    else:
        for r in recipes:
            ing_list = [i.strip().lower() for i in r[1].split(',') if i.strip()]
            have = [i for i in ing_list if i in p_set]
            missing = [i for i in ing_list if i not in p_set]
            if ing_list:
                pct = int((len(have)/len(ing_list))*100)
                if pct > 0:
                    with st.container():
                        st.markdown('<div class="match-card">', unsafe_allow_html=True)
                        st.markdown(f"### {r[0]} ({r[2]}) - {pct}% Match")
                        st.progress(pct/100)
                        st.markdown(f'<div class="have-box">✅ HAVE: {", ".join(have)}</div>', unsafe_allow_html=True)
                        if missing: st.markdown(f'<div class="missing-box">❌ MISSING: {", ".join(missing)}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

# --- AUTOMATIC GROCERY LIST ---
elif page == "🛒 GROCERY LIST":
    st.title("🛒 Automatic Grocery List")
    st.write("These items are missing from your kitchen for potential recipes:")
    p_data = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in p_data}
    recipes = db_conn.cursor().execute("SELECT ingredients FROM recipes").fetchall()
    
    all_missing = set()
    for r in recipes:
        ing_list = [i.strip().lower() for i in r[0].split(',') if i.strip()]
        for i in ing_list:
            if i not in p_set: all_missing.add(i)
    
    for m in sorted(list(all_missing))[:20]: # Show top 20 missing
        st.checkbox(f"Buy {m.title()}", key=f"buy_{m}")

# --- DIET PLANNER ---
elif page == "👤 DIET PLANNER":
    st.title("👤 Body Profile")
    w = st.number_input("Weight (kg)", 30, 200, 70)
    h = st.number_input("Height (cm)", 100, 250, 175)
    bmi = round(w / ((h/100)**2), 1)
    st.success(f"BMI: {bmi} | Daily Calories: {int((10*w)+(6.25*h)-120)} kcal")
    
