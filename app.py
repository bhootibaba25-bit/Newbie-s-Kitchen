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
                # --- BLOCK 1: MAHARASHTRIAN (15 UNIQUE RECIPES) ---
        ('Poha', 'poha,onion,peanuts,mustard,turmeric,curry leaves,lemon', 
         '1. Rinse 2 cups poha and drain. 2. Heat 2 tbsp oil; add mustard seeds, curry leaves, and peanuts. 3. Sauté chopped onions and green chilies until translucent. 4. Add turmeric and poha; salt to taste. 5. Cover and steam for 2 mins. Garnish with lemon and coriander.'),
        
        ('Misal Pav', 'sprouts,pav,onion,farsan,lemon,ginger-garlic,coconut', 
         '1. Pressure cook moth bean sprouts. 2. Sauté onions, garlic, and dried coconut; grind into a paste. 3. Heat oil, add the paste and Misal masala until oil separates. 4. Add sprouts and water to make a thin spicy gravy (Kat). 5. Serve topped with farsan, raw onions, and pav.'),
        
        ('Vada Pav', 'potato,pav,garlic,gram flour,chili,turmeric,mustard', 
         '1. Boil and mash potatoes. 2. Sauté mustard seeds, garlic-chili paste, and turmeric; mix with potatoes. 3. Make round balls. 4. Dip in a thick batter of besan, salt, and water. 5. Deep fry until golden. Serve inside pav with dry garlic chutney.'),
        
        ('Pav Bhaji', 'potato,pav,butter,peas,cauliflower,tomato,onion,capsicum', 
         '1. Boil and mash potatoes, peas, and cauliflower. 2. Sauté onions, capsicum, and tomatoes in butter. 3. Add Pav Bhaji masala and salt; mix in the mashed veggies. 4. Simmer for 10 mins, adding water for consistency. 5. Serve with pav toasted in extra butter.'),
        
        ('Puran Poli', 'wheat flour,chana dal,jaggery,ghee,cardamom,nutmeg', 
         '1. Boil chana dal until soft, drain, and cook with jaggery until thick. 2. Mash and grind into a smooth paste (Puran) with cardamom. 3. Knead a soft dough of wheat flour and oil. 4. Stuff a ball of Puran into the dough. 5. Roll thin and roast on a tawa with plenty of ghee.'),
        
        ('Sabudana Khichadi', 'sabudana,peanuts,potato,cumin,chili,ghee', 
         '1. Soak sabudana overnight (use 1:1 water ratio). 2. Mix with roasted crushed peanuts and salt. 3. Sauté cumin, chopped potatoes, and chilies in ghee. 4. Add the sabudana mixture. 5. Cook on low heat until sabudana turns translucent. Do not overmix.'),
        
        ('Thalipeeth', 'bhajani flour,onion,cucumber,curd,coriander,cumin', 
         '1. Mix 2 cups bhajani flour with grated cucumber, onions, and spices. 2. Add curd to bind into a soft dough. 3. Pat the dough onto a greased pan or damp cloth. 4. Make 3 holes, add oil, and roast both sides on medium heat until dark brown and crispy.'),
        
        ('Sol Kadhi', 'kokum,coconut milk,garlic,chili,salt,coriander', 
         '1. Soak 8-10 kokum petals in warm water for 30 mins. 2. Extract fresh coconut milk (or use canned). 3. Strain the kokum water into the milk. 4. Add crushed garlic, green chili paste, and salt. 5. Chill for 1 hour before serving as a post-meal digestive.'),
        
        ('Kothimbir Vadi', 'coriander,besan,sesame,oil,turmeric,ginger', 
         '1. Mix 2 cups chopped coriander with besan, ginger paste, and sesame seeds. 2. Shape into a log and steam for 15-20 mins. 3. Once cool, slice the log into 1/2 inch thick pieces. 4. Deep or shallow fry until the edges are very crunchy. Serve with tea.'),
        
        ('Bharli Vangi', 'brinjal,peanuts,coconut,godamasala,ginger,jaggery', 
         '1. Slit small brinjals crosswise (don’t cut off stalks). 2. Make a stuffing of roasted peanut powder, coconut, godamasala, and ginger. 3. Stuff the brinjals tightly. 4. Heat oil, sauté the brinjals, add a little water. 5. Cover and slow-cook until the brinjals are tender.'),
        
        ('Modak', 'rice flour,jaggery,coconut,ghee,cardamom', 
         '1. Cook grated coconut and jaggery until sticky; add cardamom. 2. Add rice flour to boiling water with ghee; cover and let it steam. 3. Knead the warm flour into a smooth dough. 4. Shape into small cups, fill with coconut stuffing, and pleat. 5. Steam for 12 mins.'),
        
        ('Basundi', 'milk,sugar,cardamom,charoli,saffron', 
         '1. Boil 1 litre full-cream milk in a wide pan. 2. Reduce the milk to half by simmering and scraping the sides. 3. Add 1/2 cup sugar and saffron. 4. Stir in cardamom powder and charoli. 5. Serve warm or chilled with puris.'),
        
        ('Zunka', 'besan,onion,garlic,oil,cumin,mustard,chili', 
         '1. Sauté mustard seeds, cumin, and lots of chopped garlic. 2. Add onions and sauté until brown. 3. Add red chili powder and water. 4. Slowly stir in besan to avoid lumps until it forms a thick, dry paste. 5. Cover and steam for 5 mins. Serve with bhakri.'),
        
        ('Pitla', 'besan,green chili,garlic,turmeric,coriander', 
         '1. Whisk besan with water to make a thin slurry. 2. Temper oil with garlic, green chilies, and turmeric. 3. Pour the slurry into the pan, stirring constantly. 4. Cook until it thickens into a smooth, flowing curry. 5. Garnish with coriander and serve hot.'),
        
        ('Aamti', 'tur dal,godamasala,kokum,jaggery,curry leaves,mustard', 
         '1. Pressure cook tur dal and whisk it smooth. 2. Add godamasala, kokum petals, salt, and a piece of jaggery. 3. Heat oil; add mustard seeds, curry leaves, and hing. 4. Pour the tempering into the dal. 5. Simmer for 10 mins until the flavors blend perfectly.'),
        
                # --- BLOCK 2: RAJASTHANI (15 UNIQUE RECIPES) ---
        ('Dal Bati Churma', 'wheat flour,moong dal,chana dal,ghee,garlic,jaggery', 
         '1. Knead a tight dough of wheat flour and ghee; bake into hard round balls (Bati). 2. Prepare a spicy mixed dal with garlic tempering. 3. Crush some Batis, mix with ghee and jaggery to make Churma. 4. Serve the Batis dipped in a bowl of pure ghee with dal and churma.'),
        
        ('Gatte ki Sabji', 'gram flour,curd,mustard oil,cumin,turmeric,ajwain', 
         '1. Mix besan with spices and oil; knead into a dough and roll into cylinders. 2. Boil the rolls in water, then cut into small chunks (Gatte). 3. Prepare a gravy with whisked curd, turmeric, and chili powder. 4. Add the Gatte to the boiling gravy and simmer until the sauce thickens.'),
        
        ('Ker Sangri', 'ker berries,sangri beans,dry mango,mustard oil,raisins', 
         '1. Soak ker and sangri overnight; boil until tender. 2. Heat mustard oil and add cumin and hing. 3. Sauté the berries and beans with amchur (dry mango), chili, and turmeric. 4. Add raisins for a touch of sweetness. 5. This dish is dry and lasts for days without refrigeration.'),
        
        ('Mirchi Bada', 'large green chili,potato,gram flour,fennel,oil', 
         '1. Slit large bhavnagri chilies and remove seeds. 2. Stuff with a spicy mashed potato mixture flavored with fennel seeds. 3. Dip the stuffed chili in a thick besan batter. 4. Deep fry on medium heat until the outer crust is crispy and golden brown.'),
        
        ('Panchmel Dal', 'tuar dal,chana dal,moong dal,urad dal,masoor dal,ghee,clove', 
         '1. Pressure cook all five lentils together with salt and turmeric. 2. In a small pan, heat ghee and add cloves, cinnamon, and cumin. 3. Add chopped ginger and green chilies. 4. Pour the tempering over the cooked dal and simmer for 5 minutes for the smoky aroma.'),
        
        ('Laal Maas', 'mutton,mathania red chili,ghee,curd,garlic,cloves', 
         '1. Marinate mutton in curd and salt. 2. Soak mathania chilies in water and grind to a paste. 3. Heat ghee; sauté whole spices and lots of garlic. 4. Add mutton and chili paste. 5. Slow cook for 1.5 hours until the meat is tender and the oil separates.'),
        
        ('Bajra Khichdi', 'pearl millet,moong dal,ghee,salt,water', 
         '1. Coarsely pound the bajra and wash it well. 2. Pressure cook with yellow moong dal, salt, and 5 parts water. 3. Stir continuously after opening to make it creamy. 4. Serve steaming hot with a massive dollop of ghee and optional jaggery on the side.'),
        
        ('Gond Ke Laddu', 'edible gum,wheat flour,ghee,almonds,jaggery', 
         '1. Fry edible gum (gond) in ghee until it puffs up like popcorn; crush it. 2. Roast wheat flour in ghee until fragrant and brown. 3. Mix the flour, gond, chopped almonds, and melted jaggery. 4. Roll into tight balls while still warm. Excellent for winter health.'),
        
        ('Papad ki Sabji', 'papad,curd,turmeric,cumin,coriander,ghee', 
         '1. Roast 3-4 urad dal papads and break into medium pieces. 2. Make a base of curd mixed with chili and turmeric. 3. Temper ghee with cumin and hing; add the curd mixture. 4. Once it boils, drop the papad pieces in. 5. Cook for just 2 mins so the papad stays slightly firm.'),
        
        ('Mohanthal', 'besan,ghee,sugar,cardamom,saffron,milk', 
         '1. Mix besan with a little milk and ghee to create grains. 2. Roast the mixture in ghee until deep golden. 3. Prepare a 1.5 string sugar syrup. 4. Mix the roasted besan into the syrup with cardamom and saffron. 5. Set in a tray and garnish with silver leaf.'),
        
        ('Kalmi Vada', 'chana dal,onion,green chili,ginger,fennel,oil', 
         '1. Soak chana dal and grind it coarsely with ginger and chilies. 2. Add fennel seeds and chopped onions. 3. Shape into thick patties and deep fry once. 4. Cut the fried patties into strips and deep fry again until extra crunchy. Serve with mint chutney.'),
        
        ('Churma', 'wheat flour,ghee,sugar,cardamom,almonds', 
         '1. Make a stiff dough of wheat flour and ghee. 2. Fry or bake thick muthiyas (logs) until brown. 3. Grate or grind the muthiyas into a fine powder. 4. Mix with powdered sugar, cardamom, and warm ghee. 5. Add sliced almonds for crunch.'),
        
        ('Kadhibadi', 'besan,yogurt,cumin,ginger,curry leaves,oil', 
         '1. Make small besan pakoras (Badi) and fry them. 2. Whisk yogurt and besan with water for the Kadhi base. 3. Temper with cumin, dry red chilies, and ginger. 4. Simmer the Kadhi for 20 mins. 5. Add the Badis at the end and let them soak up the tangy yogurt.'),
        
        ('Mawa Kachori', 'maida,mawa,sugar,cardamom,saffron,nuts,ghee', 
         '1. Stuff a dough of maida with a sweet mixture of roasted mawa, nuts, and cardamom. 2. Deep fry on very low heat until golden. 3. Dip the hot kachori in warm sugar syrup for 2 minutes. 4. Garnish with saffron strands and serve warm.'),
        
        ('Shahi Gatte', 'besan,mawa,curd,ginger-garlic,kashmiri chili', 
         '1. Stuff the gram flour logs (Gatte) with a small amount of mawa and nuts before boiling. 2. Fry the boiled gatte for extra richness. 3. Prepare a creamy gravy with curd, ginger, and cashew paste. 4. Simmer the stuffed gatte in this royal sauce.'),

         # --- BLOCK 3: SOUTH INDIAN (15 UNIQUE RECIPES) ---
        ('Masala Dosa', 'rice,urad dal,potato,onion,mustard,curry leaves,methi', 
         '1. Soak rice and urad dal with methi seeds; grind and ferment for 8 hours. 2. Spread batter thin on a hot tawa. 3. Sauté mustard, onions, and turmeric with boiled potatoes for the filling. 4. Place filling in the center, fold, and serve with coconut chutney.'),
        
        ('Idli Sambhar', 'idli rice,urad dal,tuar dal,drumstick,tamarind,sambhar masala', 
         '1. Steam fermented rice-dal batter in greased molds for 10 mins. 2. Boil tuar dal with drumsticks, pumpkin, and tamarind pulp. 3. Add sambhar masala and temper with mustard and red chilies. 4. Serve the soft idlis dipped in hot sambhar.'),
        
        ('Medu Vada', 'urad dal,peppercorn,curry leaves,ginger,green chili,oil', 
         '1. Grind soaked urad dal into a very thick, fluffy paste using minimal water. 2. Mix in crushed peppercorns, ginger, and curry leaves. 3. Shape into donuts with a hole in the middle. 4. Deep fry in hot oil until golden brown and crispy on the outside.'),
        
        ('Upma', 'suji,mustard seeds,onion,peanuts,curry leaves,ginger,ghee', 
         '1. Dry roast semolina (suji) until fragrant. 2. Heat ghee; sauté mustard, peanuts, urad dal, onions, and ginger. 3. Add 3 cups of boiling water to 1 cup suji. 4. Stir constantly to avoid lumps and steam for 5 mins until fluffy.'),
        
        ('Lemon Rice', 'cooked rice,lemon,turmeric,peanuts,mustard,curry leaves', 
         '1. Use cooled, cooked rice. 2. Heat oil; fry peanuts until crunchy, then add mustard, hing, and turmeric. 3. Turn off the heat and stir in fresh lemon juice. 4. Pour the tempering over the rice and mix gently with salt and coriander.'),
        
        ('Appam', 'raw rice,coconut milk,yeast,sugar,salt', 
         '1. Grind soaked rice with coconut milk and a pinch of yeast; ferment overnight. 2. Pour a ladle of thin batter into an Appam Chatti (curved pan). 3. Swirl the pan to coat the sides while keeping the center thick. 4. Cover and steam until the edges are crispy.'),
        
        ('Ven Pongal', 'rice,moong dal,black pepper,cumin,ginger,ghee,cashews', 
         '1. Pressure cook rice and moong dal together until very soft and mushy. 2. Heat plenty of ghee; fry cashews, crushed peppercorns, cumin, and ginger. 3. Add the tempering to the rice-dal mix. 4. Serve hot with coconut chutney and sambhar.'),
        
        ('Uttapam', 'dosa batter,onion,tomato,green chili,coriander,oil', 
         '1. Use slightly sour fermented dosa batter. 2. Pour a thick ladle on the tawa (don’t spread thin). 3. Top with finely chopped onions, tomatoes, and chilies. 4. Drizzle oil and cook both sides until the onions are caramelized and the base is crisp.'),
        
        ('Rasam', 'tamarind,tomato,black pepper,cumin,garlic,mustard', 
         '1. Boil tamarind water with chopped tomatoes and salt. 2. Coarsely grind pepper, cumin, and garlic. 3. Add the ground spices to the boiling water. 4. Temper with mustard and dry red chilies. 5. Garnish with coriander; serve as a soup or with rice.'),
        
        ('Curd Rice', 'rice,curd,milk,mustard,ginger,curry leaves,pomegranate', 
         '1. Overcook rice so it is very soft. 2. Mash the rice while warm, then add milk and curd. 3. Temper with mustard seeds, ginger, and curry leaves. 4. Mix in fresh pomegranate seeds or grapes for a traditional cooling finish.'),
        
        ('Paniyaram', 'idli batter,onion,mustard,chana dal,oil', 
         '1. Sauté onions and chana dal; mix into idli batter. 2. Heat a Paniyaram pan and grease the holes with oil. 3. Pour batter into holes and cook until the bottom is crisp. 4. Flip using a wooden skewer and cook the other side until golden.'),
        
        ('Bisi Bele Bath', 'rice,tuar dal,mixed veggies,tamarind,special spice powder', 
         '1. Cook rice, dal, and veggies (beans, carrots, peas) together. 2. Prepare a spice paste with cinnamon, cloves, and urad dal. 3. Mix tamarind pulp and the spice paste into the rice. 4. Temper with cashews fried in ghee.'),
        
        ('Tomato Rice', 'rice,tomato,onion,garlic,cinnamon,cloves,mint', 
         '1. Sauté whole spices, onions, and garlic. 2. Add plenty of chopped tomatoes and cook until mushy. 3. Mix in cooked rice, salt, and fresh mint leaves. 4. Let it sit for 10 mins for the flavors to absorb before serving.'),
        
        ('Coconut Rice', 'rice,fresh coconut,urad dal,mustard,dry red chili', 
         '1. Grate fresh coconut. 2. Heat oil; sauté mustard, urad dal, and red chilies until the dal turns golden. 3. Add the grated coconut and sauté for 1 minute (don’t brown it). 4. Mix in cooked rice and salt. Serve with papad.'),
        
        ('Avial', 'yam,carrot,beans,drumstick,coconut,curd,coconut oil', 
         '1. Cut mixed vegetables into long batons and boil with turmeric. 2. Grind coconut, green chilies, and cumin into a coarse paste. 3. Add the paste and thick curd to the veggies. 4. Finish with a generous drizzle of raw coconut oil and curry leaves.')
        
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
    
