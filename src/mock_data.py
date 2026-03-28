from config import settings

def img(path: str) -> str:
    return f"{settings.base_url}/images/{path}"

FEED_POSTS = [
    {
        "id": "1",
        "photoUrl": img("mockimages/1.png"),
        "cuisine": "gb",
        "user": {
            "id": "u1",
            "displayName": "grep 🍇",
            "username": "putao_doggo",
            "avatarUrl": img("mockprofilepics/grep.png"),
        },
        "date": "February 7th",
        "caption": "very dirty latte for my runner bf <3",
        "timeAgo": "2 mins ago",
        "ingredients": {"vessel": "mug", "base": "espresso", "toppings": ["milk foam", "latte art"]},
        "spriteColors": {"bg": "#C4956A", "accent": "#8B5E3C"},
        "isHot": True,
    },
    {
        "id": "2",
        "photoUrl": img("mockimages/2.png"),
        "cuisine": "kr",
        "user": {
            "id": "u2",
            "displayName": "hyems",
            "username": "heymin",
            "avatarUrl": img("mockprofilepics/hyems.png"),
        },
        "date": "February 6th",
        "caption": "sundubu jjigae for the soul",
        "timeAgo": "1 day ago",
        "ingredients": {"vessel": "bowl", "base": "tofu", "toppings": ["kimchi", "egg", "green onion"]},
        "spriteColors": {"bg": "#E8604C", "accent": "#C0392B"},
        "isHot": True,
    },
    {
        "id": "3",
        "photoUrl": img("mockimages/3.png"),
        "cuisine": "tw",
        "user": {
            "id": "u3",
            "displayName": "Leo Chang",
            "username": "secondapron",
            "avatarUrl": img("mockprofilepics/leo.png"),
        },
        "date": "February 5th",
        "caption": "luroufan from scratch, 4 hour braise 🤤",
        "timeAgo": "2 days ago",
        "ingredients": {"vessel": "bowl", "base": "rice", "toppings": ["braised pork", "egg", "pickled radish"]},
        "spriteColors": {"bg": "#8B5E3C", "accent": "#F0C27F"},
        "isHot": False,
    },
]

RECIPES = [
    {"id": "r1",  "cuisine": "tw", "name": "LUROUFAN",                     "creatorColor": "#5A6E7F", "creatorUsername": "secondapron", "creatorAvatarUrl": img("mockprofilepics/leo.png"),   "lastMade": "2 days ago",      "ingredients": ["pork belly", "soy sauce", "five spice", "rice", "egg"], "notes": "Braise the pork for at least 3 hours on low heat. The fat should be melt-in-your-mouth. Serve over steamed white rice with a soft-boiled soy egg."},
    {"id": "r2",  "cuisine": "cn", "name": "CANTONESE STEAMED CHICKEN",    "creatorColor": "#8B6F47", "creatorUsername": "heymin",       "creatorAvatarUrl": img("mockprofilepics/hyems.png"), "lastMade": "Jan 20th, 2026",  "ingredients": ["whole chicken", "ginger", "spring onion", "soy sauce", "sesame oil"], "notes": "Steam for 20 min then rest 10 min before cutting. Use the steaming juices as a sauce base."},
    {"id": "r3",  "cuisine": "tw", "name": "BEEF NOODLE SOUP",              "creatorColor": "#6B8CAE", "creatorUsername": "putao_doggo",  "creatorAvatarUrl": img("mockprofilepics/grep.png"),  "lastMade": "Dec 4th, 2025",   "ingredients": ["beef shank", "noodles", "doubanjiang", "tomato", "star anise", "soy sauce"], "notes": ""},
    {"id": "r4",  "cuisine": "mx", "name": "BREAKFAST BURRITOS",            "creatorColor": "#C0392B", "creatorUsername": "heymin",       "creatorAvatarUrl": img("mockprofilepics/hyems.png"), "lastMade": "5 days ago",      "ingredients": ["flour tortilla", "eggs", "cheddar", "salsa", "black beans", "avocado"], "notes": "Scramble eggs low and slow. Warm tortilla on dry pan before filling."},
    {"id": "r5",  "cuisine": "cn", "name": "DUCK WITH PLUM SAUCE",          "creatorColor": "#5A6E7F", "creatorUsername": "secondapron", "creatorAvatarUrl": img("mockprofilepics/leo.png"),   "lastMade": "Dec 25th, 2025",  "ingredients": ["duck legs", "plums", "star anise", "honey", "rice vinegar"], "notes": ""},
    {"id": "r6",  "cuisine": "tw", "name": "CENTURY EGG PESTO TOFU",        "creatorColor": "#8B5E3C", "creatorUsername": "putao_doggo",  "creatorAvatarUrl": img("mockprofilepics/grep.png"),  "lastMade": "Jan 2nd, 2025",   "ingredients": ["silken tofu", "century egg", "basil pesto", "spring onion", "sesame oil"], "notes": "A fusion experiment. Chill everything before plating."},
    {"id": "r7",  "cuisine": "cn", "name": "PENG'S SPECIAL TOMATO AND EGG", "creatorColor": "#6B5B95", "creatorUsername": "heymin",       "creatorAvatarUrl": img("mockprofilepics/hyems.png"), "lastMade": None,              "ingredients": ["tomatoes", "eggs", "spring onion", "sugar", "soy sauce"], "notes": ""},
    {"id": "r8",  "cuisine": "es", "name": "BURNT BASQUE CHEESECAKE",       "creatorColor": "#8B6F47", "creatorUsername": "secondapron", "creatorAvatarUrl": img("mockprofilepics/leo.png"),   "lastMade": "3 days ago",      "ingredients": ["cream cheese", "eggs", "heavy cream", "sugar", "flour"], "notes": "Bake at 220°C for 50 min. It should look burnt on top — that is correct."},
    {"id": "r9",  "cuisine": "gb", "name": "COFFEE WALNUT LOAF",            "creatorColor": "#5A6E7F", "creatorUsername": "putao_doggo",  "creatorAvatarUrl": img("mockprofilepics/grep.png"),  "lastMade": None,              "ingredients": ["flour", "walnuts", "espresso", "butter", "brown sugar", "eggs"], "notes": ""},
    {"id": "r10", "cuisine": "us", "name": "RICE KRISPIES",                 "creatorColor": "#6B8CAE", "creatorUsername": "heymin",       "creatorAvatarUrl": img("mockprofilepics/hyems.png"), "lastMade": None,              "ingredients": ["rice krispies", "butter", "marshmallows"], "notes": "Melt butter and marshmallows over low heat, fold in cereal, press into tin and cool."},
    {"id": "r11", "cuisine": "jp", "name": "TOFU CREAM UDON",               "creatorColor": "#5A6E7F", "creatorUsername": "secondapron", "creatorAvatarUrl": img("mockprofilepics/leo.png"),   "lastMade": "Dec 19th, 2025",  "ingredients": ["udon noodles", "silken tofu", "dashi", "mirin", "soy sauce", "spring onion"], "notes": ""},
    {"id": "r12", "cuisine": "ae", "name": "DUBAI CHOCOLATE",               "creatorColor": "#C0392B", "creatorUsername": "heymin",       "creatorAvatarUrl": img("mockprofilepics/hyems.png"), "lastMade": None,              "ingredients": ["dark chocolate", "kadayif", "pistachio paste", "tahini", "butter"], "notes": "Toast the kadayif until golden. Mix with pistachio paste while warm."},
    {"id": "r13", "cuisine": "fr", "name": "SOURDOUGH",                     "creatorColor": "#8B6F47", "creatorUsername": "putao_doggo",  "creatorAvatarUrl": img("mockprofilepics/grep.png"),  "lastMade": "Jan 2nd, 2025",   "ingredients": ["bread flour", "sourdough starter", "water", "salt"], "notes": "75% hydration. Bulk ferment 4h at room temp, shape, cold proof overnight, bake in dutch oven."},
    {"id": "r14", "cuisine": "it", "name": "CIABATTA",                      "creatorColor": "#6B8CAE", "creatorUsername": "putao_doggo",  "creatorAvatarUrl": img("mockprofilepics/grep.png"),  "lastMade": None,              "ingredients": ["bread flour", "yeast", "olive oil", "water", "salt"], "notes": ""},
]

def _get_recipe(recipe_id):
    return next((r for r in RECIPES if r["id"] == recipe_id), None)

PROFILE = {
    "displayName": "Leo Chang",
    "username": "secondapron",
    "avatarUrl": img("mockprofilepics/leo.png"),
    "stats": {
        "recipesShared": 3,
        "dishesLogged": 39,
        "badgesObtained": 4,
        "weekStreak": 2,
    },
    "pinnedDishes": [
        {"id": "d1", "bg": "#6B5B95", "imageUrl": img("mockfood/bento.png"),  "name": "Bento Box",   "cuisine": "jp", "ingredients": ["rice", "tamagoyaki", "karaage", "edamame", "pickled ginger"], "recipe": None},
        {"id": "d2", "bg": "#C0392B", "imageUrl": img("mockfood/congee.png"), "name": "Congee",      "cuisine": "cn", "ingredients": ["jasmine rice", "ginger", "spring onion", "century egg", "sesame oil"], "recipe": None},
        {"id": "d3", "bg": "#F8C8D4", "imageUrl": img("mockfood/cake.png"),   "name": "Basque Cake", "cuisine": "es", "ingredients": ["cream cheese", "eggs", "heavy cream", "sugar", "flour"], "recipe": _get_recipe("r8")},
    ],
    "ingredientData": [
        {"emoji": "🧅", "label": "Green Onion", "pct": 0.48},
        {"emoji": "🧄", "label": "Garlic",      "pct": 0.31},
        {"emoji": "🫚", "label": "Sesame Oil",  "pct": 0.21},
    ],
    "cuisineData": [
        {"label": "Taiwanese",  "countryCode": "tw", "pct": 0.55},
        {"label": "Korean",     "countryCode": "kr", "pct": 0.30},
        {"label": "Other",      "countryCode": "xx", "pct": 0.15},
    ],
}

DIARY = {
    "month": "February 2026",
    "year": 2026,
    "monthIndex": 1,
    "loggedDays": [
        {"day": 2,  "photoUrl": None,                       "caption": None},
        {"day": 3,  "photoUrl": None,                       "caption": None},
        {"day": 4,  "photoUrl": None,                       "caption": None},
        {"day": 7,  "photoUrl": img("mockimages/3.png"),    "caption": "luroufan from scratch, 4 hour braise 🤤"},
        {"day": 8,  "photoUrl": None,                       "caption": None},
        {"day": 9,  "photoUrl": img("mockimages/2.png"),    "caption": "sundubu jjigae for the soul"},
        {"day": 10, "photoUrl": None,                       "caption": None},
        {"day": 11, "photoUrl": img("mockimages/1.png"),    "caption": "very dirty latte for my runner bf <3"},
    ],
    "stats": {
        "recipesShared": 3,
        "dishesLogged": 39,
        "newRecipes": 2,
        "challengeRecipes": 5,
        "dayStreak": 4,
    },
    "challengeTitle": "Lunar New Year",
    "challengeDetail": {
        "title": "Lunar New Year Challenge",
        "description": "Cook traditional Lunar New Year dishes throughout February. Focus on symbolic ingredients that bring luck, prosperity, and reunion.",
        "ingredients": [
            {"label": "Spring Onion", "imageKey": "spring_onion"},
            {"label": "Cauliflower",  "imageKey": "cauliflower"},
            {"label": "Citrus Fruit", "imageKey": "citrusfruit"},
        ],
        "featuredRecipes": ["LUROUFAN", "CANTONESE STEAMED CHICKEN", "DUCK WITH PLUM SAUCE"],
    },
    "lanternProgress": {"filled": 6, "total": 10, "mealsUntilBadge": 4},
    "dishesThisWeek": [
        {"id": "w1", "bg": "#2C1810", "imageUrl": img("mockfood/ramen.png"), "name": "Beef Noodle Soup", "cuisine": "tw", "ingredients": ["beef shank", "noodles", "doubanjiang", "star anise", "soy sauce"], "recipe": _get_recipe("r3")},
        {"id": "w2", "bg": "#4A3B6B", "imageUrl": img("mockfood/rice.png"),  "name": "Luroufan",         "cuisine": "tw", "ingredients": ["pork belly", "soy sauce", "five spice", "rice", "egg"], "recipe": _get_recipe("r1")},
        {"id": "w3", "bg": "#8B6F47", "imageUrl": img("mockfood/pie.png"),   "name": "Apple Pie",        "cuisine": "gb", "ingredients": ["shortcrust pastry", "apple", "cinnamon", "butter", "brown sugar"], "recipe": None},
        {"id": "w4", "bg": "#E8D5B7", "imageUrl": None, "name": None, "cuisine": None, "ingredients": [], "recipe": None},
        {"id": "w5", "bg": "#E8E4E0", "imageUrl": None, "name": None, "cuisine": None, "ingredients": [], "recipe": None},
        {"id": "w6", "bg": "#E8E4E0", "imageUrl": None, "name": None, "cuisine": None, "ingredients": [], "recipe": None},
    ],
}

CURRENT_EVENT = {
    "title": DIARY["challengeTitle"],
    "detail": DIARY["challengeDetail"],
    "lanternProgress": DIARY["lanternProgress"],
}
