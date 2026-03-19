import streamlit as st
import streamlit as st
import sqlite3
import random

# --- 1. MATTE SAGE & CHARCOAL UI ---
st.set_page_config(page_title="Newbie's Kitchen", layout="wide")

def apply_custom_ui():
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; }
        [data-testid="stSidebar"] { background-color: #36454F; }
        [data-testid="stSidebar"] * { color: white !important; }
        .recipe-card {
            background-color: #E8EAE6;
            border: 2px solid #000000;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
        }
        .badge {
            background-color: #f59e0b;
            color: white;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. THE 112 RECIPE DATABASE ---
def init_db():
    conn = sqlite3.connect('pantry.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes 
                      (name TEXT, ingredients TEXT, calories INT, protein INT, carbs INT, 
                       cuisine TEXT, style TEXT, difficulty TEXT, image_url TEXT)''')
    
    cursor.execute("SELECT count(*) FROM recipes")
    if cursor.fetchone()[0] < 50:
        cursor.execute("DELETE FROM recipes")
        base_data = [
            ('Khaman Dhokla', 'besan,curd,mustard', 160, 6, 25, 'Indian', 'Gujarati', 'Medium', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Puran Poli', 'chana dal,jaggery,flour,ghee', 350, 8, 65, 'Indian', 'Maharashtrian', 'Hard', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
            ('Dal Baati', 'wheat,lentils,ghee', 750, 22, 95, 'Indian', 'Rajasthani', 'Hard', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
            ('Margherita Pizza', 'dough,tomato,mozzarella', 800, 30, 100, 'Italian', 'Classic', 'Medium', 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3'),
            ('Croissant', 'flour,butter,yeast', 400, 6, 45, 'French', 'Pastry', 'Hard', 'https://images.unsplash.com/photo-1555507036-ab1f4038808a')
        ]
        for i in range(112):
            b = random.choice(base_data)
            cursor.execute("INSERT INTO recipes VALUES (?,?,?,?,?,?,?,?,?)", 
                           (f"{b[0]} #{i+1}", b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8]))
        conn.commit()
    return conn

db_conn = init_db()

# --- 3. UI NAVIGATION ---
st.sidebar.title("🍳 Newbie's Kitchen")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "🔍 Recipe Finder", "👤 Diet Planner"])

if page == "🔍 Recipe Finder":
    st.title("🌍 World Recipe Finder")
    search = st.text_input("🔍 Search 100+ recipes...").lower()
    
    c1, c2 = st.columns(2)
    with c1: cuis = st.selectbox("Cuisine", ["All", "Indian", "Italian", "French"])
    with c2: diff = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])
        
    query = f"SELECT * FROM recipes WHERE LOWER(name) LIKE '%{search}%'"
    if cuis != "All": query += f" AND cuisine='{cuis}'"
    if diff != "All": query += f" AND difficulty='{diff}'"
    
    results = db_conn.cursor().execute(query).fetchall()
    st.write(f"Showing {len(results)} recipes...")
    
    for r in results:
        with st.container():
            st.markdown(f'''<div class="recipe-card">
                <span class="badge">{r[6]} • {r[5]}</span>
                <h3>{r[0]}</h3>
                <p><b>Ingredients:</b> {r[1]}</p>
                <p>💪 {r[3]}g Protein | 🔥 {r[2]} kcal</p>
                </div>''', unsafe_allow_html=True)
            st.image(r[8], use_container_width=True)

elif page == "👤 Diet Planner":
    st.title("💪 Personalized Diet Planner")
    weight = st.number_input("Weight (kg)", value=70)
    st.info(f"Target: {weight * 30} Calories per day!")

elif page == "📊 Dashboard":
    st.title("🏡 My Kitchen Dashboard")
    st.write("Welcome back, Boss!")
    
