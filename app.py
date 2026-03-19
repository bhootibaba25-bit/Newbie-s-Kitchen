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
    cursor.execute('''CREATE TABLE recipes (name TEXT, ingredients TEXT, instructions TEXT, cuisine TEXT, img TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, expiry DATE, qty TEXT)''')
    
    # 110+ MANUALLY WRITTEN UNIQUE RECIPES (NO LOOPS)
    r_list = [
        # MAHARASHTRIAN (15)
        ('Poha', 'poha,onion,peanuts,mustard,turmeric', 'Soak poha. Sauté onions and peanuts. Mix and steam.', 'Maharashtrian', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
        ('Misal Pav', 'sprouts,pav,onion,farsan,lemon', 'Make spicy sprout gravy. Serve with pav and farsan.', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Vada Pav', 'potato,pav,garlic,gram flour,chili', 'Fry spiced potato balls in batter. Serve in pav.', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Pav Bhaji', 'potato,pav,butter,peas,cauliflower', 'Mash veggies, cook with butter and spices. Toast pav.', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Puran Poli', 'wheat flour,chana dal,jaggery,ghee', 'Stuff sweet lentil paste in dough and roast with ghee.', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Sabudana Khichadi', 'sabudana,peanuts,potato,cumin', 'Sauté soaked sago with crushed peanuts and potato.', 'Maharashtrian', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
        ('Thalipeeth', 'bhajani flour,onion,cucumber,curd', 'Flatten dough on pan. Roast with oil until crispy.', 'Maharashtrian', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Sol Kadhi', 'kokum,coconut milk,garlic,chili', 'Blend coconut milk with kokum and garlic. Serve cold.', 'Maharashtrian', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
        ('Kothimbir Vadi', 'coriander,besan,sesame,oil', 'Steam coriander-besan cakes and then shallow fry.', 'Maharashtrian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Bharli Vangi', 'brinjal,peanuts,coconut,godamasala', 'Stuff brinjals with peanut masala and slow cook.', 'Maharashtrian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Modak', 'rice flour,jaggery,coconut,ghee', 'Steam rice dumplings stuffed with sweet coconut.', 'Maharashtrian', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Basundi', 'milk,sugar,cardamom,charoli', 'Reduce milk until thick. Add sugar and nuts.', 'Maharashtrian', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
        ('Zunka Bhakri', 'besan,onion,garlic,jowar flour', 'Thick gram flour paste served with jowar roti.', 'Maharashtrian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Pitla', 'besan,green chili,garlic,turmeric', 'Liquid gram flour curry tempered with garlic.', 'Maharashtrian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Aamti', 'tur dal,godamasala,kokum,jaggery', 'Maharashtrian dal with sweet and sour notes.', 'Maharashtrian', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),

        # RAJASTHANI (14)
        ('Dal Bati', 'wheat flour,moong dal,ghee,garlic', 'Bake wheat balls. Serve with spicy dal and ghee.', 'Rajasthani', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
        ('Gatte ki Sabji', 'gram flour,curd,mustard oil', 'Boil besan logs. Cook in a spicy yogurt gravy.', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Ker Sangri', 'ker,sangri,dry mango,oil', 'Traditional desert beans and berries stir-fry.', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Mirchi Bada', 'chili,potato,besan,oil', 'Spicy stuffed chili fritters.', 'Rajasthani', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Panchmel Dal', 'tuar dal,chana dal,moong dal,urad dal,masoor dal', 'Five lentil dal tempered with ghee and cloves.', 'Rajasthani', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
        ('Laal Maas', 'mutton,red chili,ghee,yogurt', 'Slow cooked spicy mutton in mathania chilies.', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Bajra Khichdi', 'pearl millet,moong dal,ghee', 'Slow cooked bajra and lentil porridge.', 'Rajasthani', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
        ('Gond Ke Laddu', 'edible gum,wheat flour,ghee,nuts', 'Winter special sweet balls made with gum.', 'Rajasthani', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Mawa Kachori', 'maida,mawa,sugar,nuts', 'Sweet kachori dipped in sugar syrup.', 'Rajasthani', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Papad ki Sabji', 'papad,curd,turmeric,cumin', 'Roasted papad cooked in yogurt gravy.', 'Rajasthani', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Mohanthal', 'besan,ghee,sugar,cardamom', 'Traditional Rajasthani besan fudge.', 'Rajasthani', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Kalmi Vada', 'chana dal,onion,chili,ginger', 'Crispy deep-fried lentil snacks.', 'Rajasthani', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Churma', 'wheat flour,sugar,ghee,cardamom', 'Crushed wheat balls mixed with ghee and sugar.', 'Rajasthani', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
        ('Kadhibadi', 'besan,yogurt,cumin,oil', 'Yogurt curry with gram flour dumplings.', 'Rajasthani', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),

        # SOUTH INDIAN (14)
        ('Masala Dosa', 'batter,potato,onion,mustard', 'Thin rice crepe stuffed with potato masala.', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
        ('Idli Sambhar', 'batter,dal,drumstick,tamarind', 'Steamed rice cakes with lentil stew.', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
        ('Medu Vada', 'urad dal,peppercorn,oil', 'Crispy donut-shaped lentil fritters.', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
        ('Upma', 'suji,mustard,onion,curry leaves', 'Savory semolina porridge.', 'South Indian', 'https://images.unsplash.com/photo-1603073163308-9654c3fb70b5'),
        ('Lemon Rice', 'rice,lemon,turmeric,peanuts', 'Tangy rice tempered with mustard and lemon.', 'South Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
        ('Appam', 'rice,coconut milk,yeast', 'Fermented rice pancakes with soft centers.', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
        ('Pongal', 'rice,moong dal,pepper,ghee', 'Savory rice and lentil mash.', 'South Indian', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
        ('Uttapam', 'batter,onion,tomato,chili', 'Thick rice pancakes with veggie toppings.', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
        ('Rasam', 'tamarind,pepper,cumin,tomato', 'Clear spicy and tangy soup.', 'South Indian', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
        ('Curd Rice', 'rice,curd,mustard,salt', 'Soft rice mixed with yogurt and tempering.', 'South Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
        ('Paniyaram', 'idli batter,onion,mustard', 'Small steamed and fried batter balls.', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc'),
        ('Bisi Bele Bath', 'rice,tuar dal,veggies,special masala', 'Spicy lentil and rice mash with veggies.', 'South Indian', 'https://images.unsplash.com/photo-1605333396915-47ed6b68a00e'),
        ('Tomato Rice', 'rice,tomato,onion,garlic', 'Spicy tomato-flavored rice.', 'South Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
        ('Coconut Rice', 'rice,coconut,mustard,oil', 'Rice flavored with fresh grated coconut.', 'South Indian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),

        # ITALIAN (13)
        ('Margherita Pizza', 'dough,mozzarella,tomato,basil', 'Bake dough with tomato, cheese, and basil.', 'Italian', 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3'),
        ('White Sauce Pasta', 'pasta,milk,butter,cheese', 'Boil pasta. Mix with bechamel sauce and cheese.', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
        ('Arrabbiata Pasta', 'pasta,tomato,garlic,chili', 'Spicy tomato sauce with garlic and pasta.', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
        ('Pesto Pasta', 'pasta,basil,walnuts,cheese', 'Fresh basil and nut sauce mixed with pasta.', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
        ('Risotto', 'arborio rice,mushroom,butter', 'Slow cooked creamy rice with mushrooms.', 'Italian', 'https://images.unsplash.com/photo-1476124369491-e7addf5db371'),
        ('Lasagna', 'sheets,tomato sauce,cheese,meat', 'Layered pasta sheets with sauce and cheese.', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
        ('Garlic Bread', 'bread,butter,garlic,herbs', 'Toast bread with garlic butter and herbs.', 'Italian', 'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c'),
        ('Bruschetta', 'bread,tomato,olive oil,garlic', 'Toasted bread topped with fresh tomatoes.', 'Italian', 'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c'),
        ('Minestrone', 'beans,carrot,celery,pasta', 'Healthy Italian vegetable soup.', 'Italian', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
        ('Focaccia', 'flour,olive oil,rosemary', 'Italian flatbread with herbs.', 'Italian', 'https://images.unsplash.com/photo-1555507036-ab1f4038808a'),
        ('Tiramisu', 'biscuits,coffee,mascarpone', 'Layered coffee-flavored dessert.', 'Italian', 'https://images.unsplash.com/photo-1567620905732-2d1ec7bb7445'),
        ('Gnocchi', 'potato,flour,butter', 'Soft potato dumplings in butter sauce.', 'Italian', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),
        ('Calzone', 'dough,cheese,tomato,ham', 'Folded pizza stuffed with fillings.', 'Italian', 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3'),

        # PUNJABI (13)
        ('Butter Chicken', 'chicken,butter,cream,tomato', 'Creamy tomato-based chicken curry.', 'Punjabi', 'https://images.unsplash.com/photo-1588166524941-3bf61a7c41eb'),
        ('Chole Bhature', 'chickpeas,maida,oil,curd', 'Spicy chickpeas with fried flatbread.', 'Punjabi', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Dal Makhani', 'black lentil,butter,cream', 'Slow cooked creamy black lentils.', 'Punjabi', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
        ('Paneer Tikka', 'paneer,yogurt,capsicum,onion', 'Grilled spiced paneer cubes.', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Aloo Paratha', 'wheat flour,potato,butter', 'Flatbread stuffed with spicy potato.', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Sarson Saag', 'mustard leaves,spinach,butter', 'Traditional winter mustard greens.', 'Punjabi', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
        ('Makki Roti', 'maize flour,ghee', 'Cornmeal flatbread.', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Rajma Rice', 'kidney beans,rice,tomato', 'Spicy kidney beans served with rice.', 'Punjabi', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
        ('Kadai Paneer', 'paneer,capsicum,onion,tomato', 'Spicy paneer in a thick capsicum gravy.', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Malai Kofta', 'paneer,potato,cream,cashew', 'Fried dumplings in a creamy sauce.', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Lassi', 'curd,sugar,cardamom', 'Sweet thickened yogurt drink.', 'Punjabi', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
        ('Chicken Tikka', 'chicken,yogurt,lemon,ginger', 'Roasted spiced chicken chunks.', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Shahi Paneer', 'paneer,cream,tomato,almonds', 'Royal creamy paneer curry.', 'Punjabi', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),

        # GUJARATI (13)
        ('Khaman Dhokla', 'besan,curd,mustard,oil', 'Steamed savory gram flour cakes.', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Thepla', 'wheat flour,methi,curd', 'Spiced flatbread with fenugreek leaves.', 'Gujarati', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Undhiyu', 'papdi,potato,brinjal,beans', 'Winter vegetable medley.', 'Gujarati', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Handvo', 'rice batter,gourd,mustard', 'Savory vegetable cake.', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Gujarati Kadhi', 'curd,besan,jaggery,ginger', 'Sweet and sour yogurt curry.', 'Gujarati', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
        ('Fafda', 'besan,oil,papadsala', 'Crispy chickpea flour snack.', 'Gujarati', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Locho', 'chana dal,butter,sev', 'Steamed spicy gram flour snack.', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Dal Dhokli', 'tuar dal,wheat flour,peanuts', 'Wheat dumplings cooked in lentil stew.', 'Gujarati', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
        ('Shrikhand', 'curd,sugar,saffron,pistachio', 'Sweetened hung yogurt dessert.', 'Gujarati', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
        ('Sev Khamani', 'chana dal,sev,pomegranate', 'Crumbled dhokla topped with sev.', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Muthiya', 'wheat flour,bottle gourd,sesame', 'Steamed or fried vegetable dumplings.', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),
        ('Khakhra', 'wheat flour,oil,salt,methi', 'Crispy thin flatbread.', 'Gujarati', 'https://images.unsplash.com/photo-1596797038558-b615ae96515b'),
        ('Patra', 'taro leaves,besan,jaggery', 'Steamed stuffed colocasia leaves.', 'Gujarati', 'https://images.unsplash.com/photo-1626132647523-66f5bf380027'),

        # ASIAN & GLOBAL (13)
        ('Maggi', 'maggi noodles,water,onion,peas', 'Boil noodles with masala and veggies.', 'Asian', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624'),
        ('Veg Fried Rice', 'rice,carrot,soy sauce,beans', 'Stir-fry rice with veggies and sauces.', 'Asian', 'https://images.unsplash.com/photo-1512058560366-cd24270083cd'),
        ('Veg Chowmein', 'noodles,cabbage,soy sauce', 'Stir-fry noodles with cabbage and soy.', 'Asian', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624'),
        ('Manchurian', 'cabbage,garlic,ginger,soy sauce', 'Fried veggie balls in spicy gravy.', 'Asian', 'https://images.unsplash.com/photo-1610192244261-3f13bc7175e9'),
        ('Spring Rolls', 'sheets,cabbage,carrot,oil', 'Wrapped veggies deep fried.', 'Asian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Veg Burger', 'bun,patty,lettuce,cheese', 'Burger bun with patty and fresh veggies.', 'Global', 'https://images.unsplash.com/photo-1550547660-d9450f859349'),
        ('Club Sandwich', 'bread,lettuce,tomato,cheese,mayo', 'Triple-layered toasted sandwich.', 'Global', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af'),
        ('Omelette', 'egg,onion,chili,salt', 'Whisked eggs fried with onions and chili.', 'Global', 'https://images.unsplash.com/photo-1510629954389-c1e0da47d4ec'),
        ('French Fries', 'potato,oil,salt', 'Deep fried potato strips.', 'Global', 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877'),
        ('Pancakes', 'flour,milk,egg,syrup', 'Fluffy breakfast pancakes.', 'Global', 'https://images.unsplash.com/photo-1567620905732-2d1ec7bb7445'),
        ('Tacos', 'shell,beans,cheese,salsa', 'Crispy shells with beans and cheese.', 'Global', 'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b'),
        ('Fruit Salad', 'apple,banana,grapes,honey', 'Fresh cut fruits with honey drizzle.', 'Global', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
        ('Pasta Salad', 'pasta,tomato,olives,dressing', 'Cold pasta mixed with veggies.', 'Global', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141'),

        # ADDITIONAL UNIQUE SNACKS/DRINKS (10)
                ('Cold Coffee', 'milk,coffee,sugar,ice', 'Blended chilled coffee.', 'Global', 'https://images.unsplash.com/photo-1541167760496-162955ed8a9f'),
        ('Lemonade', 'lemon,water,sugar,mint', 'Refreshing citrus drink.', 'Global', 'https://images.unsplash.com/photo-1523472721958-978152f4d69b'),
        ('Masala Tea', 'milk,tea,ginger,cardamom', 'Spiced Indian milk tea.', 'Global', 'https://images.unsplash.com/photo-1544787210-22bb83063677'),
        ('Corn Salad', 'corn,onion,lemon,salt', 'Boiled corn with tangy dressing.', 'Global', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
        ('Garlic Mushrooms', 'mushroom,garlic,butter', 'Sautéed mushrooms in garlic butter.', 'Global', 'https://images.unsplash.com/photo-1476124369491-e7addf5db371'),
        ('Stuffed Capsicum', 'capsicum,potato,spices', 'Bell peppers stuffed with potato mash.', 'Indian', 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'),
        ('Bread Roll', 'bread,potato,oil', 'Deep fried bread rolls stuffed with potato.', 'Indian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Bhel Puri', 'puffed rice,onion,chutney,sev', 'Savory Indian street food snack.', 'Indian', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84'),
        ('Tomato Soup', 'tomato,cream,garlic,pepper', 'Smooth and creamy tomato soup.', 'Global', 'https://images.unsplash.com/photo-1547592166-23ac45744acd'),
        ('Grilled Cheese', 'bread,butter,cheese', 'Toasted sandwich with melted cheese.', 'Global', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af')
    ]
    
    cursor.executemany("INSERT INTO recipes VALUES (?,?,?,?,?)", r_list)
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
    with st.expander("➕ Add Item Manually"):
        c1, c2, c3 = st.columns(3)
        it = c1.text_input("Item")
        qt = c2.text_input("Quantity")
        ex = c3.date_input("Expiry")
        if st.button("Add to Stock"):
            db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (it.lower().strip(), ex, qt))
            db_conn.commit()
            st.rerun()

    items = db_conn.cursor().execute("SELECT rowid, item, expiry, qty FROM pantry ORDER BY expiry ASC").fetchall()
    for s in items:
        days = (datetime.strptime(s[2], '%Y-%m-%d').date() - date.today()).days
        c_i, c_d = st.columns([5, 1])
        c_i.write(f"**{s[1].upper()}** ({s[3]}) | {days} days left")
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
        name, ing_str, instr, cuis, img = r
        ing_list = [i.strip().lower() for i in ing_str.split(',') if i.strip()]
        have = [i for i in ing_list if i in p_set]
        missing = [i for i in ing_list if i not in p_set]
        if ing_list:
            pct = int((len(have)/len(ing_list))*100)
            if pct > 0:
                with st.container():
                    st.markdown('<div class="match-card">', unsafe_allow_html=True)
                    col_info, col_img = st.columns([3, 1])
                    with col_info:
                        st.markdown(f"### {name} ({cuis}) - {pct}% Match")
                        st.progress(pct/100)
                        st.markdown(f'<div class="have-box">✅ HAVE: {", ".join(have)}</div>', unsafe_allow_html=True)
                        if missing: st.markdown(f'<div class="missing-box">❌ MISSING: {", ".join(missing)}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="recipe-box"><b>📖 Instructions:</b><br>{instr}</div>', unsafe_allow_html=True)
                    with col_img: st.image(img, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: GLOBAL EXPLORER ---
elif page == "🌍 GLOBAL EXPLORER":
    st.title("🌍 Explore 105+ Unique Recipes")
    q = st.text_input("🔍 Search recipe name...", "").lower()
    sort = st.selectbox("📂 Cuisine", ["All", "Maharashtrian", "Rajasthani", "South Indian", "Italian", "Punjabi", "Gujarati", "Asian", "Global"])
    query = "SELECT * FROM recipes WHERE LOWER(name) LIKE ?"
    params = [f"%{q}%"]
    if sort != "All": query += " AND cuisine = ?"; params.append(sort)
    res = db_conn.cursor().execute(query, params).fetchall()
    cols = st.columns(2)
    for i, r in enumerate(res):
        with cols[i % 2]:
            st.markdown(f'<div class="match-card"><span class="recipe-badge">{r[3]}</span><h3>{r[0]}</h3><p>{r[1]}</p></div>', unsafe_allow_html=True)
            st.image(r[4], use_container_width=True)

# --- PAGE: GROCERY LIST ---
elif page == "🛒 GROCERY LIST":
    st.title("🛒 Smart Grocery List")
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
            is_checked = c_check.checkbox(f"Buy {m.title()}", key=f"buy_{m}")
            qty_val = c_qty.text_input("Quantity", "1 unit", key=f"qty_{m}")
            exp_val = c_exp.date_input("Set Expiry", date.today(), key=f"exp_{m}")
            if is_checked: selected_items.append((m, exp_val, qty_val))
    
    if st.button("🛒 Add Selected to Stock"):
        for item, ex, q in selected_items:
            db_conn.cursor().execute("INSERT INTO pantry VALUES (?,?,?)", (item, ex, q))
        db_conn.commit()
        st.success("Successfully added to Dashboard!")
        st.rerun()

# --- DIET PLANNER ---
elif page == "👤 DIET PLANNER":
    st.title("👤 Body Profile")
    w = st.number_input("Weight (kg)", 30, 150, 70)
    h = st.number_input("Height (cm)", 100, 250, 175)
    bmi = round(w / ((h/100)**2), 1)
    st.info(f"BMI: {bmi} | Daily Intake: {int((10*w)+(6.25*h)-120)} kcal")
    
