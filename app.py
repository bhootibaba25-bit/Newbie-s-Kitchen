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
        .recipe-box { background-color: #FFFFFF; border: 1px solid #36454F; padding: 15px; border-radius: 8px; margin-top: 10px; }
        .recipe-badge { background-color: #36454F; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; display: inline-block; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. THE 110+ UNIQUE HARD-CODED DATABASE ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS recipes")
    cursor.execute('''CREATE TABLE recipes (name TEXT, ingredients TEXT, instructions TEXT, cuisine TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, expiry DATE, qty TEXT)''')
    
    r_list = [
        # MAHARASHTRIAN (1-15)
        ('Poha', 'poha,onion,peanuts,mustard,turmeric', 'Soak poha. Sauté onions and peanuts. Mix and steam.', 'Maharashtrian'),
        ('Misal Pav', 'sprouts,pav,onion,farsan,lemon', 'Make spicy sprout gravy. Serve with pav and farsan.', 'Maharashtrian'),
        ('Vada Pav', 'potato,pav,garlic,gram flour,chili', 'Fry spiced potato balls in batter. Serve in pav.', 'Maharashtrian'),
        ('Pav Bhaji', 'potato,pav,butter,peas,cauliflower', 'Mash veggies, cook with butter and spices. Toast pav.', 'Maharashtrian'),
        ('Puran Poli', 'wheat flour,chana dal,jaggery,ghee', 'Stuff sweet lentil paste in dough and roast with ghee.', 'Maharashtrian'),
        ('Sabudana Khichadi', 'sabudana,peanuts,potato,cumin', 'Sauté soaked sago with crushed peanuts and potato.', 'Maharashtrian'),
        ('Thalipeeth', 'bhajani flour,onion,cucumber,curd', 'Flatten dough on pan. Roast with oil until crispy.', 'Maharashtrian'),
        ('Sol Kadhi', 'kokum,coconut milk,garlic,chili', 'Blend coconut milk with kokum and garlic. Serve cold.', 'Maharashtrian'),
        ('Kothimbir Vadi', 'coriander,besan,sesame,oil', 'Steam coriander-besan cakes and then shallow fry.', 'Maharashtrian'),
        ('Bharli Vangi', 'brinjal,peanuts,coconut,godamasala', 'Stuff brinjals with peanut masala and slow cook.', 'Maharashtrian'),
        ('Modak', 'rice flour,jaggery,coconut,ghee', 'Steam rice dumplings stuffed with sweet coconut.', 'Maharashtrian'),
        ('Basundi', 'milk,sugar,cardamom,charoli', 'Reduce milk until thick. Add sugar and nuts.', 'Maharashtrian'),
        ('Zunka Bhakri', 'besan,onion,garlic,jowar flour', 'Thick gram flour paste served with jowar roti.', 'Maharashtrian'),
        ('Pitla', 'besan,green chili,garlic,turmeric', 'Liquid gram flour curry tempered with garlic.', 'Maharashtrian'),
        ('Aamti', 'tur dal,godamasala,kokum,jaggery', 'Maharashtrian dal with sweet and sour notes.', 'Maharashtrian'),
        # RAJASTHANI (16-29)
        ('Dal Bati', 'wheat flour,moong dal,ghee,garlic', 'Bake wheat balls. Serve with spicy dal and ghee.', 'Rajasthani'),
        ('Gatte ki Sabji', 'gram flour,curd,mustard oil', 'Boil besan logs. Cook in a spicy yogurt gravy.', 'Rajasthani'),
        ('Ker Sangri', 'ker,sangri,dry mango,oil', 'Traditional desert beans and berries stir-fry.', 'Rajasthani'),
        ('Mirchi Bada', 'chili,potato,besan,oil', 'Spicy stuffed chili fritters.', 'Rajasthani'),
        ('Panchmel Dal', 'tuar dal,chana dal,moong dal,urad dal,masoor dal', 'Five lentil dal tempered with ghee.', 'Rajasthani'),
        ('Laal Maas', 'mutton,red chili,ghee,yogurt', 'Slow cooked spicy mutton in mathania chilies.', 'Rajasthani'),
        ('Bajra Khichdi', 'pearl millet,moong dal,ghee', 'Slow cooked bajra and lentil porridge.', 'Rajasthani'),
        ('Gond Ke Laddu', 'edible gum,wheat flour,ghee,nuts', 'Winter special sweet balls made with gum.', 'Rajasthani'),
        ('Mawa Kachori', 'maida,mawa,sugar,nuts', 'Sweet kachori dipped in sugar syrup.', 'Rajasthani'),
        ('Papad ki Sabji', 'papad,curd,turmeric,cumin', 'Roasted papad cooked in yogurt gravy.', 'Rajasthani'),
        ('Mohanthal', 'besan,ghee,sugar,cardamom', 'Traditional Rajasthani besan fudge.', 'Rajasthani'),
        ('Kalmi Vada', 'chana dal,onion,chili,ginger', 'Crispy deep-fried lentil snacks.', 'Rajasthani'),
        ('Churma', 'wheat flour,sugar,ghee,cardamom', 'Crushed wheat balls mixed with ghee and sugar.', 'Rajasthani'),
        ('Kadhibadi', 'besan,yogurt,cumin,oil', 'Yogurt curry with gram flour dumplings.', 'Rajasthani'),
        # SOUTH INDIAN (30-43)
        ('Masala Dosa', 'batter,potato,onion,mustard', 'Thin rice crepe stuffed with potato masala.', 'South Indian'),
        ('Idli Sambhar', 'batter,dal,drumstick,tamarind', 'Steamed rice cakes with lentil stew.', 'South Indian'),
        ('Medu Vada', 'urad dal,peppercorn,oil', 'Crispy donut-shaped lentil fritters.', 'South Indian'),
        ('Upma', 'suji,mustard,onion,curry leaves', 'Savory semolina porridge.', 'South Indian'),
        ('Lemon Rice', 'rice,lemon,turmeric,peanuts', 'Tangy rice tempered with mustard and lemon.', 'South Indian'),
        ('Appam', 'rice,coconut milk,yeast', 'Fermented rice pancakes with soft centers.', 'South Indian'),
        ('Pongal', 'rice,moong dal,pepper,ghee', 'Savory rice and lentil mash.', 'South Indian'),
        ('Uttapam', 'batter,onion,tomato,chili', 'Thick rice pancakes with veggie toppings.', 'South Indian'),
        ('Rasam', 'tamarind,pepper,cumin,tomato', 'Clear spicy and tangy soup.', 'South Indian'),
        ('Curd Rice', 'rice,curd,mustard,salt', 'Soft rice mixed with yogurt and tempering.', 'South Indian'),
        ('Paniyaram', 'idli batter,onion,mustard', 'Small steamed and fried batter balls.', 'South Indian'),
        ('Bisi Bele Bath', 'rice,tuar dal,veggies,special masala', 'Spicy lentil and rice mash with veggies.', 'South Indian'),
        ('Tomato Rice', 'rice,tomato,onion,garlic', 'Spicy tomato-flavored rice.', 'South Indian'),
        ('Coconut Rice', 'rice,coconut,mustard,oil', 'Rice flavored with fresh grated coconut.', 'South Indian'),
        # ITALIAN (44-56)
        ('Margherita Pizza', 'dough,mozzarella,tomato,basil', 'Bake dough with tomato, cheese, and basil.', 'Italian'),
        ('White Sauce Pasta', 'pasta,milk,butter,cheese', 'Boil pasta. Mix with bechamel sauce and cheese.', 'Italian'),
        ('Arrabbiata Pasta', 'pasta,tomato,garlic,chili', 'Spicy tomato sauce with garlic and pasta.', 'Italian'),
        ('Pesto Pasta', 'pasta,basil,walnuts,cheese', 'Fresh basil and nut sauce mixed with pasta.', 'Italian'),
        ('Risotto', 'arborio rice,mushroom,butter', 'Slow cooked creamy rice with mushrooms.', 'Italian'),
        ('Lasagna', 'sheets,tomato sauce,cheese,meat', 'Layered pasta sheets with sauce and cheese.', 'Italian'),
        ('Garlic Bread', 'bread,butter,garlic,herbs', 'Toast bread with garlic butter and herbs.', 'Italian'),
        ('Bruschetta', 'bread,tomato,olive oil,garlic', 'Toasted bread topped with fresh tomatoes.', 'Italian'),
        ('Minestrone', 'beans,carrot,celery,pasta', 'Healthy Italian vegetable soup.', 'Italian'),
        ('Focaccia', 'flour,olive oil,rosemary', 'Italian flatbread with herbs.', 'Italian'),
        ('Tiramisu', 'biscuits,coffee,mascarpone', 'Layered coffee-flavored dessert.', 'Italian'),
        ('Gnocchi', 'potato,flour,butter', 'Soft potato dumplings in butter sauce.', 'Italian'),
        ('Calzone', 'dough,cheese,tomato,ham', 'Folded pizza stuffed with fillings.', 'Italian'),
        # PUNJABI (57-69)
        ('Butter Chicken', 'chicken,butter,cream,tomato', 'Creamy tomato-based chicken curry.', 'Punjabi'),
        ('Chole Bhature', 'chickpeas,maida,oil,curd', 'Spicy chickpeas with fried flatbread.', 'Punjabi'),
        ('Dal Makhani', 'black lentil,butter,cream', 'Slow cooked creamy black lentils.', 'Punjabi'),
        ('Paneer Tikka', 'paneer,yogurt,capsicum,onion', 'Grilled spiced paneer cubes.', 'Punjabi'),
        ('Aloo Paratha', 'wheat flour,potato,butter', 'Flatbread stuffed with spicy potato.', 'Punjabi'),
        ('Sarson Saag', 'mustard leaves,spinach,butter', 'Traditional winter mustard greens.', 'Punjabi'),
        ('Makki Roti', 'maize flour,ghee', 'Cornmeal flatbread.', 'Punjabi'),
        ('Rajma Rice', 'kidney beans,rice,tomato', 'Spicy kidney beans served with rice.', 'Punjabi'),
        ('Kadai Paneer', 'paneer,capsicum,onion,tomato', 'Spicy paneer in a thick capsicum gravy.', 'Punjabi'),
        ('Malai Kofta', 'paneer,potato,cream,cashew', 'Fried dumplings in a creamy sauce.', 'Punjabi'),
        ('Lassi', 'curd,sugar,cardamom', 'Sweet thickened yogurt drink.', 'Punjabi'),
        ('Chicken Tikka', 'chicken,yogurt,lemon,ginger', 'Roasted spiced chicken chunks.', 'Punjabi'),
        ('Shahi Paneer', 'paneer,cream,tomato,almonds', 'Royal creamy paneer curry.', 'Punjabi'),
        # GUJARATI (70-82)
        ('Khaman Dhokla', 'besan,curd,mustard,oil', 'Steamed savory gram flour cakes.', 'Gujarati'),
        ('Thepla', 'wheat flour,methi,curd', 'Spiced flatbread with fenugreek leaves.', 'Gujarati'),
        ('Undhiyu', 'papdi,potato,brinjal,beans', 'Winter vegetable medley.', 'Gujarati'),
        ('Handvo', 'rice batter,gourd,mustard', 'Savory vegetable cake.', 'Gujarati'),
        ('Gujarati Kadhi', 'curd,besan,jaggery,ginger', 'Sweet and sour yogurt curry.', 'Gujarati'),
        ('Fafda', 'besan,oil,papadsala', 'Crispy chickpea flour snack.', 'Gujarati'),
        ('Locho', 'chana dal,butter,sev', 'Steamed spicy gram flour snack.', 'Gujarati'),
        ('Dal Dhokli', 'tuar dal,wheat flour,peanuts', 'Wheat dumplings cooked in lentil stew.', 'Gujarati'),
        ('Shrikhand', 'curd,sugar,saffron,pistachio', 'Sweetened hung yogurt dessert.', 'Gujarati'),
        ('Sev Khamani', 'chana dal,sev,pomegranate', 'Crumbled dhokla topped with sev.', 'Gujarati'),
        ('Muthiya', 'wheat flour,bottle gourd,sesame', 'Steamed or fried vegetable dumplings.', 'Gujarati'),
        ('Khakhra', 'wheat flour,oil,salt,methi', 'Crispy thin flatbread.', 'Gujarati'),
        ('Patra', 'taro leaves,besan,jaggery', 'Steamed stuffed colocasia leaves.', 'Gujarati'),
        # ASIAN & GLOBAL (83-95)
        ('Maggi', 'maggi noodles,water,onion,peas', 'Boil noodles with masala and veggies.', 'Asian'),
        ('Veg Fried Rice', 'rice,carrot,soy sauce,beans', 'Stir-fry rice with veggies and sauces.', 'Asian'),
        ('Veg Chowmein', 'noodles,cabbage,soy sauce', 'Stir-fry noodles with cabbage and soy.', 'Asian'),
        ('Manchurian', 'cabbage,garlic,ginger,soy sauce', 'Fried veggie balls in spicy gravy.', 'Asian'),
        ('Spring Rolls', 'sheets,cabbage,carrot,oil', 'Wrapped veggies deep fried.', 'Asian'),
        ('Veg Burger', 'bun,patty,lettuce,cheese', 'Burger bun with patty and fresh veggies.', 'Global'),
        ('Club Sandwich', 'bread,lettuce,tomato,cheese,mayo', 'Triple-layered toasted sandwich.', 'Global'),
        ('Omelette', 'egg,onion,chili,salt', 'Whisked eggs fried with onions and chili.', 'Global'),
        ('French Fries', 'potato,oil,salt', 'Deep fried potato strips.', 'Global'),
        ('Pancakes', 'flour,milk,egg,syrup', 'Fluffy breakfast pancakes.', 'Global'),
        ('Tacos', 'shell,beans,cheese,salsa', 'Crispy shells with beans and cheese.', 'Global'),
        ('Fruit Salad', 'apple,banana,grapes,honey', 'Fresh cut fruits with honey drizzle.', 'Global'),
        ('Pasta Salad', 'pasta,tomato,olives,dressing', 'Cold pasta mixed with veggies.', 'Global'),
        # SNACKS & SIDES (96-110)
        ('Cold Coffee', 'milk,coffee,sugar,ice', 'Blended chilled coffee.', 'Global'),
        ('Lemonade', 'lemon,water,sugar,mint', 'Refreshing citrus drink.', 'Global'),
        ('Masala Tea', 'milk,tea,ginger,cardamom', 'Spiced Indian milk tea.', 'Global'),
        ('Corn Salad', 'corn,onion,lemon,salt', 'Boiled corn with tangy dressing.', 'Global'),
        ('Garlic Mushrooms', 'mushroom,garlic,butter', 'Sautéed mushrooms in garlic butter.', 'Global'),
        ('Stuffed Capsicum', 'capsicum,potato,spices', 'Bell peppers stuffed with potato mash.', 'Indian'),
        ('Bread Roll', 'bread,potato,oil', 'Deep fried bread rolls stuffed with potato.', 'Indian'),
        ('Bhel Puri', 'puffed rice,onion,chutney,sev', 'Savory Indian street food snack.', 'Indian'),
        ('Tomato Soup', 'tomato,cream,garlic,pepper', 'Smooth and creamy tomato soup.', 'Global'),
        ('Grilled Cheese', 'bread,butter,cheese', 'Toasted sandwich with melted cheese.', 'Global'),
        ('Sev Puri', 'puri,potato,onion,chutney,sev', 'Indian flat puris topped with spicy mixtures.', 'Indian'),
        ('Dahi Puri', 'puri,curd,potato,tamarind chutney', 'Hollow puris filled with yogurt and spices.', 'Indian'),
        ('Papad Roast', 'papad,cumin,oil', 'Roasted or fried lentil crackers.', 'Indian'),
        ('Veg Cutlet', 'potato,carrot,peas,bread crumbs', 'Deep fried vegetable patties.', 'Indian'),
        ('Aloo Tikki', 'potato,ginger,chili,oil', 'Spiced fried potato cakes.', 'Indian')
    ]
    
    cursor.executemany("INSERT INTO recipes VALUES (?,?,?,?)", r_list)
    conn.commit()
    return conn

db_conn = init_db()

# --- 3. NAVIGATION ---
st.sidebar.title("🍳 NEWBIE'S KITCHEN")
st.sidebar.write("Logged in: **Boss**")
page = st.sidebar.radio("NAVIGATE", ["📊 DASHBOARD", "🎯 PRECISION MATCHER", "🌍 GLOBAL EXPLORER", "🛒 GROCERY LIST", "👤 DIET PLANNER"])

# --- PAGE: DASHBOARD ---
if page == "📊 DASHBOARD":
    st.title("🏡 My Dashboard")
    with st.expander("➕ Quick Add to Stock"):
        c1, c2, c3 = st.columns(3)
        it = c1.text_input("Item Name")
        qt = c2.text_input("Quantity")
        ex = c3.date_input("Expiry Date", min_value=date.today())
        if st.button("Save to Pantry"):
            if it:
                db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (it.lower().strip(), ex, qt))
                db_conn.commit()
                st.success(f"Added {it}!")
                st.rerun()

    items = db_conn.cursor().execute("SELECT rowid, item, expiry, qty FROM pantry ORDER BY expiry ASC").fetchall()
    for s in items:
        days = (datetime.strptime(s[2], '%Y-%m-%d').date() - date.today()).days
        color = "🔴" if days < 3 else "🟢"
        c_i, c_d = st.columns([5, 1])
        c_i.write(f"{color} **{s[1].upper()}** ({s[3]}) | {days} days left")
        if c_d.button("🗑️", key=f"del_{s[0]}"):
            db_conn.cursor().execute("DELETE FROM pantry WHERE rowid=?", (s[0],))
            db_conn.commit()
            st.rerun()

# --- PAGE: PRECISION MATCHER ---
elif page == "🎯 PRECISION MATCHER":
    st.title("🎯 Precision Matcher")
    p_data = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in p_data}
    recipes = db_conn.cursor().execute("SELECT * FROM recipes").fetchall()

    for r in recipes:
        name, ing_str, instr, cuis = r
        ing_list = [i.strip().lower() for i in ing_str.split(',') if i.strip()]
        have = [i for i in ing_list if i in p_set]
        missing = [i for i in ing_list if i not in p_set]
        if ing_list:
            pct = int((len(have)/len(ing_list))*100)
            if pct > 0:
                with st.container():
                    st.markdown('<div class="match-card">', unsafe_allow_html=True)
                    st.markdown(f"### {name} ({cuis}) - {pct}% Match")
                    st.progress(pct/100)
                    st.markdown(f'<div class="have-box">✅ HAVE: {", ".join(have)}</div>', unsafe_allow_html=True)
                    if missing: st.markdown(f'<div class="missing-box">❌ MISSING: {", ".join(missing)}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="recipe-box"><b>📖 Instructions:</b><br>{instr}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: GLOBAL EXPLORER ---
elif page == "🌍 GLOBAL EXPLORER":
    st.title("🌍 Explore 110+ Unique Recipes")
    q = st.text_input("🔍 Search recipe name...", "").lower()
    sort = st.selectbox("📂 Filter by Cuisine", ["All", "Maharashtrian", "Rajasthani", "South Indian", "Italian", "Punjabi", "Gujarati", "Asian", "Global"])
    query = "SELECT * FROM recipes WHERE LOWER(name) LIKE ?"
    params = [f"%{q}%"]
    if sort != "All": query += " AND cuisine = ?"; params.append(sort)
    res = db_conn.cursor().execute(query, params).fetchall()
    for r in res:
        with st.container():
            st.markdown(f'<div class="match-card"><span class="recipe-badge">{r[3]}</span><h3>{r[0]}</h3><p><b>Ingredients:</b> {r[1]}</p><p style="color:gray;"><b>Method:</b> {r[2]}</p></div>', unsafe_allow_html=True)

# --- PAGE: GROCERY LIST ---
elif page == "🛒 GROCERY LIST":
    st.title("🛒 Smart Grocery List")
    with st.expander("➕ Add Item Manually"):
        c1, c2, c3 = st.columns(3)
        it = c1.text_input("Item")
        qt = c2.text_input("Qty")
        ex = c3.date_input("Exp Date", key="groc_exp")
        if st.button("Add to Stock", key="groc_add"):
            db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (it.lower().strip(), ex, qt))
            db_conn.commit()
            st.rerun()

    p_data = db_conn.cursor().execute("SELECT item FROM pantry").fetchall()
    p_set = {r[0].lower().strip() for r in p_data}
    all_ing = db_conn.cursor().execute("SELECT ingredients FROM recipes").fetchall()
    missing = set()
    for row in all_ing:
        for i in row[0].split(','):
            if i.strip().lower() not in p_set: missing.add(i.strip().lower())
    
    selected_items = []
    for m in sorted(list(missing))[:30]:
        with st.container():
            c_check, c_qty, c_exp = st.columns([2, 2, 2])
            if c_check.checkbox(f"Buy {m.title()}", key=f"buy_{m}"):
                selected_items.append((m, c_exp.date_input("Set Expiry", date.today(), key=f"exp_{m}"), c_qty.text_input("Set Qty", "1 unit", key=f"qty_{m}")))
    
    if st.button("🛒 Confirm Purchase"):
        for item, ex, q in selected_items:
            db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (item, ex, q))
        db_conn.commit()
        st.success("Successfully added to Dashboard!")
        st.rerun()

# --- PAGE: DIET PLANNER ---
elif page == "👤 DIET PLANNER":
    st.title("👤 Body Profile")
    w = st.number_input("Weight (kg)", 30, 150, 70)
    h = st.number_input("Height (cm)", 100, 250, 175)
    bmi = round(w / ((h/100)**2), 1)
    st.info(f"BMI: {bmi} | Daily Intake: {int((10*w)+(6.25*h)-120)} kcal")
    
