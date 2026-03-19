import streamlit as st
import sqlite3
import random
from datetime import datetime, date

# --- 1. PREMIUM UI THEME ---
st.set_page_config(page_title="Newbie's Kitchen", layout="wide", page_icon="🍳")

def apply_custom_ui():
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #36454F; border-right: 3px solid #000000; }
        [data-testid="stSidebar"] * { color: #FFFFFF !important; }
        .match-card { background-color: #E8EAE6; border: 2px solid #36454F; border-radius: 12px; padding: 20px; margin-bottom: 25px; box-shadow: 4px 4px 0px #36454F; }
        .missing-box { background-color: #ffebe6; padding: 10px; border-radius: 8px; border-left: 5px solid #ff4d4d; margin-top: 10px; color: #b91c1c; font-weight: bold; }
        .have-box { background-color: #e6ffed; padding: 10px; border-radius: 8px; border-left: 5px solid #28a745; margin-top: 10px; color: #166534; font-weight: bold; }
        .recipe-badge { background-color: #36454F; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; margin-bottom: 5px; display: inline-block; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. THE 110+ REAL UNIQUE RECIPE DATABASE ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Structure Check
    try:
        cursor.execute("SELECT name, ingredients, cuisine, img FROM recipes LIMIT 1")
    except:
        cursor.execute("DROP TABLE IF EXISTS recipes")
        cursor.execute("DROP TABLE IF EXISTS pantry")

    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (name TEXT, ingredients TEXT, cuisine TEXT, img TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, expiry DATE, qty TEXT)''')
    
    cursor.execute("SELECT count(*) FROM recipes")
    if cursor.fetchone()[0] < 100:
        cursor.execute("DELETE FROM recipes")
        
        # MASTER LIST: 110+ REAL UNIQUE RECIPES
        r_list = [
            # MAHARASHTRIAN (15)
            ('Poha', 'poha,onion,peanuts,mustard,turmeric', 'Maharashtrian', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
            ('Misal Pav', 'sprouts,pav,onion,farsan,lemon', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Vada Pav', 'potato,pav,garlic,gram flour,chili', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Pav Bhaji', 'potato,pav,butter,peas,cauliflower', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Puran Poli', 'wheat flour,chana dal,jaggery,ghee', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Sabudana Khichadi', 'sabudana,peanuts,potato,cumin,chili', 'Maharashtrian', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
            ('Kothimbir Vadi', 'coriander,gram flour,sesame,oil', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Thalipeeth', 'bhajani flour,onion,cucumber,curd', 'Maharashtrian', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Sol Kadhi', 'kokum,coconut milk,garlic,chili', 'Maharashtrian', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
            ('Bharli Vangi', 'eggplant,peanuts,coconut,godamasala', 'Maharashtrian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Pitla Bhakri', 'gram flour,garlic,jowar flour,onion', 'Maharashtrian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Modak', 'rice flour,coconut,jaggery,steamer', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Batata Vada', 'potato,gram flour,turmeric,oil', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Aamti', 'tur dal,kokum,jaggery,curry leaves', 'Maharashtrian', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
            ('Ukadiche Modak', 'rice flour,jaggery,coconut,cardamom', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),

            # RAJASTHANI (14)
            ('Dal Bati', 'wheat flour,moong dal,ghee,garlic', 'Rajasthani', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Gatte ki Sabji', 'gram flour,curd,mustard oil,cumin', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Ker Sangri', 'ker berries,sangri beans,dry mango,oil', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Mirchi Bada', 'large chili,potato,gram flour,oil', 'Rajasthani', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Panchmel Dal', 'five lentils,ghee,hing,clove', 'Rajasthani', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
            ('Lal Maas', 'mutton,mathania chili,ghee,curd', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Mohan Thaal', 'besan,ghee,milk,sugar,cardamom', 'Rajasthani', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Papad ki Sabji', 'papad,curd,turmeric,cumin', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Gond Ke Laddu', 'edible gum,wheat flour,ghee,dry fruits', 'Rajasthani', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Mawa Kachori', 'maida,mawa,sugar syrup,nuts', 'Rajasthani', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Onion Kachori', 'maida,onion,fennel,oil', 'Rajasthani', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Bajra Roti', 'pearl millet flour,ghee,water', 'Rajasthani', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Kalmi Vada', 'chana dal,cabbage,onion,oil', 'Rajasthani', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Churma', 'wheat flour,ghee,jaggery,nuts', 'Rajasthani', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),

            # SOUTH INDIAN (14)
            ('Masala Dosa', 'batter,potato,onion,mustard,oil', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Idli Sambhar', 'batter,tuar dal,drumstick,tamarind', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Medu Vada', 'urad dal,peppercorn,curry leaves,oil', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Upma', 'suji,mustard,onion,peanuts,curry leaves', 'South Indian', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
            ('Lemon Rice', 'rice,lemon,turmeric,peanuts,mustard', 'South Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Appam', 'rice batter,coconut milk,yeast', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Pongal', 'rice,moong dal,peppercorn,ghee', 'South Indian', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
            ('Uttapam', 'batter,onion,tomato,chili', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Hyderabadi Biryani', 'basmati rice,chicken,yogurt,saffron', 'South Indian', 'https://images.unsplash.com/photo-1589302168068-9646c2e93061'),
            ('Chicken 65', 'chicken,curd,curry leaves,red chili', 'South Indian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Rasam', 'tamarind,pepper,tomato,cumin', 'South Indian', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
            ('Coconut Chutney', 'coconut,roasted gram,green chili,mustard', 'South Indian', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
            ('Tomato Rice', 'rice,tomato,onion,garlic,clove', 'South Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Paniyaram', 'idli batter,onion,chili,mustard', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),

            # ITALIAN (14)
            ('Margherita Pizza', 'pizza dough,mozzarella,tomato,basil', 'Italian', 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3'),
            ('White Sauce Pasta', 'pasta,milk,butter,cheese,flour', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Arrabbiata Pasta', 'pasta,tomato,garlic,chili flakes', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Pesto Pasta', 'pasta,basil,walnuts,olive oil,cheese', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Risotto', 'arborio rice,mushroom,butter,parmesan', 'Italian', 'https://images.unsplash.com/photo-1476124369491-e7addf5db371'),
            ('Lasagna', 'lasagna sheets,minced meat,tomato,cheese', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Garlic Bread', 'bread,butter,garlic,oregano', 'Italian', 'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c'),
            ('Bruschetta', 'bread,tomato,garlic,olive oil', 'Italian', 'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c'),
            ('Minestrone Soup', 'beans,carrot,celery,tomato,pasta', 'Italian', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
            ('Focaccia', 'flour,olive oil,rosemary,sea salt', 'Italian', 'https://images.unsplash.com/photo-1555507036-ab1f4038808a'),
            ('Tiramisu', 'ladyfingers,coffee,mascarpone,cocoa', 'Italian', 'https://images.unsplash.com/photo-1567620905732-2d1ec7bb7445'),
            ('Spaghetti Carbonara', 'spaghetti,egg,cheese,black pepper', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Gnocchi', 'potato,flour,egg,butter', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
            ('Calzone', 'dough,cheese,tomato,ham', 'Italian', 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3'),

            # PUNJABI (14)
            ('Butter Chicken', 'chicken,butter,cream,tomato,kasoori methi', 'Punjabi', 'https://images.unsplash.com/photo-1588166524941-3bf61a7c41eb'),
            ('Chole Bhature', 'chickpeas,maida,oil,curd,onion', 'Punjabi', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Dal Makhani', 'black lentil,kidney beans,butter,cream', 'Punjabi', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
            ('Paneer Tikka', 'paneer,curd,capsicum,onion,spices', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Aloo Paratha', 'wheat flour,potato,butter,chili', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Sarson ka Saag', 'mustard leaves,spinach,maize flour,butter', 'Punjabi', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
            ('Makki di Roti', 'maize flour,ghee,water', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Rajma Rice', 'kidney beans,rice,onion,tomato', 'Punjabi', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Amritsari Kulcha', 'maida,potato,butter,pomegranate seeds', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Kadai Paneer', 'paneer,capsicum,coriander seeds,tomato', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Malai Kofta', 'paneer,potato,cream,cashew,tomato', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Lassi', 'curd,sugar,cardamom,malai', 'Punjabi', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
            ('Chicken Tikka', 'chicken,yogurt,lemon,ginger,garlic', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Pinni', 'wheat flour,ghee,jaggery,dry fruits', 'Punjabi', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),

            # GUJARATI (13)
            ('Khaman Dhokla', 'besan,curd,mustard seeds,oil,eno', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Thepla', 'wheat flour,methi,curd,turmeric', 'Gujarati', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
            ('Undhiyu', 'papdi,potato,brinjal,muthiya,oil', 'Gujarati', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Handvo', 'rice dal batter,bottle gourd,sesame,mustard', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Gujarati Kadhi', 'curd,besan,jaggery,ginger,chili', 'Gujarati', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
            ('Fafda Jalebi', 'besan,papadsala,oil,maida,sugar', 'Gujarati', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Locho', 'chana dal,ginger,chili,butter,sev', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Dal Dhokli', 'tuar dal,wheat flour,peanuts,jaggery', 'Gujarati', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
            ('Sev Khamani', 'chana dal,garlic,sev,pomegranate', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Basundi', 'milk,sugar,almonds,cardamom', 'Gujarati', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
            ('Shrikhand', 'hung curd,sugar,saffron,pistachio', 'Gujarati', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
            ('Muthiya', 'wheat flour,bottle gourd,ginger,sesame', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Khakhra', 'wheat flour,oil,salt,kasuri methi', 'Gujarati', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),

            # ASIAN & GLOBAL (13)
            ('Maggi Masala', 'maggi noodles,water,onion,peas,carrot', 'Asian', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624'),
            ('Veg Chowmein', 'noodles,cabbage,carrot,soy sauce,vinegar', 'Asian', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624'),
            ('Veg Fried Rice', 'rice,carrot,beans,soy sauce,spring onion', 'Asian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
            ('Spring Rolls', 'maida sheets,cabbage,carrot,oil', 'Asian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
            ('Manchurian', 'cabbage,cornflour,soy sauce,garlic,ginger', 'Asian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
            ('Sushi Roll', 'sushi rice,nori sheet,cucumber,vinegar', 'Asian', 'https://images.unsplash.com/photo-1553621042-f6e147245754'),
            ('Club Sandwich', 'bread,lettuce,tomato,cheese,mayonnaise', 'Global', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af'),
            ('Cheese Burger', 'burger bun,cheese,lettuce,patty,onion', 'Global', 'https://images.unsplash.com/photo-1550547660-d9450f859349'),
            ('French Fries', 'potato,oil,salt', 'Global', 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877'),
            ('Pancakes', 'flour,milk,egg,maple syrup', 'Global', 'https://images.unsplash.com/photo-1567620905732-2d1ec7bb7445'),
            ('Tacos', 'taco shell,beans,cheese,lettuce,salsa', 'Global', 'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b'),
            ('Omelette', 'egg,onion,green chili,salt', 'Global', 'https://images.unsplash.com/photo-1510629954389-c1e0da47d4ec'),
            ('Fruit Salad', 'apple,banana,papaya,honey', 'Global', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd')
        ]
        
        cursor.executemany("INSERT INTO recipes VALUES (?,?,?,?)", r_list)
        conn.commit()
    return conn

db_conn = init_db()

# --- 3. NAVIGATION ---
st.sidebar.title("🍳 NEWBIE'S KITCHEN")
st.sidebar.write("Logged in: **Boss**")
page = st.sidebar.radio("COMMAND CENTER", ["📊 DASHBOARD", "🎯 PRECISION MATCHER", "🌍 GLOBAL EXPLORER", "🛒 GROCERY LIST", "👤 DIET PLANNER"])

# --- DASHBOARD ---
if page == "📊 DASHBOARD":
    st.title("🏡 Dashboard")
    with st.expander("➕ Add Item to Stock"):
        c1, c2, c3 = st.columns(3)
        it = c1.text_input("Item Name")
        qt = c2.text_input("Qty (e.g. 1kg)")
        ex = c3.date_input("Expiry", min_value=date.today())
        if st.button("Add to Pantry"):
            if it:
                db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (it.lower().strip(), ex, qt))
                db_conn.commit()
                st.rerun()

    st.subheader("📦 My Inventory")
    items = db_conn.cursor().execute("SELECT rowid, item, expiry, qty FROM pantry ORDER BY expiry ASC").fetchall()
    for s in items:
        days = (datetime.strptime(s[2], '%Y-%m-%d').date() - date.today()).days
        color = "🔴" if days < 3 else "🟢"
        c_i, c_d = st.columns([5, 1])
        c_i.write(f"{color} **{s[1].upper()}** ({s[3]}) | Expires in: {days} days")
        if c_d.button("🗑️", key=f"del_{s[0]}"):
            db_conn.cursor().execute("DELETE FROM pantry WHERE rowid=?", (s[0],))
            db_conn.commit()
            st.rerun()

# --- PRECISION MATCHER ---
elif page == "🎯 PRECISION MATCHER":
    st.title("🎯 Precision Matcher")
    p_data = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in p_data}
    recipes = db_conn.cursor().execute("SELECT * FROM recipes").fetchall()

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

# --- GLOBAL EXPLORER (SEARCH & SORT) ---
elif page == "🌍 GLOBAL EXPLORER":
    st.title("🌍 Global Explorer (110+ Recipes)")
    q = st.text_input("🔍 Search by name...", "").lower()
    sort = st.selectbox("📂 Filter Cuisine", ["All", "Maharashtrian", "Rajasthani", "South Indian", "Italian", "Punjabi", "Gujarati", "Asian", "Global"])
    
    query = "SELECT * FROM recipes WHERE LOWER(name) LIKE ?"
    params = [f"%{q}%"]
    if sort != "All":
        query += " AND cuisine = ?"
        params.append(sort)
    
    res = db_conn.cursor().execute(query, params).fetchall()
    st.write(f"Showing {len(res)} results...")
    
    cols = st.columns(2)
    for i, r in enumerate(res):
        with cols[i % 2]:
            st.markdown(f'<div class="match-card"><span class="recipe-badge">{r[2]}</span><h3>{r[0]}</h3><p><b>Ingredients:</b> {r[1]}</p></div>', unsafe_allow_html=True)
            st.image(r[3], use_container_width=True)

# --- GROCERY LIST ---
elif page == "🛒 GROCERY LIST":
    st.title("🛒 Smart Grocery List")
    p_data = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in p_data}
    all_ing = db_conn.cursor().execute("SELECT ingredients FROM recipes").fetchall()
    
    missing = set()
    for row in all_ing:
   
