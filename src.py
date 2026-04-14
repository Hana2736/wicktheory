import streamlit as st



# Standalone product list
PRODUCTS = [
    {"id": "afreshchapter_L",    "name": "A Fresh Chapter",       "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Smells like new beginnings."},
    {"id": "bahamabreeze_L",     "name": "Bahama Breeze",         "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Fruity and refreshing."},
    {"id": "chocolatelayer_L",   "name": "Chocolate Layer Cake",  "scent": "gourmet", "size": "L", "price": 29.99, "stock": 10, "description": "Delicious and indulgent."},
    {"id": "cleancotton_L",      "name": "Clean Cotton",          "scent": "earthy",  "size": "L", "price": 29.99, "stock": 10, "description": "Fresh and airy cotton scent."},
    {"id": "cocoadream_L",       "name": "Cocoa Dream",           "scent": "gourmet", "size": "L", "price": 29.99, "stock": 10, "description": "Rich and velvety chocolate aroma."},
    {"id": "coconutbeach_L",     "name": "Coconut Beach",         "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Tropical coconut escape."},
    {"id": "frenchvanilla_L",    "name": "French Vanilla",        "scent": "gourmet", "size": "L", "price": 29.99, "stock": 10, "description": "Classic warm vanilla fragrance."},
    {"id": "juicywatermelon_L",  "name": "Juicy Watermelon",      "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Sweet and vibrant watermelon scent."},
    {"id": "lemonlavender_L",    "name": "Lemon Lavender",        "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Citrus lemon softened with lavender."},
    {"id": "lilacblossom_L",     "name": "Lilac Blossom",         "scent": "floral",  "size": "L", "price": 29.99, "stock": 10, "description": "Soft blooming lilac fragrance."},
    {"id": "midsummersnight_L",  "name": "Midsummer's Night",     "scent": "earthy",  "size": "L", "price": 29.99, "stock": 10, "description": "Deep and mysterious evening scent."},
    {"id": "pinksands_L",        "name": "Pink Sands",            "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Soft tropical island breeze."},
    {"id": "sageandcitrus_L",    "name": "Sage and Citrus",       "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Herbal sage with bright citrus notes."},
    {"id": "saltedcaramel_L",    "name": "Salted Caramel",        "scent": "gourmet", "size": "L", "price": 29.99, "stock": 10, "description": "Sweet caramel with a touch of sea salt."},
    {"id": "sicilianlemon_L",    "name": "Sicilian Lemon",        "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Sharp and vibrant lemon zest."},
    {"id": "tangerinevanilla_L", "name": "Tangerine and Vanilla", "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Sweet tangerine blended with warm vanilla."},
    {"id": "cucumbermint_L",     "name": "Cucumber Mint Cooler",  "scent": "earthy",  "size": "L", "price": 29.99, "stock": 10, "description": "Refreshing cucumber and mint blend."},
    {"id": "lemonblueberry_L",   "name": "Lemon Blueberry Bliss", "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Bright lemon with sweet blueberry notes."},

    {"id": "applepumpkin_M",     "name": "Apple Pumpkin",         "scent": "gourmet", "size": "M", "price": 19.99, "stock": 10, "description": "Warm apple blended with spiced pumpkin."},
    {"id": "catchingrays_M",     "name": "Catching Rays",         "scent": "citrus",  "size": "M", "price": 19.99, "stock": 10, "description": "Bright sun-kissed citrus aroma."},
    {"id": "freshcutroses_M",    "name": "Fresh Cut Roses",       "scent": "floral",  "size": "M", "price": 19.99, "stock": 10, "description": "Classic blooming rose fragrance."},
    {"id": "greenapple_M",       "name": "Green Apple Sorbet",    "scent": "fruity",  "size": "M", "price": 19.99, "stock": 10, "description": "Sweet and tart green apple delight."},
    {"id": "honeyclementine_M",  "name": "Honey Clementine",      "scent": "citrus",  "size": "M", "price": 19.99, "stock": 10, "description": "Golden honey with juicy citrus notes."},
    {"id": "icedberry_M",        "name": "Iced Berry Lemonade",   "scent": "fruity",  "size": "M", "price": 19.99, "stock": 10, "description": "Chilled berries with zesty lemonade."},
    {"id": "juicywatermelon_M",  "name": "Juicy Watermelon",      "scent": "fruity",  "size": "M", "price": 19.99, "stock": 10, "description": "Sweet and vibrant watermelon scent."},
    {"id": "magicallights_M",    "name": "Magical Bright Lights", "scent": "floral",  "size": "M", "price": 19.99, "stock": 10, "description": "Vibrant sparkling festive fragrance."},
    {"id": "sparklingcinnamon_M","name": "Sparkling Cinnamon",    "scent": "gourmet", "size": "M", "price": 19.99, "stock": 10, "description": "Warm cinnamon with a sparkling twist."},
    {"id": "starfruitsun_M",     "name": "Starfruit & Sunshine",  "scent": "fruity",  "size": "M", "price": 19.99, "stock": 10, "description": "Exotic starfruit with bright citrus glow."},
    {"id": "vintagevelvet_M",    "name": "Vintage Velvet",        "scent": "earthy",  "size": "M", "price": 19.99, "stock": 10, "description": "Deep smooth luxurious fragrance."},

    {"id": "afreshchapter_S",    "name": "A Fresh Chapter",       "scent": "citrus",  "size": "S", "price": 9.99, "stock": 10, "description": "Smells like new beginnings."},
    {"id": "balsamcedar_S",      "name": "Balsam and Cedar",      "scent": "earthy",  "size": "S", "price": 9.99, "stock": 10, "description": "Warm balsam and cedar wood fragrance."},
    {"id": "freshcutroses_S",    "name": "Fresh Cut Roses",       "scent": "floral",  "size": "S", "price": 9.99, "stock": 10, "description": "Classic blooming rose fragrance."},
    {"id": "serenitystone_S",    "name": "Serenity Stone",        "scent": "earthy",  "size": "S", "price": 9.99, "stock": 10, "description": "Calming mineral and earthy tones."},
    {"id": "slowbloom_S",        "name": "Slow Bloom",            "scent": "floral",  "size": "S", "price": 9.99, "stock": 10, "description": "Delicate floral aroma unfolding slowly."},
    {"id": "springherbarium_S",  "name": "Spring Herbarium",      "scent": "earthy",  "size": "S", "price": 9.99, "stock": 10, "description": "Fresh spring herbs and greenery."},
    {"id": "wildflower_S",       "name": "Wildflower Breeze",     "scent": "floral",  "size": "S", "price": 9.99, "stock": 10, "description": "Light and airy wildflower scent."},
]


def search_products(products, query):
    if not query.strip():
        return products

    query = query.lower().strip()
    results = []

    for product in products:
        if (
            query in product["name"].lower()
            or query in product["scent"].lower()
            or query in product["size"].lower()
            or query in product["description"].lower()
        ):
            results.append(product)

    return results


def sort_products(products, sort_option):
    sorted_products = products.copy()

    if sort_option == "Price: Low to High":
        sorted_products.sort(key=lambda p: p["price"])

    elif sort_option == "Price: High to Low":
        sorted_products.sort(key=lambda p: p["price"], reverse=True)

    elif sort_option == "Name: A to Z":
        sorted_products.sort(key=lambda p: p["name"].lower())

    elif sort_option == "Name: Z to A":
        sorted_products.sort(key=lambda p: p["name"].lower(), reverse=True)

    elif sort_option == "Size: Small to Large":
        size_order = {"S": 1, "M": 2, "L": 3}
        sorted_products.sort(key=lambda p: size_order.get(p["size"], 99))

    elif sort_option == "Size: Large to Small":
        size_order = {"S": 1, "M": 2, "L": 3}
        sorted_products.sort(key=lambda p: size_order.get(p["size"], 99), reverse=True)

    return sorted_products




search_query = st.text_input("Search products", "")

sort_option = st.selectbox(
    "Sort by",
    [
        "Default",
        "Price: Low to High",
        "Price: High to Low",
        "Name: A to Z",
        "Name: Z to A",
        "Size: Small to Large",
        "Size: Large to Small",
    ],
)

filtered_products = search_products(PRODUCTS, search_query)
filtered_products = sort_products(filtered_products, sort_option)

st.write(f"Products found: {len(filtered_products)}")

if not filtered_products:
    st.warning("No matching products found.")
else:
    num_cols = 3

    for i in range(0, len(filtered_products), num_cols):
        cols = st.columns(num_cols)

        for j, product in enumerate(filtered_products[i:i+num_cols]):
            with cols[j]:
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        padding: 15px;
                        margin-bottom: 15px;
                        background-color: #f9f9f9;
                    ">
                        <h4>{product['name']}</h4>
                        <p><strong>Price:</strong> ${product['price']:.2f}</p>
                        <p><strong>Size:</strong> {product['size']}</p>
                        <p><strong>Scent:</strong> {product['scent'].title()}</p>
                        <p>{product['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )