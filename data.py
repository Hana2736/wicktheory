"""Shared product catalog for Wick Theory.

Values come from WickTheorySetUpScript.sql — the app runs in-memory so the
SQL file is the schema reference, not a live DB. Each entry points at an
image file under assets/images/YC{L,M,S}/.
"""

from pathlib import Path

ASSETS = Path(__file__).parent / "assets" / "images"


def _img(size_dir: str, filename: str) -> str:
    return str(ASSETS / size_dir / filename)


PRODUCTS = [
    # Large — $29.99
    {"id": "afreshchapter_L",    "name": "A Fresh Chapter",       "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Smells like new beginnings.",            "image": _img("YCL", "afreshchapter.jpg")},
    {"id": "bahamabreeze_L",     "name": "Bahama Breeze",         "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Fruity and refreshing.",                 "image": _img("YCL", "bahamabreeze.jpg")},
    {"id": "chocolatelayer_L",   "name": "Chocolate Layer Cake",  "scent": "gourmet", "size": "L", "price": 29.99, "stock": 10, "description": "Delicious and indulgent.",               "image": _img("YCL", "chocolatelayercake.jpg")},
    {"id": "cleancotton_L",      "name": "Clean Cotton",          "scent": "earthy",  "size": "L", "price": 29.99, "stock": 10, "description": "Fresh and airy cotton scent.",           "image": _img("YCL", "cleancotton.jpg")},
    {"id": "cocoadream_L",       "name": "Cocoa Dream",           "scent": "gourmet", "size": "L", "price": 29.99, "stock": 10, "description": "Rich and velvety chocolate aroma.",      "image": _img("YCL", "cocoadream.jpg")},
    {"id": "coconutbeach_L",     "name": "Coconut Beach",         "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Tropical coconut escape.",               "image": _img("YCL", "coconutbeach.jpg")},
    {"id": "frenchvanilla_L",    "name": "French Vanilla",        "scent": "gourmet", "size": "L", "price": 29.99, "stock": 10, "description": "Classic warm vanilla fragrance.",        "image": _img("YCL", "frenchvanilla.jpg")},
    {"id": "juicywatermelon_L",  "name": "Juicy Watermelon",      "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Sweet and vibrant watermelon scent.",    "image": _img("YCL", "juicywatermelon.jpg")},
    {"id": "lemonlavender_L",    "name": "Lemon Lavender",        "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Citrus lemon softened with lavender.",   "image": _img("YCL", "lemonlavender.jpg")},
    {"id": "lilacblossom_L",     "name": "Lilac Blossom",         "scent": "floral",  "size": "L", "price": 29.99, "stock": 10, "description": "Soft blooming lilac fragrance.",         "image": _img("YCL", "lilacblossom.jpg")},
    {"id": "midsummersnight_L",  "name": "Midsummer's Night",     "scent": "earthy",  "size": "L", "price": 29.99, "stock": 10, "description": "Deep and mysterious evening scent.",     "image": _img("YCL", "midsumer'snight.jpg")},
    {"id": "pinksands_L",        "name": "Pink Sands",            "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Soft tropical island breeze.",           "image": _img("YCL", "pinksands.jpg")},
    {"id": "sageandcitrus_L",    "name": "Sage and Citrus",       "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Herbal sage with bright citrus notes.",  "image": _img("YCL", "sageandcitrus.jpg")},
    {"id": "saltedcaramel_L",    "name": "Salted Caramel",        "scent": "gourmet", "size": "L", "price": 29.99, "stock": 10, "description": "Sweet caramel with a touch of sea salt.", "image": _img("YCL", "saltedcaramel.jpg")},
    {"id": "sicilianlemon_L",    "name": "Sicilian Lemon",        "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Sharp and vibrant lemon zest.",          "image": _img("YCL", "sicilianlemon.jpg")},
    {"id": "tangerinevanilla_L", "name": "Tangerine and Vanilla", "scent": "citrus",  "size": "L", "price": 29.99, "stock": 10, "description": "Sweet tangerine blended with warm vanilla.", "image": _img("YCL", "tangerineandvanilla.jpg")},
    {"id": "cucumbermint_L",     "name": "Cucumber Mint Cooler",  "scent": "earthy",  "size": "L", "price": 29.99, "stock": 10, "description": "Refreshing cucumber and mint blend.",    "image": _img("YCL", "cucumbermintcooler.jpg")},
    {"id": "lemonblueberry_L",   "name": "Lemon Blueberry Bliss", "scent": "fruity",  "size": "L", "price": 29.99, "stock": 10, "description": "Bright lemon with sweet blueberry notes.", "image": _img("YCL", "lemonblueberrybliss.jpg")},

    # Medium — $19.99
    {"id": "applepumpkin_M",     "name": "Apple Pumpkin",         "scent": "gourmet", "size": "M", "price": 19.99, "stock": 10, "description": "Warm apple blended with spiced pumpkin.", "image": _img("YCM", "applepumpkinM.jpg")},
    {"id": "catchingrays_M",     "name": "Catching Rays",         "scent": "citrus",  "size": "M", "price": 19.99, "stock": 10, "description": "Bright sun-kissed citrus aroma.",        "image": _img("YCM", "catchingraysM.jpg")},
    {"id": "freshcutroses_M",    "name": "Fresh Cut Roses",       "scent": "floral",  "size": "M", "price": 19.99, "stock": 10, "description": "Classic blooming rose fragrance.",       "image": _img("YCM", "freshcutrosesM.jpg")},
    {"id": "greenapple_M",       "name": "Green Apple Sorbet",    "scent": "fruity",  "size": "M", "price": 19.99, "stock": 10, "description": "Sweet and tart green apple delight.",    "image": _img("YCM", "greenapplesorbetM.jpg")},
    {"id": "honeyclementine_M",  "name": "Honey Clementine",      "scent": "citrus",  "size": "M", "price": 19.99, "stock": 10, "description": "Golden honey with juicy citrus notes.",  "image": _img("YCM", "honeyclementineM.jpg")},
    {"id": "icedberry_M",        "name": "Iced Berry Lemonade",   "scent": "fruity",  "size": "M", "price": 19.99, "stock": 10, "description": "Chilled berries with zesty lemonade.",   "image": _img("YCM", "icedberrylemonadeM.jpg")},
    {"id": "juicywatermelon_M",  "name": "Juicy Watermelon",      "scent": "fruity",  "size": "M", "price": 19.99, "stock": 10, "description": "Sweet and vibrant watermelon scent.",    "image": _img("YCM", "juicywatermelonM.jpg")},
    {"id": "magicallights_M",    "name": "Magical Bright Lights", "scent": "floral",  "size": "M", "price": 19.99, "stock": 10, "description": "Vibrant sparkling festive fragrance.",   "image": _img("YCM", "magicalbrightlightsM.jpg")},
    {"id": "sparklingcinnamon_M","name": "Sparkling Cinnamon",    "scent": "gourmet", "size": "M", "price": 19.99, "stock": 10, "description": "Warm cinnamon with a sparkling twist.",  "image": _img("YCM", "sparklingcinnamon.jpg")},
    {"id": "starfruitsun_M",     "name": "Starfruit & Sunshine",  "scent": "fruity",  "size": "M", "price": 19.99, "stock": 10, "description": "Exotic starfruit with bright citrus glow.", "image": _img("YCM", "starfruitsunshineM.jpg")},
    {"id": "vintagevelvet_M",    "name": "Vintage Velvet",        "scent": "earthy",  "size": "M", "price": 19.99, "stock": 10, "description": "Deep smooth luxurious fragrance.",       "image": _img("YCM", "vintagevelvetM.jpg")},

    # Small — $9.99
    {"id": "afreshchapter_S",    "name": "A Fresh Chapter",       "scent": "citrus",  "size": "S", "price": 9.99, "stock": 10, "description": "Smells like new beginnings.",             "image": _img("YCS", "afreshchapterS.jpg")},
    {"id": "balsamcedar_S",      "name": "Balsam and Cedar",      "scent": "earthy",  "size": "S", "price": 9.99, "stock": 10, "description": "Warm balsam and cedar wood fragrance.",   "image": _img("YCS", "balsamandcedarS.jpg")},
    {"id": "freshcutroses_S",    "name": "Fresh Cut Roses",       "scent": "floral",  "size": "S", "price": 9.99, "stock": 10, "description": "Classic blooming rose fragrance.",        "image": _img("YCS", "freshcutrosesS.jpg")},
    {"id": "serenitystone_S",    "name": "Serenity Stone",        "scent": "earthy",  "size": "S", "price": 9.99, "stock": 10, "description": "Calming mineral and earthy tones.",       "image": _img("YCS", "serenitystoneS.jpg")},
    {"id": "slowbloom_S",        "name": "Slow Bloom",            "scent": "floral",  "size": "S", "price": 9.99, "stock": 10, "description": "Delicate floral aroma unfolding slowly.", "image": _img("YCS", "slowbloomS.jpg")},
    {"id": "springherbarium_S",  "name": "Spring Herbarium",      "scent": "earthy",  "size": "S", "price": 9.99, "stock": 10, "description": "Fresh spring herbs and greenery.",        "image": _img("YCS", "springherbariumS.jpg")},
    {"id": "wildflower_S",       "name": "Wildflower Breeze",     "scent": "floral",  "size": "S", "price": 9.99, "stock": 10, "description": "Light and airy wildflower scent.",        "image": _img("YCS", "wildflowerbreezeS.jpg")},
]

SIZE_LABELS = {"L": "Large (10 oz)", "M": "Medium (8 oz)", "S": "Small (4 oz)"}


STATE_TAX_RATES = {
    "Alabama": 0.04, "Alaska": 0.00, "Arizona": 0.056, "Arkansas": 0.065,
    "California": 0.0725, "Colorado": 0.029, "Connecticut": 0.0635, "Delaware": 0.00,
    "Florida": 0.06, "Georgia": 0.04, "Hawaii": 0.04, "Idaho": 0.06,
    "Illinois": 0.0625, "Indiana": 0.07, "Iowa": 0.06, "Kansas": 0.065,
    "Kentucky": 0.06, "Louisiana": 0.0445, "Maine": 0.055, "Maryland": 0.06,
    "Massachusetts": 0.0625, "Michigan": 0.06, "Minnesota": 0.06875, "Mississippi": 0.07,
    "Missouri": 0.04225, "Montana": 0.00, "Nebraska": 0.055, "Nevada": 0.0685,
    "New Hampshire": 0.00, "New Jersey": 0.06625, "New Mexico": 0.05125, "New York": 0.04,
    "North Carolina": 0.0475, "North Dakota": 0.05, "Ohio": 0.0575, "Oklahoma": 0.045,
    "Oregon": 0.00, "Pennsylvania": 0.06, "Rhode Island": 0.07, "South Carolina": 0.06,
    "South Dakota": 0.042, "Tennessee": 0.07, "Texas": 0.0625, "Utah": 0.061,
    "Vermont": 0.06, "Virginia": 0.053, "Washington": 0.065, "West Virginia": 0.06,
    "Wisconsin": 0.05, "Wyoming": 0.04, "Washington, D.C.": 0.06,
}

SHIPPING_OPTIONS = {
    "Standard (5-7 days)": 6.99,
    "Express (2-3 days)": 12.99,
    "Free pickup": 0.00,
}

DISCOUNT_CODES = {
    "WELCOME10": 0.10,
    "CANDLE20":  0.20,
    "FREESHIP":  0.00,  # handled specially in cart
}


def get_product(product_id: str):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def money(amount: float) -> str:
    return f"${amount:,.2f}"
