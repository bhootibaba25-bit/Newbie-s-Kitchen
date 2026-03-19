import streamlit as st
import sqlite3
import random
from datetime import datetime, date
from PIL import Image

# --- 1. PREMIUM UI CONFIG ---
st.set_page_config(page_title="Newbie's Kitchen", layout="wide", page_icon="🍳")

def apply_custom_ui():
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #36454F; border-right: 3px solid #000000; }
        [data-testid="stSidebar"] * { color: #FFFFFF !important; }
        
        /* Recipe Grid Styling */
        .recipe-grid-card {
            background-color: #E8EAE6;
            border: 2px solid #36454F;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            min-height: 250px;
        }
        .main-card {
            background-color: #F8F9F8;
            border: 1px solid #36454F;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .badge {
            background-color: #f59e0b;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 10px;
            font-weight: bold;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. EXPANDED UNIQUE DATABASE ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes 
                      (name TEXT, ingredients TEXT, calories INT, protein INT, carbs INT, 
                       cuisine TEXT, style TEXT, difficulty TEXT, image_url TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, expiry DATE, qty TEXT)''')
    
    # Refresh database to add the new expanded list
    cursor.execute("SELECT count(*) FROM recipes")
    if cursor.fetchone()[0] < 25:
        cursor.execute("DELETE FROM recipes")
        
        # 30+ UNIQUE REAL RECIPES
        expanded_recipes = [
            ('Sandwich', 'bread,butter,cheese,tomato,cucumber', 250, 8, 30, 'Global', 'Snack', 'Easy', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af'),
            ('Omelette', 'egg,onion,chili,salt', 150, 12, 2, 'Global', 'Breakfast', 'Easy', 'https://images.unsplash.com/photo-1510629954389-c1e0da47d4ec'),
            ('Poha', 'flattened rice,peanuts,onion,curry leaves', 250, 6, 40, 'Indian', 'Maharashtrian', 'Easy', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
            ('Maggi', 'noodles,water,maggi masala', 300, 7, 50, 'Asian', 'Instant', 'Easy', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624'),
            ('Pasta', 'pasta,tomato,garlic,basil,cheese', 400, 12, 60, 'Italian', 'Classic', 'Medium', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Dosa', 'batter,potato,oil,chutney', 300, 5, 55, 'Indian', 'South Indian', 'Medium', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Khichadi', 'rice,moong dal,ghee,cumin', 350, 10, 60, 'Indian', 'Healthy', 'Easy', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
            ('Lemonade', 'lemon,water,sugar,mint', 100, 0, 25, 'Global', 'Beverage', 'Easy', 'https://images.unsplash.com/photo-1523472721958-978152f4d69b'),
            ('Puran Poli', 'chana dal,jaggery,wheat flour,ghee', 350, 8, 65, 'Indian', 'Maharashtrian', 'Hard', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Tea', 'milk,tea leaves,sugar,ginger,cardamom', 100, 2, 15, 'Indian', 'Beverage', 'Easy', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
            ('Misal Pav', 'sprouts,onion,tomato,farsan,pav', 450, 15, 50, 'Indian', 'Maharashtrian', 'Medium', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Vada Pav', 'potato,gram flour,bread,garlic chutney', 300, 6, 45, 'Indian', 'Maharashtrian', 'Easy', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Pav Bhaji', 'potato,cauliflower,peas,butter,pav', 500, 10, 70, 'Indian', 'Maharashtrian', 'Medium', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Idli', 'batter,salt,water', 150, 5, 30, 'Indian', 'South Indian', 'Easy', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Upma', 'semolina,onion,mustard seeds,curry leaves', 220, 5, 35, 'Indian', 'Breakfast', 'Easy', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
            ('Medu Vada', 'urad dal,peppercorns,oil', 350, 12, 25, 'Indian', 'South Indian', 'Hard', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Coffee', 'milk,coffee powder,sugar', 120, 3, 18, 'Global', 'Beverage', 'Easy', 'https://images.unsplash.com/photo-1541167760496-162955ed8a9f'),
            ('Chips', 'potato,oil,salt,masala', 500, 2, 60, 'Global', 'Snack', 'Easy', 'https://images.unsplash.com/photo-1566478989037-eec170784d0b'),
            ('Sprouts Salad', 'moong sprouts,onion,lemon,chili', 120, 10, 15, 'Indian', 'Healthy', 'Easy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
            ('French Fries', 'potato,oil,salt', 350, 3, 45, 'Global', 'Snack', 'Easy', 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877'),
            ('Tacos', 'tortilla,beans,cheese,lettuce', 400, 15, 35, 'Mexican', 'Classic', 'Medium', 'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b'),
            ('Fried Rice', 'rice,carrot,beans,soy sauce', 350, 7, 60, 'Asian', 'Classic', 'Medium', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Veg Burger', 'bun,potato patty,lettuce,mayo', 450, 10, 50, 'Global', 'Snack', 'Medium', 'https://images.unsplash.com/photo-1550547660-d9450f859349'),
            ('Pancakes', 'flour,milk,egg,syrup', 350, 8, 55, 'Global', 'Breakfast', 'Easy', 'https://images.unsplash.com/photo-1567620905732-2d1ec7bb7445'),
            ('Fruit Salad', 'apple,banana,grapes,honey', 150, 1, 35, 'Global', 'Healthy', 'Easy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
            ('Garlic Bread', 'bread,butter,garlic,herbs', 280, 5, 35, 'Italian', 'Snack', 'Easy', 'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c'),
            ('Gatte ki Sabji', 'gram flour,curd,spices', 320, 12, 18, 'Indian', 'Rajasthani', 'Hard', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Aloo Paratha', 'wheat flour,potato,butter', 380, 7, 50, 'Indian', 'Punjabi', 'Medium', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Veg Stir Fry', 'broccoli,bell peppers,soy sauce', 180, 5, 20, 'Asian', 'Healthy', 'Easy', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd')
        ]
        cursor.executemany("INSERT INTO recipes VALUES (?,?,?,?,?,?,?,?,?)", expanded_recipes)
        conn.commit()
    return conn

db_conn = init_db()

# --- 3. NAVIGATION ---
st.sidebar.title("🍳 NEWBIE'S KITCHEN")
st.sidebar.write("Logged in as: **Boss**")
page = st.sidebar.radio("COMMAND CENTER", ["📊 DASHBOARD", "🔍 SMART MATCHER", "👤 DIET PLANNER"])

# --- DASHBOARD: INDIVIDUAL DELETE ---
if page == "📊 DASHBOARD":
    st.title("🏡 Kitchen Command Center")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="main-card"><h3>➕ Add Stock</h3>', unsafe_allow_html=True)
        it = st.text_input("Item Name (e.g. Bread, Potato)")
        ex = st.date_input("Expiry Date", min_value=date.today())
        if st.button("Save to Pantry"):
            if it:
                db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (it.lower(), ex, "1 unit"))
                db_conn.commit()
                st.success(f"{it} Added!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="main-card"><h3>📋 Stock Inventory</h3>', unsafe_allow_html=True)
        stock = db_conn.cursor().execute("SELECT rowid, * FROM pantry ORDER BY expiry ASC").fetchall()
        if not stock:
            st.info("Pantry is empty.")
        for s in stock:
            c_info, c_del = st.columns([4, 1])
            c_info.write(f"**{s[1].upper()}** (Exp: {s[2]})")
            if c_del.button("🗑️", key=f"del_{s[0]}"):
                db_conn.cursor().execute("DELETE FROM pantry WHERE rowid=?", (s[0],))
                db_conn.commit()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- SMART MATCHER: GRID OUTPUT ---
elif page == "🔍 SMART MATCHER":
    st.title("🔍 Smart Recipe Matcher")
    
    pantry = [row[0] for row in db_conn.cursor().execute("SELECT item FROM pantry").fetchall()]
    
    if not pantry:
        st.warning("Your pantry is empty, Boss! Add items on the Dashboard to find matches.")
    else:
        st.write(f"Matching for your stock: **{', '.join(pantry).upper()}**")
        
        # TAILOR FEATURE
        if st.button("✨ Random Access Tailor (Surprise Me)"):
            all_r = db_conn.cursor().execute("SELECT * FROM recipes").fetchall()
            matches = [r for r in all_r if any(i in r[1].lower() for i in pantry)]
            if matches:
                res = random.choice(matches)
                st.balloons()
                st.success(f"Boss, how about: {res[0]}?")
                st.image(res[8], width=400)
            else: st.error("No matches found for current stock.")

        st.markdown("---")
        
        # SEARCH AND GRID
        all_r = db_conn.cursor().execute("SELECT * FROM recipes").fetchall()
        matches = [r for r in all_r if any(i in r[1].lower() for i in pantry)]
        
        if matches:
            st.subheader(f"Found {len(matches)} matches for you:")
            cols = st.columns(3)
            for idx, r in enumerate(matches):
                with cols[idx % 3]:
                    st.markdown(f'''
                        <div class="recipe-grid-card">
                            <span class="badge">{r[6]} • {r[5]}</span>
                            <h4 style="margin:5px 0;">{r[0]}</h4>
                            <p style="font-size:12px; color:#555;"><b>Ingredients:</b> {r[1]}</p>
                        </div>
                    ''', unsafe_allow_html=True)
                    st.image(r[8], use_container_width=True)
        else:
            st.info("No recipes found with these ingredients. Try adding 'potato', 'bread', or 'egg'!")

# --- DIET PLANNER ---
elif page == "👤 DIET PLANNER":
    st.title("👤 Personalized Diet Planner")
    w = st.number_input("Your Weight (kg)", 40, 150, 70)
    st.markdown(f"""
        <div class="main-card">
            <h3>Nutrition Targets for Boss</h3>
            <p>Daily Calories: <b>{w * 30} kcal</b></p>
            <p>Target Protein: <b>{int(w * 1.5)}g</b></p>
        </div>
    """, unsafe_allow_html=True)
    
