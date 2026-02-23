import streamlit as st
import sqlite3

# --- 1. DATABASE SETUP & INITIALIZATION ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, instructions TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, recipe_id INTEGER, name TEXT,
                       FOREIGN KEY(recipe_id) REFERENCES recipes(id))''')

    # CLEAR OLD DATA to ensure only your specific 12 recipes exist
    cursor.execute("DELETE FROM ingredients")
    cursor.execute("DELETE FROM recipes")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='recipes'") 

    # YOUR SPECIFIC 12 RECIPES
    recipe_data = [
        ("Sandwich", "Butter the bread, add your fillings/cheese, and toast it.", ["Bread", "Butter", "Cheese", "Cucumber", "Tomato"]),
        ("Omelette", "Whisk eggs with salt and pepper. Fry in a pan with butter.", ["Eggs", "Butter", "Salt", "Pepper"]),
        ("Brown Rice", "Boil brown rice with double the amount of water until soft.", ["Brown Rice", "Water"]),
        ("Pohe", "Soak poha, sauté onions, mustard seeds, and turmeric. Mix together.", ["Poha", "Onion", "Turmeric", "Mustard Seeds", "Peanuts"]),
        ("Maggie", "Boil water, add tastemaker and noodles. Cook for 2 minutes.", ["Maggie Noodles", "Water", "Maggie Masala"]),
        ("Pasta", "Boil pasta and toss with garlic, olive oil, or sauce.", ["Pasta", "Garlic", "Olive Oil", "Cheese"]),
        ("Dosa", "Spread fermented batter on a hot tawa. Drizzle oil and cook until crisp.", ["Dosa Batter", "Oil", "Potato"]),
        ("Tea", "Boil water with tea powder, sugar, and milk.", ["Tea Powder", "Sugar", "Milk", "Water", "Ginger"]),
        ("Coffee", "Mix coffee powder with hot milk and sugar.", ["Coffee Powder", "Milk", "Sugar", "Water"]),
        ("Khichadi", "Pressure cook rice and moong dal together with turmeric and salt.", ["Rice", "Moong Dal", "Turmeric", "Salt", "Ghee"]),
        ("Chips", "Thinly slice potatoes and deep fry until crispy. Add salt.", ["Potato", "Oil", "Salt"]),
        ("Lemonade", "Mix lemon juice, water, and sugar. Serve chilled.", ["Lemon", "Water", "Sugar", "Ice"])
    ]

    for r_name, r_inst, r_ings in recipe_data:
        cursor.execute("INSERT INTO recipes (name, instructions) VALUES (?,?)", (r_name, r_inst))
        r_id = cursor.lastrowid
        for ing in r_ings:
            cursor.execute("INSERT INTO ingredients (recipe_id, name) VALUES (?,?)", (r_id, ing))
    
    conn.commit()
    return conn

db_conn = init_db()

# --- 2. STREAMLIT UI SETUP ---
# Updated page title for the browser tab
st.set_page_config(page_title="Newbie's Kitchen", page_icon="🍳")

# Updated Sidebar Name as requested
st.sidebar.title("👨‍🍳 Newbie's Kitchen")
page = st.sidebar.radio("Go to:", ["Manage My Pantry", "Smart Recipe Finder"])

# --- 3. INTERFACE 1: MANAGE MY PANTRY ---
if page == "Manage My Pantry":
    st.header("🛒 My Digital Pantry")
    
    if 'my_pantry' not in st.session_state:
        st.session_state.my_pantry = []

    col1, col2 = st.columns([3, 1])
    with col1:
        new_item = st.text_input("Add ingredient (e.g., Bread, Poha, Milk):")
    with col2:
        st.write("##") 
        if st.button("Add Item"):
            if new_item and new_item not in st.session_state.my_pantry:
                st.session_state.my_pantry.append(new_item.strip().title())
                st.rerun()

    st.subheader("Current Stock")
    if st.session_state.my_pantry:
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state.my_pantry):
            cols[idx % 3].info(f"✔ {item}")
        if st.button("Clear Pantry"):
            st.session_state.my_pantry = []
            st.rerun()
    else:
        st.info("Your pantry is empty! Start adding ingredients to see what you can cook.")

# --- 4. INTERFACE 2: SMART RECIPE FINDER ---
elif page == "Smart Recipe Finder":
    st.header("🔍 Smart Recipe Matcher")
    
    if not st.session_state.get('my_pantry'):
        st.warning("⚠️ Go to 'Manage My Pantry' to add ingredients first!")
    else:
        st.write(f"Finding recipes for your: **{', '.join(st.session_state.my_pantry)}**")
        
        query = '''
            SELECT r.name, r.instructions, GROUP_CONCAT(i.name) as required_ings
            FROM recipes r
            JOIN ingredients i ON r.id = i.recipe_id
            GROUP BY r.id
        '''
        cursor = db_conn.cursor()
        cursor.execute(query)
        all_recipes = cursor.fetchall()

        results = []
        for name, instructions, req_ings in all_recipes:
            req_list = req_ings.split(',')
            user_set = set(st.session_state.my_pantry)
            req_set = set(req_list)
            
            matches = user_set.intersection(req_set)
            score = (len(matches) / len(req_set)) * 100
            
            if score > 0:
                results.append((score, name, instructions, req_list, list(req_set - user_set)))

        results.sort(key=lambda x: x[0], reverse=True)

        if results:
            for score, name, instructions, req_list, missing in results:
                with st.expander(f"{name} — {score:.0f}% Match"):
                    st.progress(score / 100)
                    st.write("**Ingredients:**", ", ".join(req_list))
                    st.write("**Method:**", instructions)
                    if missing:
                        st.error(f"Missing items: {', '.join(missing)}")
                    else:
                        st.success("You have everything to make this!")
        else:
            st.info("No recipes match your ingredients yet. Try adding more items like 'Bread' or 'Maggie Noodles'.")