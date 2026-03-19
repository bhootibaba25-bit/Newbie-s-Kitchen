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
        .missing-box { background-color: #ffebe6; padding: 10px; border-radius: 8px; border-left: 5px solid #ff4d4d; margin-top: 10px; }
        .have-box { background-color: #e6ffed; padding: 10px; border-radius: 8px; border-left: 5px solid #28a745; margin-top: 10px; }
        .percentage-text { font-size: 22px; font-weight: bold; color: #36454F; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. THE 50+ UNIQUE RECIPE ENGINE ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (name TEXT, ingredients TEXT, cuisine TEXT, img TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, date DATE)''')
    
    cursor.execute("SELECT count(*) FROM recipes")
    if cursor.fetchone()[0] < 50:
        cursor.execute("DELETE FROM recipes")
        # 50 UNIQUE REAL-WORLD RECIPES
        r_list = [
            ('Sandwich', 'bread,butter,cheese,tomato,cucumber', 'Global', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af'),
            ('Omelette', 'egg,onion,chili,salt', 'Global', 'https://images.unsplash.com/photo-1510629954389-c1e0da47d4ec'),
            ('Brown Rice', 'rice,water,salt', 'Healthy', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Poha', 'poha,onion,peanuts,turmeric,mustard', 'Maharashtrian', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
            ('Maggi', 'maggi,water,onion,chili', 'Instant', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624'),
            ('Pasta', 'pasta,tomato,garlic,cheese', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Dosa', 'batter,potato,oil,onion', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Tea', 'milk,tea,sugar,ginger', 'Beverage', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
            ('Coffee', 'milk,coffee,sugar', 'Beverage', 'https://images.unsplash.com/photo-1541167760496-162955ed8a9f'),
            ('Khichadi', 'rice,dal,ghee,turmeric', 'Healthy', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
            ('Chips', 'potato,oil,salt,masala', 'Snack', 'https://images.unsplash.com/photo-1566478989037-eec170784d0b'),
            ('Lemonade', 'lemon,water,sugar,mint', 'Beverage', 'https://images.unsplash.com/photo-1523472721958-978152f4d69b'),
            ('Vada Pav', 'pav,potato,garlic,gram flour', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Pav Bhaji', 'pav,butter,potato,peas,tomato', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Idli', 'batter,salt,water', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Upma', 'semolina,onion,mustard,curry leaves', 'South Indian', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
            ('French Fries', 'potato,oil,salt', 'Global', 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877'),
            ('Misal Pav', 'sprouts,pav,onion,tomato,farsan', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Garlic Bread', 'bread,butter,garlic,cheese', 'Italian', 'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c'),
            ('Tacos', 'tortilla,beans,cheese,lettuce', 'Mexican', 'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b'),
            ('Aloo Paratha', 'flour,potato,butter,curd', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Burger', 'bun,patty,cheese,onion,lettuce', 'Global', 'https://images.unsplash.com/photo-1550547660-d9450f859349'),
            ('Noodles', 'noodles,carrot,capsicum,soy sauce', 'Asian', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624'),
            ('Pizza', 'dough,cheese,tomato,capsicum', 'Italian', 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3'),
            ('Stir Fry', 'broccoli,carrot,soy sauce,tofu', 'Healthy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
            ('Puran Poli', 'wheat,dal,jaggery,ghee', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Medu Vada', 'batter,dal,oil,curry leaves', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Sprouts Salad', 'sprouts,onion,lemon,salt', 'Healthy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
            ('Masala Tea', 'milk,tea,sugar,ginger,cardamom', 'Beverage', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
            ('Cold Coffee', 'milk,coffee,ice,sugar', 'Beverage', 'https://images.unsplash.com/photo-1541167760496-162955ed8a9f'),
            ('Egg Bhurji', 'egg,onion,tomato,chili', 'Indian', 'https://images.unsplash.com/photo-1510629954389-c1e0da47d4ec'),
            ('Gatte ki Sabji', 'gram flour,curd,spices', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Dal Bati', 'flour,dal,ghee,salt', 'Rajasthani', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Fruit Salad', 'apple,banana,grapes,honey', 'Healthy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
            ('White Sauce Pasta', 'pasta,milk,butter,cheese', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Red Sauce Pasta', 'pasta,tomato,garlic,basil', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Veg Pulao', 'rice,carrot,peas,onion', 'Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Paneer Tikka', 'paneer,curd,onion,capsicum', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Chana Masala', 'chana,onion,tomato,ginger', 'Punjabi', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Bhindi Fry', 'okra,onion,spices,oil', 'Indian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Jeera Rice', 'rice,cumin,ghee,water', 'Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Curd Rice', 'rice,curd,mustard,curry leaves', 'South Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Onion Pakora', 'onion,gram flour,oil,chili', 'Snack', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Bread Pakora', 'bread,potato,gram flour,oil', 'Snack', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Potato Wedges', 'potato,oil,herbs,salt', 'Snack', 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877'),
            ('Smoothie', 'milk,banana,honey,oats', 'Healthy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
            ('Veg Sandwich', 'bread,potato,onion,cucumber', 'Snack', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af'),
            ('Cheese Sandwich', 'bread,cheese,butter', 'Snack', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af'),
            ('Lemon Rice', 'rice,lemon,turmeric,peanuts', 'South Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Egg Sandwich', 'bread,egg,butter,mayo', 'Breakfast', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af'),
            ('Corn Salad', 'corn,onion,lemon,salt', 'Healthy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd')
        ]
        cursor.executemany("INSERT INTO recipes VALUES (?,?,?,?)", r_list)
        conn.commit()
    return conn

db_conn = init_db()

# --- 3. NAVIGATION ---
st.sidebar.title("🍳 NEWBIE'S KITCHEN")
page = st.sidebar.radio("COMMAND CENTER", ["📊 DASHBOARD", "🎯 PERCENTAGE MATCHER", "👤 DIET PLANNER"])

# --- PAGE: DASHBOARD ---
if page == "📊 DASHBOARD":
    st.title("🏡 Kitchen Dashboard")
    it = st.text_input("➕ Add Item to Stock")
    if st.button("Save Item"):
        db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?)", (it.lower().strip(), date.today()))
        db_conn.commit()
        st.rerun()
    
    st.markdown("---")
    st.subheader("📦 My Current Grocery Stock")
    stock = db_conn.cursor().execute("SELECT rowid, item FROM pantry ORDER BY rowid DESC").fetchall()
    for s in stock:
        c1, c2 = st.columns([5, 1])
        c1.write(f"• **{s[1].upper()}**")
        if c2.button("🗑️", key=f"del_{s[0]}"):
            db_conn.cursor().execute("DELETE FROM pantry WHERE rowid=?", (s[0],))
            db_conn.commit()
            st.rerun()

# --- PAGE: PERCENTAGE MATCHER ---
elif page == "🎯 PERCENTAGE MATCHER":
    st.title("🎯 Smart Percentage Matcher")
    pantry_rows = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in pantry_rows}
    
    if not p_set:
        st.warning("Your pantry is empty, Boss! Add items on the Dashboard.")
    else:
        st.write(f"Analyzing stock: **{', '.join(p_set).upper()}**")
        all_r = db_conn.cursor().execute("SELECT * FROM recipes").fetchall()
        
        for r in all_r:
            name, ing_str, cuis, img = r
            ing_list = [i.strip().lower() for i in ing_str.split(',')]
            have = [i for i in ing_list if i in p_set]
            missing = [i for i in ing_list if i not in p_set]
            pct = int((len(have) / len(ing_list)) * 100)
            
            if pct > 0:
                st.markdown(f'<div class="match-card">', unsafe_allow_html=True)
                col_i, col_t = st.columns([1, 2])
                with col_i: st.image(img, use_container_width=True)
                with col_t:
                    st.markdown(f"### {name} ({cuis})")
                    st.markdown(f'<span class="percentage-text">{pct}% Match</span>', unsafe_allow_html=True)
                    st.progress(pct / 100)
                    st.markdown(f'<div class="have-box">✅ **Have:** {", ".join(have)}</div>', unsafe_allow_html=True)
                    if missing:
                        st.markdown(f'<div class="missing-box">❌ **Missing:** {", ".join(missing)}</div>', unsafe_allow_html=True)
                    else:
                        st.success("Perfect Match! You have everything Boss!")
                st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: DIET PLANNER ---
elif page == "👤 DIET PLANNER":
    st.title("👤 Diet Planner")
    w = st.number_input("Your Weight (kg)", 40, 150, 70)
    st.info(f"Target: {w * 30} Calories & {int(w * 1.5)}g Protein Daily.")
    
