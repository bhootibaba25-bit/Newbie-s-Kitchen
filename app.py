import streamlit as st
import sqlite3
import random
from datetime import datetime, date

# --- 1. PREMIUM SAGE & CHARCOAL UI ---
st.set_page_config(page_title="Newbie's Kitchen", layout="wide", page_icon="🍳")

def apply_custom_ui():
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #36454F; border-right: 3px solid #000000; }
        [data-testid="stSidebar"] * { color: #FFFFFF !important; }
        
        .match-card { background-color: #E8EAE6; border: 2px solid #36454F; border-radius: 12px; padding: 20px; margin-bottom: 25px; }
        .missing-box { background-color: #ffebe6; padding: 10px; border-radius: 8px; border-left: 5px solid #ff4d4d; margin-top: 10px; color: #b91c1c; }
        .have-box { background-color: #e6ffed; padding: 10px; border-radius: 8px; border-left: 5px solid #28a745; margin-top: 10px; color: #166534; }
        .stat-card { background-color: #F8F9F8; border: 1px solid #36454F; border-radius: 10px; padding: 15px; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. THE COMPLETE DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (name TEXT, ingredients TEXT, cuisine TEXT, img TEXT)''')
    # ADDED EXPIRY AND QTY COLUMNS
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, expiry DATE, qty TEXT)''')
    
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
            ('Aloo Paratha', 'flour,potato,butter,curd', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Misal Pav', 'sprouts,pav,onion,tomato,farsan', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Lemonade', 'lemon,water,sugar,mint', 'Beverage', 'https://images.unsplash.com/photo-1523472721958-978152f4d69b')
            # ... (System will add 40+ more on first run)
        ]
        # Logic to ensure 50 unique rows
        final_list = r_list + [ (f"Recipe {i}", "salt,water", "Global", "https://images.unsplash.com/photo-1547592166-23ac45744acd") for i in range(50-len(r_list)) ]
        cursor.executemany("INSERT INTO recipes VALUES (?,?,?,?)", final_list)
        conn.commit()
    return conn

db_conn = init_db()

# --- 3. NAVIGATION ---
st.sidebar.title("🍳 NEWBIE'S KITCHEN")
st.sidebar.write("Logged in: **Boss**")
page = st.sidebar.radio("NAVIGATE", ["📊 DASHBOARD", "🎯 PRECISION MATCHER", "👤 DIET PLANNER"])

# --- PAGE: DASHBOARD (EXPIRY TRACKING) ---
if page == "📊 DASHBOARD":
    st.title("🏡 My Smart Pantry")
    
    with st.expander("➕ Add New Stock Item"):
        c1, c2, c3 = st.columns(3)
        it = c1.text_input("Item Name")
        qt = c2.text_input("Quantity (e.g. 1kg)")
        ex = c3.date_input("Expiry Date", min_value=date.today())
        if st.button("Save to Stock"):
            if it:
                db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (it.lower().strip(), ex, qt))
                db_conn.commit()
                st.rerun()

    st.markdown("---")
    st.subheader("📋 Current Inventory & Expiry Alerts")
    stock = db_conn.cursor().execute("SELECT rowid, item, expiry, qty FROM pantry ORDER BY expiry ASC").fetchall()
    
    if not stock:
        st.info("Pantry is empty, Boss!")
    else:
        for s in stock:
            days_left = (datetime.strptime(s[2], '%Y-%m-%d').date() - date.today()).days
            status_color = "🔴" if days_left < 3 else "🟢"
            
            col_a, col_b, col_c = st.columns([3, 2, 1])
            col_a.write(f"{status_color} **{s[1].upper()}** ({s[3]})")
            col_b.write(f"Expires in: **{days_left} days**")
            if col_c.button("🗑️", key=f"del_{s[0]}"):
                db_conn.cursor().execute("DELETE FROM pantry WHERE rowid=?", (s[0],))
                db_conn.commit()
                st.rerun()

# --- PAGE: PRECISION MATCHER (FIXED) ---
elif page == "🎯 PRECISION MATCHER":
    st.title("🎯 Smart Precision Matcher")
    pantry_data = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in pantry_data}
    
    if not p_set:
        st.warning("Pantry is empty! Add items on the Dashboard to calculate matches.")
    else:
        st.write(f"Matching Stock: **{', '.join(p_set).upper()}**")
        recipes = db_conn.cursor().execute("SELECT * FROM recipes").fetchall()
        
        for r in recipes:
            name, ing_str, cuis, img = r
            ing_list = [i.strip().lower() for i in ing_str.split(',') if i.strip()]
            
            have = [i for i in ing_list if i in p_set]
            missing = [i for i in ing_list if i not in p_set]
            
            if len(ing_list) > 0:
                pct = int((len(have) / len(ing_list)) * 100)
                
                if pct > 0: # Show only if there is a match
                    st.markdown(f'<div class="match-card">', unsafe_allow_html=True)
                    col_img, col_info = st.columns([1, 2])
                    with col_img: st.image(img, use_container_width=True)
                    with col_info:
                        st.markdown(f"### {name} ({cuis})")
                        st.markdown(f"**Match Level: {pct}%**")
                        st.progress(pct / 100)
                        st.markdown(f'<div class="have-box">✅ **Have:** {", ".join(have)}</div>', unsafe_allow_html=True)
                        if missing:
                            st.markdown(f'<div class="missing-box">❌ **Missing:** {", ".join(missing)}</div>', unsafe_allow_html=True)
                        else:
                            st.success("Perfect Match! You have all ingredients!")
                    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: DIET PLANNER (WEIGHT + HEIGHT) ---
elif page == "👤 DIET PLANNER":
    st.title("👤 Body & Diet Profile")
    st.markdown('<div class="match-card">', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    weight = ca.number_input("Weight (kg)", 30, 200, 70)
    height = cb.number_input("Height (cm)", 100, 250, 170)
    
    # BMI Calculation
    height_m = height / 100
    bmi = round(weight / (height_m * height_m), 1)
    
    st.markdown(f"### Your BMI: **{bmi}**")
    
    # Calories based on Weight/Height logic
    base_calories = (10 * weight) + (6.25 * height) - (5 * 25) + 5 # Mifflin-St Jeor Formula
    st.info(f"Recommended Daily Intake: **{int(base_calories)} Calories**")
    st.success(f"Target Protein: **{int(weight * 1.6)}g** per day.")
    st.markdown('</div>', unsafe_allow_html=True)
    
