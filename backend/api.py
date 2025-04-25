from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Data - The 39 Melachot organized by categories
melachot = [
    # Category 1: Field Work
    {
        "id": 1,
        "name": "Choresh (Plowing)",
        "hebrew": "חורש",
        "category": "Field Work",
        "description": "Breaking or loosening the ground",
        "examples": ["Digging", "Rototilling the garden", "Aerating the lawn"],
        "keywords": [
            "digging", "gardening", "landscaping", "raking", "yard work", "tilling soil",
            "excavating", "shoveling", "aerating lawn", "breaking ground", "potting soil",
            "planting preparation", "garden beds", "turning compost", "landscaping",
            "ground preparation", "sandbox digging", "hole drilling", "construction digging",
            "preparing flower beds", "golf divots", "sandboxes", "children digging"
        ]
    },
    {
        "id": 2,
        "name": "Zore'a (Sowing)",
        "hebrew": "זורע",
        "category": "Field Work",
        "description": "Planting seeds or causing plants to grow",
        "examples": ["Planting trees", "Watering plants", "Starting a garden"],
        "keywords": [
            "gardening", "watering plants", "planting", "hydroponics", "growing herbs", 
            "sprouting seeds", "fertilizing", "indoor gardening", "flower pots", 
            "microgreens", "plant cuttings", "repotting", "vegetable garden", "window herbs", 
            "seed starting", "misting plants", "watering lawn", "composting", "seedlings", 
            "houseplants", "rooting plants", "plant propagation", "plant maintenance",
            "grass watering", "flower arranging"
        ]
    },
    {
        "id": 3,
        "name": "Kotzer (Reaping)",
        "hebrew": "קוצר",
        "category": "Field Work",
        "description": "Cutting or plucking growing things",
        "examples": ["Picking fruits", "Mowing grass", "Cutting flowers"],
        "keywords": [
            "mowing lawn", "trimming plants", "cutting flowers", "pruning", "harvesting",
            "picking fruit", "grass cutting", "tree trimming", "deadheading plants", 
            "harvesting vegetables", "cutting herbs", "picking berries", "leaf removal", 
            "weeding garden", "plucking fruit", "garden scissors", "pruning shears", 
            "hedge trimming", "flower arrangement", "cutting stems", "picking tomatoes", 
            "apple picking", "leaf collection", "weed removal", "haircuts", "shaving", "nail cutting"
        ]
    },
    {
        "id": 4,
        "name": "Me'amer (Gathering)",
        "hebrew": "מעמר",
        "category": "Field Work",
        "description": "Collecting or gathering scattered growing things",
        "examples": ["Gathering fallen fruits", "Bundling flowers", "Collecting vegetables"],
        "keywords": [
            "collecting", "picking up produce", "gathering leaves", "foraging", "harvesting",
            "leaf raking", "picking up fallen fruit", "collecting nuts", "gathering vegetables", 
            "collecting herbs", "berry foraging", "mushroom hunting", "collecting wildflowers", 
            "apple gathering", "grocery shopping", "organizing produce", "organizing items",
            "filing paperwork", "collecting mail", "organizing office", "collecting eggs",
            "gathering kindling", "laundry collection", "sorting objects", "collecting recyclables"
        ]
    },
    {
        "id": 5,
        "name": "Dash (Threshing)",
        "hebrew": "דש",
        "category": "Field Work",
        "description": "Extracting food from its natural shell or husk",
        "examples": ["Removing kernels from husks", "Shelling nuts", "Peeling fruits"],
        "keywords": [
            "peeling", "shelling nuts", "opening packages", "husking corn", "cracking shells",
            "peeling oranges", "opening nuts", "removing seeds", "peeling vegetables", 
            "opening coconuts", "shelling pistachios", "cracking walnuts", "shucking oysters", 
            "unboxing items", "removing plastic wrap", "breaking seals", "peeling bananas", 
            "removing egg shells", "opening food packages", "pill packaging", "bubble wrap",
            "amazon packages", "food preparation", "opening letters", "snack preparation"
        ]
    },
    {
        "id": 6,
        "name": "Zoreh (Winnowing)",
        "hebrew": "זורה",
        "category": "Field Work",
        "description": "Separating food from inedible parts using wind",
        "examples": ["Blowing on food to remove unwanted parts", "Fanning grain"],
        "keywords": [
            "blowing dust", "using fans", "air purifier", "blowing crumbs", "air drying",
            "blow dryer", "drying with fan", "blowing off debris", "cooling hot food", 
            "blowing on soup", "air conditioning", "vacuum cleaner", "leaf blower", 
            "dust removal", "hair drying", "blowing out candles", "exhaust fan", 
            "drying hands", "compressed air", "cleaning keyboard", "dusting furniture",
            "cooling down drinks", "wind machines", "ventilation", "air circulation"
        ]
    },
    {
        "id": 7,
        "name": "Borer (Selecting/Sorting)",
        "hebrew": "בורר",
        "category": "Field Work",
        "description": "Separating mixed materials, selecting the desirable from the undesirable",
        "examples": ["Sorting silverware", "Removing stones from rice", "Filtering water"],
        "keywords": [
            "sorting", "organizing", "separating", "filtering", "removing unwanted items",
            "sorting laundry", "sorting silverware", "separating recycling", "filtering coffee", 
            "removing bad produce", "email sorting", "organizing folders", "digital organizing", 
            "separating laundry", "removing debris", "filtering water", "straining pasta",
            "separating food", "junk mail sorting", "organizing closet", "color sorting", 
            "categorization", "selecting clothing", "grocery selection", "removing stains"
        ]
    },
    {
        "id": 8,
        "name": "Tochen (Grinding)",
        "hebrew": "טוחן",
        "category": "Field Work",
        "description": "Grinding or milling substances into small pieces or powder",
        "examples": ["Grinding coffee beans", "Using a food processor", "Crushing herbs"],
        "keywords": [
            "grinding coffee", "food processor", "blender", "crushing pills", "grating cheese",
            "milling flour", "spice grinding", "crushing ice", "pureeing food", "smoothie making",
            "chopping vegetables", "grating vegetables", "crushing garlic", "juicing fruits",
            "nutribullet", "meat grinding", "herb chopping", "pepper mill", "salt grinder",
            "electric grinder", "mortar and pestle", "vegetable chopper", "food preparation",
            "crushing nuts", "grinding spices", "cutting board use"
        ]
    },
    {
        "id": 9,
        "name": "Merakeid (Sifting)",
        "hebrew": "מרקד",
        "category": "Field Work",
        "description": "Sifting or straining materials",
        "examples": ["Sifting flour", "Straining tea", "Using a colander for pasta"],
        "keywords": [
            "sifting flour", "straining", "filtering", "colander", "sieve", "pasta straining",
            "tea strainer", "filter coffee", "water filtering", "juice straining", "sifter",
            "dust filtering", "air filters", "draining vegetables", "straining sauces", 
            "mesh screens", "oil filters", "dust mask", "straining soup", "pulp removal",
            "water purifier", "draining cans", "draining sink", "pool filters", "aquarium filters",
            "straining yogurt"
        ]
    },
    {
        "id": 10,
        "name": "Lash (Kneading)",
        "hebrew": "לש",
        "category": "Field Work",
        "description": "Combining solids and liquids to form a paste or dough",
        "examples": ["Kneading bread dough", "Mixing cement", "Making clay"],
        "keywords": [
            "mixing batter", "kneading dough", "bread making", "pizza dough", "cake mixing",
            "combining ingredients", "mixing cement", "clay molding", "cookie dough", "playdough",
            "mixing paint", "preparing mortar", "mixing salad dressing", "mixing concrete",
            "stirring sauce", "making mud", "mixing drinks", "putty preparation", "making batter",
            "stirring yogurt", "mixing oatmeal", "preparing mashed potatoes", "mixing smoothies",
            "salad tossing", "mixing guacamole"
        ]
    },
    {
        "id": 11,
        "name": "Ofeh/Bishul (Baking/Cooking)",
        "hebrew": "אופה/בישול",
        "category": "Field Work",
        "description": "Changing a substance through heat",
        "examples": ["Baking bread", "Cooking on a stove", "Using a microwave"],
        "keywords": [
            "cooking", "baking", "boiling", "frying", "roasting", "microwave heating",
            "oven use", "toaster", "air fryer", "grilling", "heating food", "slow cooker",
            "pressure cooker", "steaming", "brewing coffee", "tea preparation", "poaching",
            "sous vide", "hot plate", "warming tray", "toaster oven", "crock pot", "water boiling",
            "sautéing", "melting chocolate", "heating soup", "reheating leftovers", "stove use",
            "barbecuing", "rice cooker", "food warming"
        ]
    },
    
    # Category 2: Making Material Curtains
    {
        "id": 12,
        "name": "Gozez (Shearing)",
        "hebrew": "גוזז",
        "category": "Making Material Curtains",
        "description": "Removing hair, wool, or feathers from a living creature",
        "examples": ["Cutting hair", "Shaving", "Plucking feathers"],
        "keywords": [
            "haircut", "shaving", "plucking", "trimming beard", "cutting nails", "waxing",
            "eyebrow threading", "hair removal", "hair trimming", "animal grooming", "dog grooming",
            "facial hair removal", "cutting children's hair", "body hair removal", "salon haircuts", 
            "trimming mustache", "nail clipping", "pet grooming", "wool shearing", "feather plucking",
            "laser hair removal", "threading", "tweezing", "eyebrow plucking", "home haircuts",
            "barber visits"
        ]
    },
    {
        "id": 13,
        "name": "Melaben (Whitening/Cleaning)",
        "hebrew": "מלבן",
        "category": "Making Material Curtains",
        "description": "Cleansing items to remove dirt or stains",
        "examples": ["Washing clothes", "Dry cleaning", "Scrubbing dishes"],
        "keywords": [
            "laundry", "washing clothes", "dry cleaning", "stain removal", "bleaching", 
            "dishwasher", "washing dishes", "scrubbing", "cleaning surfaces", "mopping floors", 
            "polishing silver", "cleaning shoes", "washing windows", "car washing", "pressure washing", 
            "carpet cleaning", "linen washing", "washing bathroom", "cleaning kitchen", "polishing",
            "shower cleaning", "sink cleaning", "toilet cleaning", "sanitizing", "disinfecting",
            "washing hands", "face washing", "bathing", "showering"
        ]
    },
    {
        "id": 14,
        "name": "Menafetz (Combing/Carding)",
        "hebrew": "מנפץ",
        "category": "Making Material Curtains",
        "description": "Separating and straightening fibers",
        "examples": ["Combing wool", "Brushing hair", "Carding cotton"],
        "keywords": [
            "combing hair", "brushing", "detangling", "straightening hair", "brushing pet fur",
            "lint roller", "wool carding", "fiber preparation", "cotton carding", "hair styling",
            "using hairbrush", "detangling hair", "untangling yarn", "preparing fibers",
            "fiber separation", "hair care", "hair brushing", "beard combing", "wig care",
            "hair detangling", "pet grooming", "wool preparation", "preparing fabric",
            "smoothing fibers", "detangling wigs"
        ]
    },
    {
        "id": 15,
        "name": "Tzove'a (Dyeing)",
        "hebrew": "צובע",
        "category": "Making Material Curtains",
        "description": "Changing or enhancing the color of an item",
        "examples": ["Dyeing fabric", "Applying makeup", "Painting walls"],
        "keywords": [
            "dyeing", "coloring", "painting", "makeup application", "hair dye", "nail polish",
            "food coloring", "painting walls", "staining wood", "art painting", "coloring books",
            "highlighting hair", "eyeshadow", "lipstick", "foundation makeup", "blush application",
            "eyeliner", "coloring eggs", "tie-dye", "fabric dyeing", "watercolors", "face painting",
            "spray painting", "car painting", "furniture staining", "hair coloring", "marker use",
            "ink use", "airbrushing", "tinting windows"
        ]
    },
    {
        "id": 16,
        "name": "Toveh (Spinning)",
        "hebrew": "טווה",
        "category": "Making Material Curtains",
        "description": "Spinning fibers into thread",
        "examples": ["Spinning wool", "Making rope", "Twisting fibers into yarn"],
        "keywords": [
            "spinning wheel", "yarn making", "rope making", "twisting fibers", "thread creation",
            "yarn spinning", "wool spinning", "rope twisting", "string making", "fiber twisting",
            "twining cord", "braiding rope", "cotton spinning", "spinning thread", "textile creation",
            "fiber arts", "yarn craft", "string preparation", "twisting wire", "making cordage",
            "braiding string", "twisting yarn", "handspinning", "fiber spinning", "wire twisting"
        ]
    },
    {
        "id": 17,
        "name": "Meisach (Warping)",
        "hebrew": "מיסך",
        "category": "Making Material Curtains",
        "description": "Setting up the threads on a loom",
        "examples": ["Setting up a loom", "Arranging threads for weaving", "Preparing warp threads"],
        "keywords": [
            "loom setup", "thread preparation", "loom warping", "weaving preparation",
            "textile preparation", "arranging threads", "setting up warp threads",
            "threading loom", "weaving setup", "warp and weft", "preparing textile",
            "weaving prep", "textile craft", "thread arrangement", "weaving pattern setup",
            "textile design", "handloom preparation", "thread organization", "yarn preparation",
            "fabric preparation", "fiber arts setup", "weaving project", "thread tensioning",
            "preparing material", "thread alignment"
        ]
    },
    {
        "id": 18,
        "name": "Oseh Shtei Batei Nirin (Making Two Loops)",
        "hebrew": "עושה שתי בתי נירין",
        "category": "Making Material Curtains",
        "description": "Creating thread loops for weaving",
        "examples": ["Making heddles on a loom", "Creating thread loops", "Setting up loop patterns"],
        "keywords": [
            "loom heddles", "thread loops", "weaving loops", "textiles", "loop creation",
            "weaving preparation", "fiber loops", "textile craft", "heddle making",
            "thread arrangement", "weaving setup", "loom operation", "loop threading",
            "weaving pattern", "thread preparation", "loop design", "textile manufacturing",
            "weaving technique", "fiber craft", "textile loops", "pattern making",
            "loom threading", "weaving structure", "fabric design", "weaving tools"
        ]
    },
    {
        "id": 19,
        "name": "Oreg (Weaving)",
        "hebrew": "אורג",
        "category": "Making Material Curtains",
        "description": "Interlacing threads to make cloth",
        "examples": ["Weaving fabric", "Knitting", "Braiding hair"],
        "keywords": [
            "weaving", "knitting", "crochet", "braiding hair", "basket making", "loom work",
            "macramé", "knitting scarves", "weaving baskets", "crochet blanket", "cross-stitch",
            "needlepoint", "braiding challah", "braiding friendship bracelets", "weaving pot holders",
            "knitting socks", "hair braiding", "loom weaving", "textile creation", "hand knitting",
            "embroidery", "fabric creation", "thread work", "crochet hook", "knitting needles",
            "knitting machine", "loom operation", "rug weaving", "tapestry making"
        ]
    },
    {
        "id": 20,
        "name": "Potzei'a (Separating Threads)",
        "hebrew": "פוצע",
        "category": "Making Material Curtains",
        "description": "Removing the finished product from the loom",
        "examples": ["Removing woven cloth", "Taking knitting off needles", "Freeing woven material"],
        "keywords": [
            "removing fabric", "unthreading loom", "taking off weaving", "finishing textiles",
            "removing knitting", "completing weaving", "extracting woven product", "unweaving",
            "detaching fabric", "cutting off fabric", "removing from loom", "textile completion",
            "final textile steps", "loom removal", "weaving finalization", "cloth removal",
            "fabric detachment", "completing knitting", "unraveling knitting", "loosening weaving",
            "liberating fabric", "cutting threads", "textile liberation", "freeing cloth",
            "weaving completion"
        ]
    },
    {
        "id": 21,
        "name": "Kosher (Tying)",
        "hebrew": "קושר",
        "category": "Making Material Curtains",
        "description": "Creating a permanent knot",
        "examples": ["Tying shoelaces", "Making fishing knots", "Tying packages"],
        "keywords": [
            "tying knots", "shoelace tying", "knot creation", "rope knots", "tying packages",
            "securing items", "fishing knots", "tying ties", "shoe tying", "binding items",
            "knot work", "rope securing", "package tying", "securing loads", "securing tents",
            "tying boats", "surgical knots", "crafting knots", "binding books", "tying garbage bags",
            "birthday gift wrapping", "yarn knots", "string tying", "cable management", "tying decorations",
            "balloon tying", "securing furniture"
        ]
    },
    {
        "id": 22,
        "name": "Matir (Untying)",
        "hebrew": "מתיר",
        "category": "Making Material Curtains",
        "description": "Untying a permanent knot",
        "examples": ["Untying shoelaces", "Undoing knots", "Opening tied packages"],
        "keywords": [
            "untying knots", "loosening", "unwrapping packages", "opening tied bags",
            "removing knots", "undoing shoelaces", "untying rope", "loosening knots",
            "untying ribbons", "opening gifts", "untangling yarn", "removing tied objects",
            "opening tied boxes", "releasing knots", "untying bows", "package opening",
            "gift unwrapping", "liberating tied items", "removing tied closures",
            "opening tied trash bags", "undoing rope knots", "untying strings",
            "freeing tied objects", "releasing tied bags", "opening food packaging"
        ]
    },
    {
        "id": 23,
        "name": "Tofer (Sewing)",
        "hebrew": "תופר",
        "category": "Making Material Curtains",
        "description": "Joining items with thread and needle",
        "examples": ["Sewing clothes", "Mending tears", "Using a sewing machine"],
        "keywords": [
            "sewing", "stitching", "mending clothes", "sewing machine", "needle and thread",
            "patching holes", "embroidery", "clothing repair", "hemming pants", "tailoring",
            "button sewing", "darning socks", "upholstery repair", "quilting", "cross-stitch",
            "hand sewing", "sewing crafts", "fabric joining", "basting", "seamstress work",
            "pattern sewing", "costume making", "fashion design", "leather stitching",
            "garment alteration", "reattaching buttons", "clothing creation"
        ]
    },
    {
        "id": 24,
        "name": "Kore'a (Tearing)",
        "hebrew": "קורע",
        "category": "Making Material Curtains",
        "description": "Tearing or rending cloth or other material",
        "examples": ["Tearing cloth", "Ripping paper", "Tearing packaging"],
        "keywords": [
            "tearing paper", "ripping cloth", "opening packages", "tearing wrapping paper",
            "fabric tearing", "ripping seams", "tearing open letters", "removing tags",
            "opening sealed containers", "ripping cardboard", "tearing newspaper",
            "opening food packages", "removing product seals", "opening envelopes",
            "tearing toilet paper", "ripping pages", "paper towel tearing", "package opening",
            "opening boxes", "removing bandages", "tearing stickers", "opening medication",
            "breaking seals", "ripping off labels", "removing packaging"
        ]
    },
    
    # Category 3: Making Leather Curtains
    {
        "id": 25,
        "name": "Tzad (Trapping)",
        "hebrew": "צד",
        "category": "Making Leather Curtains",
        "description": "Capturing or restraining a living creature",
        "examples": ["Catching an insect", "Setting mousetraps", "Closing doors on animals"],
        "keywords": [
            "catching insects", "mousetraps", "bug catching", "closing pet cages", "fishing",
            "closing doors on bugs", "pet carriers", "ant traps", "capturing animals",
            "bug containers", "fly swatter", "insect jars", "butterfly nets", "animal control",
            "dog leashes", "animal cages", "pet enclosures", "crab traps", "fish nets",
            "catching mice", "closing aquarium lid", "closing bird cage", "moth trapping",
            "mosquito netting", "live animal capture", "closing windows on insects"
        ]
    },
    {
        "id": 26,
        "name": "Shochet (Slaughtering)",
        "hebrew": "שוחט",
        "category": "Making Leather Curtains",
        "description": "Taking the life of a living creature",
        "examples": ["Killing insects", "Fish slaughter", "Animal slaughter"],
        "keywords": [
            "killing insects", "fishing", "bug killing", "extermination", "swatting flies",
            "pest control", "squashing bugs", "killing mosquitoes", "insect spray",
            "roach killing", "ant poison", "mouse traps", "hunting", "fishing for food",
            "bug spray", "slaughtering animals", "killing pests", "animal butchering",
            "kosher slaughter", "bug elimination", "cockroach killing", "termite treatments",
            "fish killing", "animal processing", "slaughterhouse processes"
        ]
    },
    {
        "id": 27,
        "name": "Mafshit (Skinning/Flaying)",
        "hebrew": "מפשיט",
        "category": "Making Leather Curtains",
        "description": "Removing the hide or skin of an animal",
        "examples": ["Peeling animal skin", "Removing hides", "Skinning animals"],
        "keywords": [
            "skinning", "peeling fruit", "removing peels", "animal processing", "hide removal",
            "peeling vegetables", "removing egg shells", "peeling potatoes", "fruit peeling",
            "removing shells", "banana peeling", "orange peels", "potato skins", "shrimp peeling",
            "crab shell removal", "fish scaling", "removing husks", "corn husking",
            "removing stickers", "peeling labels", "removing plastic packaging", "shell cracking",
            "nut shelling", "removing food wraps", "removing produce stickers"
        ]
    },
    {
        "id": 28,
        "name": "Me'abed (Tanning)",
        "hebrew": "מעבד",
        "category": "Making Leather Curtains",
        "description": "Preserving skins through tanning",
        "examples": ["Leather tanning", "Preserving hides", "Treating leather"],
        "keywords": [
            "leather treatment", "hide preservation", "leather conditioning", "skin preservation",
            "leather processing", "treating skins", "food preserving", "pickling foods",
            "preserving meat", "jerky making", "drying food", "leather care", "curing meat",
            "preserving fish", "smoking food", "fermenting food", "canning produce",
            "jam making", "smoking meats", "fruit preservation", "vegetable pickling",
            "salting meat", "leather conditioning", "chemical preservation",
            "tanning process", "leather crafting", "treating animal skins"
        ]
    },
    {
        "id": 29,
        "name": "Memachek (Smoothing)",
        "hebrew": "ממחק",
        "category": "Making Leather Curtains",
        "description": "Scraping or smoothing the hide",
        "examples": ["Smoothing leather", "Sanding wood", "Polishing metal"],
        "keywords": [
            "sanding", "polishing", "smoothing", "leather work", "furniture finishing",
            "wood sanding", "metal polishing", "buffing", "leather smoothing", "refinishing",
            "sandpaper", "surface preparation", "finishing work", "smoothing rough edges",
            "wood finishing", "removing scratches", "polishing silver", "buffing shoes",
            "sanding furniture", "floor sanding", "metal finishing", "waxing surfaces",
            "filing rough edges", "filing nails", "polishing jewelry", "leather conditioning"
        ]
    },
    {
        "id": 30,
        "name": "Mesartet (Scoring/Marking)",
        "hebrew": "משרטט",
        "category": "Making Leather Curtains",
        "description": "Drawing lines or marking for cutting",
        "examples": ["Drawing cutting lines on leather", "Marking patterns", "Scoring wood for cutting"],
        "keywords": [
            "marking", "drawing lines", "measuring", "pattern making", "scoring", "guidelines",
            "chalk lines", "tailor's marks", "leather marking", "pattern cutting", "ruler use",
            "tracing patterns", "architectural drawing", "drafting", "technical drawing",
            "woodworking marks", "carpentry lines", "measuring fabric", "scoring cardboard",
            "marking measurements", "drawing patterns", "paper templates", "marking leather",
            "creating guides", "craft templates", "marking guidelines"
        ]
    },
    {
        "id": 31,
        "name": "Mechateich (Cutting to Shape)",
        "hebrew": "מחתך",
        "category": "Making Leather Curtains",
        "description": "Cutting material to a specific size or shape",
        "examples": ["Cutting leather to size", "Trimming paper to shape", "Cutting wood to length"],
        "keywords": [
            "cutting", "scissors use", "paper cutting", "fabric cutting", "leather cutting",
            "wood cutting", "trimming", "cutting to size", "cutting board", "knife usage",
            "precision cutting", "shape cutting", "die cutting", "laser cutting", "exacto knife",
            "cutting patterns", "trimming excess", "cutting vegetables", "paper crafts",
            "cutting mat", "rotary cutter", "cookie cutter", "cutting cardboard", "box cutting",
            "cutting wires", "cutting tape", "cutting bread", "meat cutting"
        ]
    },
    
    # Category 4: Making the Beams of the Mishkan
    {
        "id": 32,
        "name": "Kotev (Writing)",
        "hebrew": "כותב",
        "category": "Making the Beams of the Mishkan",
        "description": "Creating letters, symbols or drawing images",
        "examples": ["Writing words", "Typing on a computer", "Drawing pictures"],
        "keywords": [
            "writing", "typing", "drawing", "digital writing", "handwriting", "calligraphy",
            "note taking", "keyboard use", "document creation", "signing documents",
            "writing emails", "texting", "messaging", "social media posting", "letter writing",
            "journaling", "graphic design", "sketching", "drawing diagrams", "writing code",
            "digital art", "graffiti", "signature", "addressing envelopes", "making lists",
            "filling forms", "completing documents", "printer use"
        ]
    },
    {
        "id": 33,
        "name": "Mochek (Erasing)",
        "hebrew": "מוחק",
        "category": "Making the Beams of the Mishkan",
        "description": "Erasing letters, symbols or drawings",
        "examples": ["Erasing pencil marks", "Deleting computer text", "Removing writing"],
        "keywords": [
            "erasing", "deleting", "backspacing", "removing text", "clearing writing",
            "eraser use", "deleting files", "clearing history", "removing ink", "white-out",
            "correction fluid", "removing pencil marks", "editing documents", "clearing boards",
            "deleting emails", "removing posts", "digital deletion", "clearing browser history",
            "erasing chalk", "removing signatures", "deleting photos", "clearing notes",
            "removing stains", "cleaning surfaces", "digital erasing", "message deletion"
        ]
    },
    
    # Category 5: The Putting up and Taking down of the Mishkan
    {
        "id": 34,
        "name": "Boneh (Building)",
        "hebrew": "בונה",
        "category": "The Putting up and Taking down of the Mishkan",
        "description": "Constructing or forming a durable connection",
        "examples": ["Building structures", "Assembling furniture", "Installing fixtures"],
        "keywords": [
            "building", "construction", "assembling", "installing", "home improvement", 
            "furniture assembly", "IKEA furniture", "fixing appliances", "home repairs",
            "hanging pictures", "mounting TVs", "installing shelves", "building decks",
            "construction projects", "setting up tents", "building legos", "installing fixtures",
            "organizing closets", "arranging furniture", "building blocks", "model making",
            "setting up equipment", "putting together toys", "constructing models",
            "puzzle assembly", "construction tools", "wall mounting"
        ]
    },
    {
        "id": 35,
        "name": "Soter (Breaking Down)",
        "hebrew": "סותר",
        "category": "The Putting up and Taking down of the Mishkan",
        "description": "Demolishing or taking apart a structure",
        "examples": ["Dismantling furniture", "Demolishing walls", "Taking apart devices"],
        "keywords": [
            "disassembling", "demolishing", "dismantling", "taking apart", "removing fixtures",
            "furniture disassembly", "breaking down structures", "home demolition", "uninstalling",
            "unscrewing", "detaching parts", "separating components", "removing shelves",
            "taking down tents", "breaking apart legos", "opening devices", "removing attachments",
            "deconstructing", "unbuilding", "disassembling toys", "demolition work", "breaking down",
            "removing installations", "unfastening", "unscrewing parts", "hardware removal",
            "taking down decorations"
        ]
    },
    
    # Category 6: The Mishkan's Final Touches
    {
        "id": 36,
        "name": "Makeh B'Patish (Completing a Task)",
        "hebrew": "מכה בפטיש",
        "category": "The Mishkan's Final Touches",
        "description": "Completing the final step in a process",
        "examples": ["Putting final touches on a project", "Completing an item", "Final adjustments"],
        "keywords": [
            "finishing touches", "completing projects", "finalizing work", "final adjustments", 
            "last details", "project completion", "fine-tuning", "final edits", "perfecting",
            "putting on finishing touches", "final corrections", "adding last details",
            "completing tasks", "closing projects", "adding final features", "polishing work",
            "final assembly", "last minute adjustments", "quality control", "final inspection",
            "finishing work", "final embellishments", "completing products", "final review",
            "perfecting details", "finishing steps", "final configuration"
        ]
    },
    {
        "id": 37,
        "name": "Mechabeh (Extinguishing)",
        "hebrew": "מכבה",
        "category": "The Mishkan's Final Touches",
        "description": "Extinguishing or diminishing a fire or flame",
        "examples": ["Putting out a fire", "Turning off gas burners", "Extinguishing candles"],
        "keywords": [
            "extinguishing fires", "putting out flames", "turning off stoves", "extinguishing candles",
            "turning off lights", "shutting down appliances", "powering down electronics",
            "turning off gas", "fire prevention", "dousing flames", "smothering fire",
            "fire safety", "turning off burners", "extinguishing matches", "water on fire",
            "fire extinguisher", "turning off heaters", "shutting systems down", "powering off",
            "turning off electronic devices", "shutting down computers", "turning off ovens",
            "extinguishing bbq", "turning off equipment", "closing gas valves"
        ]
    },
    {
        "id": 38,
        "name": "Mav'ir (Kindling a Fire)",
        "hebrew": "מבעיר",
        "category": "The Mishkan's Final Touches",
        "description": "Creating or adding fuel to a fire",
        "examples": ["Lighting a match", "Starting a fire", "Turning on an electric stove"],
        "keywords": [
            "lighting fires", "turning on stoves", "lighting candles", "starting bbq",
            "turning on ovens", "lighting matches", "creating sparks", "turning on lights",
            "powering on devices", "turning on electronics", "igniting gas", "starting bonfires",
            "lighting grills", "turning on heaters", "fireplaces", "lighting cigarettes",
            "starting car engines", "turning on appliances", "powering up", "lighting lamps",
            "turning on electric stoves", "heating elements", "switching on", "activating electronics",
            "turning on cooking devices", "starting combustion", "lighting gas burners", "phone"
        ]
    },
    {
        "id": 39,
        "name": "Hotza'ah (Transferring Between Domains)",
        "hebrew": "הוצאה",
        "category": "The Mishkan's Final Touches",
        "description": "Carrying from a private domain to a public domain, or vice versa",
        "examples": ["Carrying from house to street", "Taking items from home", "Carrying wallet outside"],
        "keywords": [
            "carrying outside", "bringing in", "taking out", "transporting items", "moving objects",
            "carrying wallet", "taking keys", "carrying bags", "outdoor transport", "public carrying",
            "bringing groceries", "moving between domains", "carrying shopping", "transporting goods",
            "taking out trash", "bringing in mail", "carrying from car", "taking to street",
            "outdoor movement", "public transport of items", "carrying purses", "moving belongings",
            "carrying ID", "moving packages", "carrying items outside", "bringing objects indoors",
            "carrying phones", "transporting outdoor", "carrying in public"
        ]
    }
]

# Routes

# GET all melachot
@app.route('/api/melachot', methods=['GET'])
def get_all_melachot():
    return jsonify(melachot)

# GET a specific melacha by ID
@app.route('/api/melachot/<int:melacha_id>', methods=['GET'])
def get_melacha(melacha_id):
    for melacha in melachot:
        if melacha['id'] == melacha_id:
            return jsonify(melacha)
    return jsonify({"error": "Melacha not found"}), 404

# GET melachot by category
@app.route('/api/categories/<category>', methods=['GET'])
def get_by_category(category):
    results = [m for m in melachot if m['category'].lower() == category.lower()]
    if results:
        return jsonify(results)
    return jsonify({"error": "Category not found"}), 404

# GET list of all categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = list(set(m['category'] for m in melachot))
    return jsonify(categories)

# POST - Add a new melacha (admin functionality)
@app.route('/api/melachot', methods=['POST'])
def add_melacha():
    new_melacha = request.json
    
    # Validate required fields
    if not all(key in new_melacha for key in ['name', 'category', 'description']):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Generate new ID (simple implementation)
    new_id = max(m['id'] for m in melachot) + 1
    new_melacha['id'] = new_id
    
    melachot.append(new_melacha)
    return jsonify(new_melacha), 201

# PUT - Update a melacha
@app.route('/api/melachot/<int:melacha_id>', methods=['PUT'])
def update_melacha(melacha_id):
    update_data = request.json
    
    for i, melacha in enumerate(melachot):
        if melacha['id'] == melacha_id:
            # Update the melacha while preserving its ID
            melachot[i] = {**update_data, 'id': melacha_id}
            return jsonify(melachot[i])
    
    return jsonify({"error": "Melacha not found"}), 404

# DELETE - Remove a melacha
@app.route('/api/melachot/<int:melacha_id>', methods=['DELETE'])
def delete_melacha(melacha_id):
    for i, melacha in enumerate(melachot):
        if melacha['id'] == melacha_id:
            deleted = melachot.pop(i)
            return jsonify({"message": f"Melacha '{deleted['name']}' deleted successfully"})
    
    return jsonify({"error": "Melacha not found"}), 404

# Search melachot by name or description
@app.route('/api/search', methods=['GET'])
def search_melachot():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query is required"}), 400
    
    results = [m for m in melachot if query in m['name'].lower() or query in m['description'].lower()]
    return jsonify(results)

# Search melachot by keywords
@app.route('/api/search/keywords', methods=['GET'])
def search_by_keyword():
    keyword = request.args.get('keyword', '').lower()
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    
    results = []
    for melacha in melachot:
        if 'keywords' in melacha:
            if any(keyword in kw.lower() for kw in melacha['keywords']):
                results.append(melacha)
    
    return jsonify(results)

# GET all keywords
@app.route('/api/keywords', methods=['GET'])
def get_all_keywords():
    all_keywords = set()
    for melacha in melachot:
        if 'keywords' in melacha:
            all_keywords.update(melacha['keywords'])
    return jsonify(sorted(list(all_keywords)))

if __name__ == '__main__':
    app.run(debug=True, port=3000)