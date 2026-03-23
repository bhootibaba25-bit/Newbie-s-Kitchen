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
        .recipe-box { background-color: #FFFFFF; border: 1px solid #36454F; padding: 15px; border-radius: 8px; margin-top: 10px; font-size: 14px; line-height: 1.6; }
        .recipe-badge { background-color: #36454F; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; display: inline-block; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_ui()

# --- 2. DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('pantry.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS recipes")
    cursor.execute('''CREATE TABLE recipes (name TEXT, ingredients TEXT, instructions TEXT, cuisine TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pantry (item TEXT, expiry DATE, qty TEXT)''')
    
    r_list = [
        # --- MAHARASHTRIAN (15) ---
        ('Poha', 'poha,onion,peanuts,mustard,turmeric,curry leaves,lemon', '1. Rinse 2 cups poha and drain. 2. Heat 2 tbsp oil; add mustard seeds, curry leaves, and peanuts. 3. Sauté chopped onions and green chilies until translucent. 4. Add turmeric and poha; salt to taste. 5. Cover and steam for 2 mins. Garnish with lemon and coriander.', 'Maharashtrian'),
        ('Misal Pav', 'sprouts,pav,onion,farsan,lemon,ginger-garlic,coconut', '1. Pressure cook moth bean sprouts. 2. Sauté onions, garlic, and dried coconut; grind into a paste. 3. Heat oil, add the paste and Misal masala until oil separates. 4. Add sprouts and water to make a thin spicy gravy (Kat). 5. Serve topped with farsan, raw onions, and pav.', 'Maharashtrian'),
        ('Vada Pav', 'potato,pav,garlic,gram flour,chili,turmeric,mustard', '1. Boil and mash potatoes. 2. Sauté mustard seeds, garlic-chili paste, and turmeric; mix with potatoes. 3. Make round balls. 4. Dip in a thick batter of besan, salt, and water. 5. Deep fry until golden. Serve inside pav with dry garlic chutney.', 'Maharashtrian'),
        ('Pav Bhaji', 'potato,pav,butter,peas,cauliflower,tomato,onion,capsicum', '1. Boil and mash potatoes, peas, and cauliflower. 2. Sauté onions, capsicum, and tomatoes in butter. 3. Add Pav Bhaji masala and salt; mix in the mashed veggies. 4. Simmer for 10 mins, adding water for consistency. 5. Serve with pav toasted in extra butter.', 'Maharashtrian'),
        ('Puran Poli', 'wheat flour,chana dal,jaggery,ghee,cardamom,nutmeg', '1. Boil chana dal until soft, drain, and cook with jaggery until thick. 2. Mash and grind into a smooth paste (Puran) with cardamom. 3. Knead a soft dough of wheat flour and oil. 4. Stuff a ball of Puran into the dough. 5. Roll thin and roast on a tawa with plenty of ghee.', 'Maharashtrian'),
        ('Sabudana Khichadi', 'sabudana,peanuts,potato,cumin,chili,ghee', '1. Soak sabudana overnight (use 1:1 water ratio). 2. Mix with roasted crushed peanuts and salt. 3. Sauté cumin, chopped potatoes, and chilies in ghee. 4. Add the sabudana mixture. 5. Cook on low heat until sabudana turns translucent. Do not overmix.', 'Maharashtrian'),
        ('Thalipeeth', 'bhajani flour,onion,cucumber,curd,coriander,cumin', '1. Mix 2 cups bhajani flour with grated cucumber, onions, and spices. 2. Add curd to bind into a soft dough. 3. Pat the dough onto a greased pan or damp cloth. 4. Make 3 holes, add oil, and roast both sides on medium heat until dark brown and crispy.', 'Maharashtrian'),
        ('Sol Kadhi', 'kokum,coconut milk,garlic,chili,salt,coriander', '1. Soak 8-10 kokum petals in warm water for 30 mins. 2. Extract fresh coconut milk (or use canned). 3. Strain the kokum water into the milk. 4. Add crushed garlic, green chili paste, and salt. 5. Chill for 1 hour before serving as a post-meal digestive.', 'Maharashtrian'),
        ('Kothimbir Vadi', 'coriander,besan,sesame,oil,turmeric,ginger', '1. Mix 2 cups chopped coriander with besan, ginger paste, and sesame seeds. 2. Shape into a log and steam for 15-20 mins. 3. Once cool, slice the log into 1/2 inch thick pieces. 4. Deep or shallow fry until the edges are very crunchy. Serve with tea.', 'Maharashtrian'),
        ('Bharli Vangi', 'brinjal,peanuts,coconut,godamasala,ginger,jaggery', '1. Slit small brinjals crosswise (don’t cut off stalks). 2. Make a stuffing of roasted peanut powder, coconut, godamasala, and ginger. 3. Stuff the brinjals tightly. 4. Heat oil, sauté the brinjals, add a little water. 5. Cover and slow-cook until the brinjals are tender.', 'Maharashtrian'),
        ('Modak', 'rice flour,jaggery,coconut,ghee,cardamom', '1. Cook grated coconut and jaggery until sticky; add cardamom. 2. Add rice flour to boiling water with ghee; cover and let it steam. 3. Knead the warm flour into a smooth dough. 4. Shape into small cups, fill with coconut stuffing, and pleat. 5. Steam for 12 mins.', 'Maharashtrian'),
        ('Basundi', 'milk,sugar,cardamom,charoli,saffron', '1. Boil 1 litre full-cream milk in a wide pan. 2. Reduce the milk to half by simmering and scraping the sides. 3. Add 1/2 cup sugar and saffron. 4. Stir in cardamom powder and charoli. 5. Serve warm or chilled with puris.', 'Maharashtrian'),
        ('Zunka', 'besan,onion,garlic,oil,cumin,mustard,chili', '1. Sauté mustard seeds, cumin, and lots of chopped garlic. 2. Add onions and sauté until brown. 3. Add red chili powder and water. 4. Slowly stir in besan to avoid lumps until it forms a thick, dry paste. 5. Cover and steam for 5 mins. Serve with bhakri.', 'Maharashtrian'),
        ('Pitla', 'besan,green chili,garlic,turmeric,coriander', '1. Whisk besan with water to make a thin slurry. 2. Temper oil with garlic, green chilies, and turmeric. 3. Pour the slurry into the pan, stirring constantly. 4. Cook until it thickens into a smooth, flowing curry. 5. Garnish with coriander and serve hot.', 'Maharashtrian'),
        ('Aamti', 'tur dal,godamasala,kokum,jaggery,curry leaves,mustard', '1. Pressure cook tur dal and whisk it smooth. 2. Add godamasala, kokum petals, salt, and a piece of jaggery. 3. Heat oil; add mustard seeds, curry leaves, and hing. 4. Pour the tempering into the dal. 5. Simmer for 10 mins until the flavors blend perfectly.', 'Maharashtrian'),

        # --- RAJASTHANI (15) ---
        ('Dal Bati', 'wheat flour,moong dal,chana dal,ghee,garlic,jaggery', '1. Knead tight dough of wheat flour and ghee; bake into hard round balls (Bati). 2. Prepare spicy mixed dal with garlic tempering. 3. Crush some Batis, mix with ghee and jaggery to make Churma. 4. Serve Batis dipped in pure ghee with dal.', 'Rajasthani'),
        ('Gatte ki Sabji', 'gram flour,curd,mustard oil,cumin,turmeric,ajwain', '1. Mix besan with spices and oil; knead dough and roll cylinders. 2. Boil rolls, then cut into chunks (Gatte). 3. Prepare gravy with curd, turmeric, chili. 4. Add Gatte to boiling gravy and simmer until sauce thickens.', 'Rajasthani'),
        ('Ker Sangri', 'ker berries,sangri beans,dry mango,mustard oil,raisins', '1. Soak ker and sangri overnight; boil until tender. 2. Heat mustard oil; add cumin and hing. 3. Sauté berries and beans with amchur, chili, turmeric. 4. Add raisins for sweetness. Dry dish that lasts for days.', 'Rajasthani'),
        ('Mirchi Bada', 'large green chili,potato,gram flour,fennel,oil', '1. Slit large green chilies and remove seeds. 2. Stuff with spicy mashed potato flavored with fennel. 3. Dip in thick besan batter. 4. Deep fry on medium heat until crust is crispy and golden brown.', 'Rajasthani'),
        ('Panchmel Dal', 'tuar dal,chana dal,moong dal,urad dal,masoor dal,ghee,clove', '1. Pressure cook all five lentils with salt/turmeric. 2. Heat ghee; add cloves, cinnamon, cumin, ginger, and chilies. 3. Pour tempering over dal and simmer for 5 mins for smoky aroma.', 'Rajasthani'),
        ('Laal Maas', 'mutton,mathania red chili,ghee,curd,garlic,cloves', '1. Marinate mutton in curd/salt. 2. Grind mathania chilies to paste. 3. Heat ghee; sauté whole spices and garlic. 4. Add mutton and chili paste. 5. Slow cook until meat is tender and oil separates.', 'Rajasthani'),
        ('Bajra Khichdi', 'pearl millet,moong dal,ghee,salt,water', '1. Coarsely pound bajra. 2. Pressure cook with moong dal, salt, and 5 parts water. 3. Stir continuously after opening to make it creamy. 4. Serve hot with a dollop of ghee and jaggery.', 'Rajasthani'),
        ('Gond Ke Laddu', 'edible gum,wheat flour,ghee,almonds,jaggery', '1. Fry gond in ghee until it puffs up; crush it. 2. Roast wheat flour in ghee until brown. 3. Mix flour, gond, almonds, and melted jaggery. 4. Roll into balls while warm.', 'Rajasthani'),
        ('Papad ki Sabji', 'papad,curd,turmeric,cumin,coriander,ghee', '1. Roast papads and break into pieces. 2. Make curd base with chili and turmeric. 3. Temper ghee with cumin and hing; add curd mixture. 4. Once boiling, drop papad in and cook for 2 mins.', 'Rajasthani'),
        ('Mohanthal', 'besan,ghee,sugar,cardamom,saffron,milk', '1. Mix besan with milk/ghee to create grains. 2. Roast in ghee until deep golden. 3. Prepare sugar syrup. 4. Mix roasted besan into syrup with cardamom and saffron. 5. Set in a tray and garnish.', 'Rajasthani'),
        ('Kalmi Vada', 'chana dal,onion,green chili,ginger,fennel,oil', '1. Grind soaked chana dal coarsely with ginger/chilies. 2. Add fennel and onions. 3. Shape into patties and fry once. 4. Cut into strips and fry again until extra crunchy.', 'Rajasthani'),
        ('Churma', 'wheat flour,ghee,sugar,cardamom,almonds', '1. Make stiff dough of wheat flour/ghee. 2. Fry thick muthiyas until brown. 3. Grind muthiyas into fine powder. 4. Mix with powdered sugar, cardamom, and warm ghee. 5. Add almonds.', 'Rajasthani'),
        ('Kadhibadi', 'besan,yogurt,cumin,ginger,curry leaves,oil', '1. Fry besan pakoras (Badi). 2. Whisk yogurt and besan with water for Kadhi base. 3. Temper with cumin, red chilies, and ginger. 4. Simmer for 20 mins; add Badis at the end.', 'Rajasthani'),
        ('Mawa Kachori', 'maida,mawa,sugar,cardamom,saffron,nuts,ghee', '1. Stuff maida dough with roasted mawa, nuts, and cardamom. 2. Deep fry on low heat until golden. 3. Dip hot kachori in warm sugar syrup for 2 mins. 4. Garnish with saffron.', 'Rajasthani'),
        ('Shahi Gatte', 'besan,mawa,curd,ginger-garlic,kashmiri chili', '1. Stuff besan logs with mawa/nuts before boiling. 2. Fry boiled gatte. 3. Prepare creamy gravy with curd and cashew paste. 4. Simmer stuffed gatte in this royal sauce.', 'Rajasthani'),

        # --- SOUTH INDIAN (15) ---
        ('Masala Dosa', 'rice,urad dal,potato,onion,mustard,curry leaves,methi', '1. Ferment rice-dal batter for 8 hours. 2. Spread thin on hot tawa. 3. Sauté mustard, onions, turmeric with boiled potatoes for filling. 4. Place filling in center, fold, and serve.', 'South Indian'),
        ('Idli Sambhar', 'idli rice,urad dal,tuar dal,drumstick,tamarind,sambhar masala', '1. Steam rice-dal batter in molds. 2. Boil tuar dal with drumsticks/tamarind. 3. Add sambhar masala and temper with mustard. 4. Serve soft idlis dipped in sambhar.', 'South Indian'),
        ('Medu Vada', 'urad dal,peppercorn,curry leaves,ginger,green chili,oil', '1. Grind soaked urad dal into thick fluffy paste. 2. Mix peppercorns and curry leaves. 3. Shape into donuts with hole. 4. Deep fry until golden brown and crispy.', 'South Indian'),
        ('Upma', 'suji,mustard seeds,onion,peanuts,curry leaves,ginger,ghee', '1. Roast suji. 2. Heat ghee; sauté mustard, peanuts, onions, ginger. 3. Add boiling water (3:1 ratio). 4. Stir to avoid lumps and steam until fluffy.', 'South Indian'),
        ('Lemon Rice', 'cooked rice,lemon,turmeric,peanuts,mustard,curry leaves', '1. Temper oil with mustard, peanuts, turmeric. 2. Turn off heat; stir in fresh lemon juice. 3. Pour over cooled cooked rice and mix gently.', 'South Indian'),
        ('Appam', 'raw rice,coconut milk,yeast,sugar,salt', '1. Grind rice with coconut milk/yeast; ferment overnight. 2. Pour ladle into curved pan (Chatti) and swirl. 3. Cover and steam until edges are crispy and center is soft.', 'South Indian'),
        ('Ven Pongal', 'rice,moong dal,black pepper,cumin,ginger,ghee,cashews', '1. Cook rice and moong dal until mushy. 2. Heat ghee; fry cashews, peppercorns, cumin, and ginger. 3. Add tempering to rice-dal mix. 4. Serve hot.', 'South Indian'),
        ('Uttapam', 'dosa batter,onion,tomato,green chili,coriander,oil', '1. Pour thick ladle of batter on tawa. 2. Top with onions, tomatoes, chilies. 3. Drizzle oil and cook both sides until base is crisp.', 'South Indian'),
        ('Rasam', 'tamarind,tomato,black pepper,cumin,garlic,mustard', '1. Boil tamarind water with tomatoes. 2. Coarsely grind pepper, cumin, garlic. 3. Add ground spices to boiling water. 4. Temper with mustard/chilies. 5. Garnish with coriander.', 'South Indian'),
        ('Curd Rice', 'rice,curd,milk,mustard,ginger,curry leaves,pomegranate', '1. Overcook rice until very soft. 2. Mash and add milk/curd. 3. Temper with mustard, ginger, curry leaves. 4. Mix in fresh pomegranate seeds.', 'South Indian'),
        ('Paniyaram', 'idli batter,onion,mustard,chana dal,oil', '1. Sauté onions/dal; mix into batter. 2. Heat Paniyaram pan and grease holes. 3. Pour batter and cook until bottom is crisp. 4. Flip and cook other side.', 'South Indian'),
        ('Bisi Bele Bath', 'rice,tuar dal,mixed veggies,tamarind,special spice powder', '1. Cook rice, dal, and veggies together. 2. Mix tamarind pulp and special spice paste into the rice. 3. Temper with cashews fried in ghee.', 'South Indian'),
        ('Tomato Rice', 'rice,tomato,onion,garlic,cinnamon,cloves,mint', '1. Sauté whole spices, onions, and garlic. 2. Add plenty of tomatoes and cook until mushy. 3. Mix in cooked rice, salt, and mint.', 'South Indian'),
        ('Coconut Rice', 'rice,fresh coconut,urad dal,mustard,dry red chili', '1. Heat oil; sauté mustard, urad dal, and red chilies. 2. Add fresh grated coconut and sauté for 1 min. 3. Mix in cooked rice and salt.', 'South Indian'),
        ('Avial', 'yam,carrot,beans,drumstick,coconut,curd,coconut oil', '1. Boil veggies with turmeric. 2. Grind coconut, chilies, cumin to coarse paste. 3. Add paste and curd to veggies. 4. Finish with raw coconut oil and curry leaves.', 'South Indian'),
    # --- BLOCK 4: ITALIAN (13 UNIQUE RECIPES) ---
        ('Margherita Pizza', 'pizza dough,mozzarella,tomato sauce,basil', '1. Roll out dough. 2. Spread tomato sauce. 3. Top with fresh mozzarella. 4. Bake at high heat until crust is charred. 5. Garnish with fresh basil and olive oil.', 'Italian'),
        ('White Sauce Pasta', 'pasta,milk,butter,cheese,flour', '1. Boil pasta al dente. 2. Melt butter, add flour, and whisk in milk to make a roux. 3. Add plenty of cheese. 4. Toss pasta in the sauce and season with oregano.', 'Italian'),
        ('Arrabbiata Pasta', 'pasta,tomato,garlic,chili flakes,parsley', '1. Sauté garlic and chili flakes in olive oil. 2. Add crushed tomatoes and simmer. 3. Toss in boiled pasta. 4. Garnish with fresh parsley.', 'Italian'),
        ('Pesto Pasta', 'pasta,basil,walnuts,olive oil,cheese', '1. Blend basil, nuts, garlic, and oil into a paste. 2. Mix with grated cheese. 3. Toss with hot pasta and a splash of pasta water.', 'Italian'),
        ('Risotto', 'arborio rice,mushroom,butter,parmesan,garlic', '1. Sauté mushrooms and garlic. 2. Add rice and toast. 3. Add warm broth one ladle at a time, stirring until absorbed. 4. Finish with butter and parmesan.', 'Italian'),
        ('Lasagna', 'lasagna sheets,tomato sauce,cheese,meat,flour', '1. Layer pasta sheets with bolognese sauce and bechamel. 2. Top with mozzarella and parmesan. 3. Bake until bubbly and golden brown.', 'Italian'),
        ('Garlic Bread', 'bread,butter,garlic,oregano,chili flakes', '1. Mix softened butter with minced garlic and herbs. 2. Spread on bread slices. 3. Toast in oven or pan until golden and fragrant.', 'Italian'),
        ('Bruschetta', 'bread,tomato,garlic,olive oil,basil', '1. Toast bread slices. 2. Rub with raw garlic. 3. Top with a mixture of chopped tomatoes, basil, and olive oil.', 'Italian'),
        ('Minestrone', 'beans,carrot,celery,tomato,pasta,potato', '1. Sauté mirepoix (onion, carrot, celery). 2. Add broth, tomatoes, beans, and veggies. 3. Simmer until tender. 4. Add small pasta and cook until done.', 'Italian'),
        ('Focaccia', 'flour,olive oil,rosemary,sea salt,yeast', '1. Make a high-hydration dough. 2. Proof in a tray with plenty of oil. 3. Dimple with fingers, add rosemary and salt. 4. Bake until crispy.', 'Italian'),
        ('Tiramisu', 'biscuits,coffee,mascarpone,cocoa,sugar', '1. Dip ladyfingers in espresso. 2. Layer with a whipped mixture of mascarpone and sugar. 3. Dust with cocoa powder. 4. Chill for 4 hours.', 'Italian'),
        ('Gnocchi', 'potato,flour,egg,butter,sage', '1. Mash boiled potatoes and mix with flour/egg to make dough. 2. Roll into small ridges. 3. Boil until they float. 4. Toss in sage butter.', 'Italian'),
        ('Calzone', 'dough,cheese,tomato,ham,oregano', '1. Fill half of a pizza circle with toppings. 2. Fold over and seal edges. 3. Brush with oil and bake until puffed and golden.', 'Italian'),

        # --- BLOCK 5: PUNJABI (13 UNIQUE RECIPES) ---
        ('Butter Chicken', 'chicken,butter,cream,tomato puree,kasoori methi', '1. Grill marinated chicken. 2. Simmer in a rich tomato, butter, and cream gravy. 3. Add kasoori methi and honey for balance.', 'Punjabi'),
        ('Chole Bhature', 'chickpeas,maida,oil,curd,onion,spices', '1. Cook chickpeas with tea-bags and spices. 2. Make fermented maida dough. 3. Deep fry bhatures. 4. Serve with spicy chole and pickles.', 'Punjabi'),
        ('Dal Makhani', 'black lentil,kidney beans,butter,cream,garlic', '1. Soak lentils/beans overnight. 2. Slow cook with salt. 3. Temper with tomato and garlic. 4. Finish with a heavy hand of butter and cream.', 'Punjabi'),
        ('Paneer Tikka', 'paneer,yogurt,capsicum,onion,spices', '1. Marinate cubes in spiced yogurt. 2. Skewer with veggies. 3. Grill in a tandoor or oven until charred. 4. Serve with mint chutney.', 'Punjabi'),
        ('Aloo Paratha', 'wheat flour,potato,butter,green chili,ginger', '1. Stuff wheat dough with spicy mashed potatoes. 2. Roll out carefully. 3. Roast on tawa with ghee until crispy. 4. Serve with white butter.', 'Punjabi'),
        ('Sarson ka Saag', 'mustard leaves,spinach,butter,maize flour', '1. Boil greens and blend coarsely. 2. Cook with maize flour (makki atta). 3. Temper with garlic, ginger, and chilies. 4. Serve with extra butter.', 'Punjabi'),
        ('Makki di Roti', 'maize flour,ghee,warm water', '1. Knead maize flour with warm water. 2. Pat into a flatbread using hands or parchment. 3. Roast on tawa with ghee until firm and brown.', 'Punjabi'),
        ('Rajma Rice', 'kidney beans,rice,onion,tomato,ginger,garlic', '1. Pressure cook soaked rajma. 2. Sauté onion-tomato masala. 3. Simmer rajma in masala until thick. 4. Serve over steaming basmati rice.', 'Punjabi'),
        ('Kadai Paneer', 'paneer,capsicum,onion,tomato,coriander seeds', '1. Sauté paneer and veggies. 2. Add freshly ground kadai masala. 3. Simmer in a spicy tomato base until oil separates.', 'Punjabi'),
        ('Malai Kofta', 'paneer,potato,cream,cashew,tomato,raisins', '1. Make balls of paneer/potato; deep fry. 2. Prepare a sweet and creamy white or orange gravy. 3. Pour gravy over koftas just before serving.', 'Punjabi'),
        ('Lassi', 'curd,sugar,cardamom,ice,malai', '1. Whisk thick curd with sugar and cardamom. 2. Blend until frothy. 3. Serve chilled in a tall glass topped with a layer of malai.', 'Punjabi'),
        ('Chicken Tikka', 'chicken,yogurt,lemon,ginger,garlic,mustard oil', '1. Marinate chicken chunks in mustard oil and yogurt. 2. Grill until smoky. 3. Toss with butter and chaat masala.', 'Punjabi'),
        ('Shahi Paneer', 'paneer,cream,tomato,cashew,onion,saffron', '1. Make a smooth paste of boiled onions and cashews. 2. Cook with tomato and cream. 3. Add paneer cubes and saffron.', 'Punjabi'),

        # --- BLOCK 6: GUJARATI (13 UNIQUE RECIPES) ---
        ('Khaman Dhokla', 'besan,curd,mustard,oil,eno,sugar', '1. Make a smooth besan batter. 2. Add eno and steam immediately. 3. Pour a sweet-salty tempering of mustard and chilies over it.', 'Gujarati'),
        ('Thepla', 'wheat flour,methi,curd,turmeric,oil', '1. Mix flour with chopped methi and curd. 2. Roll into thin discs. 3. Roast on tawa with oil. Perfect for travel.', 'Gujarati'),
        ('Undhiyu', 'papdi,potato,brinjal,muthiya,oil,spices', '1. Sauté winter veggies and fried fenugreek dumplings (muthiya). 2. Slow cook with a special green masala until tender.', 'Gujarati'),
        ('Handvo', 'rice dal batter,bottle gourd,sesame,mustard', '1. Ferment rice-dal batter. 2. Mix with grated gourd and spices. 3. Bake or cook in a pan with a sesame-mustard tempering.', 'Gujarati'),
        ('Gujarati Kadhi', 'curd,besan,jaggery,ginger,cinnamon', '1. Whisk curd and besan. 2. Cook with ginger and chili. 3. Add jaggery for sweetness. 4. Temper with cinnamon and cloves.', 'Gujarati'),
        ('Fafda', 'besan,oil,papadsala,ajwain', '1. Stretch besan dough on a wooden board with your palm. 2. Deep fry until crispy. 3. Serve with fried chilies and papaya sambhara.', 'Gujarati'),
        ('Locho', 'chana dal,butter,sev,ginger,chili', '1. Steam a spicy chana dal batter. 2. Mash slightly while hot. 3. Top with a mountain of butter, sev, and locho masala.', 'Gujarati'),
        ('Dal Dhokli', 'tuar dal,wheat flour,peanuts,jaggery,kokum', '1. Cook spicy Gujarati dal. 2. Roll wheat dough thin, cut into diamonds, and drop into boiling dal. 3. Cook until dough is tender.', 'Gujarati'),
        ('Shrikhand', 'hung curd,sugar,saffron,pistachio,cardamom', '1. Drain curd in a muslin cloth overnight. 2. Mix thick "chakka" with powdered sugar and saffron. 3. Blend until smooth and silky.', 'Gujarati'),
        ('Sev Khamani', 'chana dal,garlic,sev,pomegranate,oil', '1. Crumble dhoklas. 2. Temper with garlic and chilies. 3. Garnish with lots of sev and pomegranate seeds.', 'Gujarati'),
        ('Muthiya', 'wheat flour,bottle gourd,ginger,sesame,oil', '1. Mix flour and grated gourd. 2. Steam the cylinders. 3. Slice and sauté with sesame seeds until crispy.', 'Gujarati'),
        ('Khakhra', 'wheat flour,oil,salt,methi,spices', '1. Roll wheat dough paper-thin. 2. Roast on a very low flame using a wooden press until completely crunchy.', 'Gujarati'),
        ('Patra', 'taro leaves,besan,jaggery,tamarind,sesame', '1. Spread spicy-sweet besan paste on taro leaves. 2. Roll, steam, and slice. 3. Sauté with sesame and mustard seeds.', 'Gujarati'),

        # --- BLOCK 7: ASIAN & GLOBAL (13 UNIQUE RECIPES) ---
        ('Maggi', 'maggi noodles,water,onion,peas,carrot', '1. Sauté veggies. 2. Add water and tastemaker. 3. Bring to boil, add noodles. 4. Cook for 2 mins until the sauce is thick.', 'Asian'),
        ('Veg Fried Rice', 'rice,carrot,soy sauce,beans,spring onion', '1. Sauté finely chopped veggies on high heat. 2. Add cold cooked rice. 3. Season with soy sauce, vinegar, and white pepper.', 'Asian'),
        ('Veg Chowmein', 'noodles,cabbage,carrot,soy sauce,vinegar', '1. Boil noodles. 2. Stir-fry julienned veggies. 3. Toss noodles with sauces and veggies on high flame.', 'Asian'),
        ('Manchurian', 'cabbage,garlic,ginger,soy sauce,cornflour', '1. Make fried cabbage balls. 2. Simmer in a thick, spicy soy-garlic gravy with spring onions.', 'Asian'),
        ('Spring Rolls', 'sheets,cabbage,carrot,capsicum,oil', '1. Sauté veggies. 2. Wrap in thin pastry sheets. 3. Deep fry until golden and serve with sweet chili sauce.', 'Asian'),
        ('Veg Burger', 'bun,patty,lettuce,cheese,mayo,tomato', '1. Toast buns. 2. Fry patty. 3. Layer mayo, lettuce, tomato, patty, and cheese. 4. Press together and serve.', 'Global'),
        ('Club Sandwich', 'bread,lettuce,tomato,cheese,mayo,butter', '1. Toast 3 bread slices. 2. Layer veggies and cheese between slices. 3. Secure with toothpicks and cut into triangles.', 'Global'),
        ('Omelette', 'egg,onion,chili,salt,pepper', '1. Whisk eggs. 2. Sauté onions/chilies. 3. Pour eggs and cook until set. 4. Fold and serve with toast.', 'Global'),
        ('French Fries', 'potato,oil,salt,peri peri', '1. Cut potatoes into sticks. 2. Soak in cold water. 3. Double fry for extra crispiness. 4. Season with salt immediately.', 'Global'),
        ('Pancakes', 'flour,milk,egg,syrup,butter', '1. Whisk batter until smooth. 2. Pour on a greased pan. 3. Flip when bubbles appear. 4. Serve with maple syrup and butter.', 'Global'),
        ('Tacos', 'shell,beans,cheese,salsa,lettuce', '1. Fill shells with warm beans. 2. Top with shredded lettuce, salsa, and plenty of cheese.', 'Global'),
        ('Fruit Salad', 'apple,banana,grapes,honey,lemon', '1. Chop fresh fruits. 2. Toss with a drizzle of honey and a squeeze of lemon to keep them fresh.', 'Global'),
        ('Pasta Salad', 'pasta,tomato,olives,dressing,cucumber', '1. Mix cold boiled pasta with chopped veggies. 2. Add Italian dressing and olives. 3. Toss well and serve chilled.', 'Global'),

        # --- BLOCK 8: SNACKS & SIDES (15 UNIQUE RECIPES) ---
        ('Cold Coffee', 'milk,coffee,sugar,ice,chocolate syrup', '1. Blend milk, coffee, and sugar with ice. 2. Drizzle syrup in glass. 3. Pour and serve frothy.', 'Global'),
        ('Lemonade', 'lemon,water,sugar,mint,black salt', '1. Mix lemon juice, sugar, and water. 2. Add a pinch of black salt and crushed mint. 3. Serve over ice.', 'Global'),
        ('Masala Tea', 'milk,tea,ginger,cardamom,cloves', '1. Boil water with crushed ginger and spices. 2. Add tea leaves and sugar. 3. Add milk and simmer until rich brown.', 'Global'),
        ('Corn Salad', 'corn,onion,lemon,salt,chaat masala', '1. Boil sweet corn. 2. Toss with chopped onions, lemon juice, and chaat masala.', 'Global'),
        ('Garlic Mushrooms', 'mushroom,garlic,butter,parsley', '1. Sauté sliced mushrooms in butter. 2. Add lots of minced garlic. 3. Garnish with parsley.', 'Global'),
        ('Stuffed Capsicum', 'capsicum,potato,spices,onion', '1. Hollow out bell peppers. 2. Stuff with spicy mashed potatoes. 3. Roast in a pan until the skin is charred.', 'Indian'),
        ('Bread Roll', 'bread,potato,oil,ginger', '1. Dip bread in water and squeeze. 2. Wrap around a spicy potato log. 3. Deep fry until golden and crunchy.', 'Indian'),
        ('Bhel Puri', 'puffed rice,onion,chutney,sev,papdi', '1. Mix puffed rice with chopped onions and boiled potatoes. 2. Add tangy tamarind and spicy mint chutneys. 3. Top with sev.', 'Indian'),
        ('Tomato Soup', 'tomato,cream,garlic,pepper,croutons', '1. Boil tomatoes and garlic; blend and strain. 2. Simmer with pepper and a splash of cream. 3. Serve with fried bread cubes.', 'Global'),
        ('Grilled Cheese', 'bread,butter,cheese,garlic powder', '1. Butter the outside of bread. 2. Place cheese between slices. 3. Grill until bread is toasted and cheese is gooey.', 'Global'),
        ('Sev Puri', 'puri,potato,onion,chutney,sev,mango', '1. Arrange flat puris. 2. Top with potato, onion, and chutneys. 3. Cover with a thick layer of sev.', 'Indian'),
        ('Dahi Puri', 'puri,curd,potato,tamarind chutney,sev', '1. Fill hollow puris with potato. 2. Pour sweetened curd and chutneys inside. 3. Garnish with sev and coriander.', 'Indian'),
        ('Papad Roast', 'papad,cumin,oil', '1. Roast papad directly on flame or fry in oil. 2. Sprinkle with red chili powder if desired.', 'Indian'),
        ('Veg Cutlet', 'potato,carrot,peas,bread crumbs,ginger', '1. Mash boiled veggies. 2. Shape into patties. 3. Coat in bread crumbs and shallow fry until crispy.', 'Indian'),
        ('Aloo Tikki', 'potato,ginger,chili,oil,cornflour', '1. Mix mashed potato with cornflour and spices. 2. Flatten into discs. 3. Shallow fry on a tawa until very crispy.', 'Indian')
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
    if not items:
        st.info("Pantry is empty, Boss!")
    else:
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
    st.info(f"BMI: {bmi} | Daily Intake: {int((10*w)+(6.25*h)-120)} kcal"
