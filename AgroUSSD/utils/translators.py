# this file contains translations for various prompts and messages in multiple languages
# used across the AgroUSSD application.
languages = ["en", "yo", "ig", "ha", "pi"]  # English, Yoruba, Igbo, Hausa, Pidgin

translations = {
    # Main / navigation
    "welcome_message": {
        "en": "Welcome to AgroUSSD",
        "yo": "Kaabọ si AgroUSSD",
        "ig": "Nnọọ na AgroUSSD",
        "ha": "Barka da zuwa AgroUSSD",
        "pi": "How far! Welcome to AgroUSSD"
    },
    "select_language_prompt": {
        "en": "Select language:",
        "yo": "Yan ede:",
        "ig": "Họrọ asụsụ:",
        "ha": "Zaɓi harshe:",
        "pi": "Choose language:"
    },
    "menu_prompt": {
        "en": "Select option",
        "yo": "Yan aṣayan",
        "ig": "Họrọ nhọrọ",
        "ha": "Zaɓi zaɓi",
        "pi": "Which one you wan?"
    },
    "register_farmer": {
        "en": "Register as Farmer",
        "yo": "Forukọsilẹ bi Agbe",
        "ig": "Debanye aha dị ka Onye Ọkụ",
        "ha": "Yi rajista a matsayin Manomi",
        "pi": "Register as Farmer"
    },
    "register_buyer": {
        "en": "Register as Buyer",
        "yo": "Forukọsilẹ bi Olura",
        "ig": "Debanye aha dị ka Onye Zụrụ",
        "ha": "Yi rijista a matsayin Mai Saye",
        "pi": "Register as Buyer"
    },
    "login": {
        "en": "Login",
        "yo": "Wọle",
        "ig": "Banye",
        "ha": "Shiga",
        "pi": "Login"
    },
    "browse_market_prices": {
        "en": "Browse Market Prices",
        "yo": "Wo Iye Ọja",
        "ig": "Lelee ọnụ ahịa ahịa",
        "ha": "Duba Farashin Kasuwa",
        "pi": "Check Market Price"
    },
    "search_farmers": {
        "en": "Search Farmers",
        "yo": "Wa Awọn Agbe",
        "ig": "Chọọ ndị na-akọ",
        "ha": "Nemo manoma",
        "pi": "Search Farmers"
    },
    "exit": {
        "en": "Exit",
        "yo": "Jade",
        "ig": "Pụọ",
        "ha": "Fita",
        "pi": "Comot"
    },
    "thank_you_bye": {
        "en": "Thank you for using AgroUSSD. Bye.",
        "yo": "O ṣeun fun lilo AgroUSSD. O dabọ.",
        "ig": "Daalu maka iji AgroUSSD. Ka ọ dị.",
        "ha": "Na gode da amfani da AgroUSSD. Sai anjima.",
        "pi": "Thank you for using AgroUSSD. Bye-bye."
    },

    # Inputs / prompts
    "enter_name": {
        "en": "Name: ",
        "yo": "Orukọ: ",
        "ig": "Aha: ",
        "ha": "Suna: ",
        "pi": "Name: "
    },
    "enter_phone": {
        "en": "Phone (e.g. 080xxxxxxx): ",
        "yo": "Foonu (e.g. 080xxxxxxx): ",
        "ig": "Ekwenti (e.g. 080xxxxxxx): ",
        "ha": "Lambar waya (e.g. 080xxxxxxx): ",
        "pi": "Phone (e.g. 080xxxxxxx): "
    },
    "enter_location": {
        "en": "Location (state/city): ",
        "yo": "Ibi (Ipinle/Ilẹ̀): ",
        "ig": "Ebe (steeti/obodo): ",
        "ha": "Wuri (jiha/garin): ",
        "pi": "Where you dey (state/city): "
    },
    "enter_farm_size": {
        "en": "Farm size (hectares): ",
        "yo": "Iwọn oko (hectares): ",
        "ig": "Ibu ubi (hectares): ",
        "ha": "Girman gona (hectares): ",
        "pi": "How many hectares: "
    },
    "enter_primary_crops": {
        "en": "Primary crops (comma separated): ",
        "yo": "Awọn ọgbin akọkọ (ya pẹlu koma): ",
        "ig": "Crops ndị bụ isi (tinye comma): ",
        "ha": "Babban amfanin gona (raba da comma): ",
        "pi": "Primary crops (separate with comma): "
    },
    "enter_business_name": {
        "en": "Business name (optional): ",
        "yo": "Orukọ iṣowo (aṣayan): ",
        "ig": "Aha azụmahịa (nke bụghị iwu): ",
        "ha": "Sunan kasuwanci (zabi): ",
        "pi": "Business name (if you get): "
    },
    "enter_pin": {
        "en": "Enter PIN: ",
        "yo": "Tẹ PIN: ",
        "ig": "Tinye PIN: ",
        "ha": "Shigar da PIN: ",
        "pi": "Enter your PIN: "
    },

    # Registration / login / errors
    "farmer_registered": {
        "en": "Farmer registered",
        "yo": "Agbe ti forukọsilẹ",
        "ig": "A denye onye ọkụ",
        "ha": "An yi rajista manomi",
        "pi": "Farmer don register"
    },
    "buyer_registered": {
        "en": "Buyer registered",
        "yo": "Olura ti forukọsilẹ",
        "ig": "A denye onye zụrụ",
        "ha": "An yi rajista mai siye",
        "pi": "Buyer don register"
    },
    "error": {
        "en": "Error",
        "yo": "Aṣiṣe",
        "ig": "Njọ",
        "ha": "Kuskure",
        "pi": "Error"
    },
    "invalid_credentials": {
        "en": "Invalid credentials",
        "yo": "Awọn iwe-ẹri ti ko tọ",
        "ig": "Akwụkwọ ikike adịghị irè",
        "ha": "Bayanan shiga ba daidai ba ne",
        "pi": "Credentials no correct"
    },
    "invalid_choice": {
        "en": "Invalid choice",
        "yo": "Aṣayan ti ko tọ",
        "ig": "Nhọrọ ezighi ezi",
        "ha": "Zaɓin da bai dace ba",
        "pi": "Na wrong choice"
    },
    "phone_already_registered": {
        "en": "Phone number already registered",
        "yo": "Foonu ti forukọsilẹ tẹlẹ",
        "ig": "Ekwenti edebere",
        "ha": "Lambar waya ta riga an yi rijista",
        "pi": "Phone don register before"
    },

    # Farmer menu
    "hello": {"en":"Hello","yo":"Bawo","ig":"Ndewo","ha":"Sannu","pi":"How far"},
    "farmer": {"en":"Farmer","yo":"Agbe","ig":"Onye ọchụ","ha":"Manomi","pi":"Farmer"},
    "buyer": {"en":"Buyer","yo":"Olura","ig":"Onye na-azụ","ha":"Mai siye","pi":"Buyer"},
    "record_harvest": {"en":"Record Harvest","yo":"Gba Ajọjọ","ig":"Dee ihe ubi","ha":"Rubuta amfanin gona","pi":"Post wetin you harvest"},
    "my_harvests": {"en":"My Harvests","yo":"Awọn Ikore mi","ig":"Ihe m kọrọ","ha":"Amfanin gonata","pi":"My harvests"},
    "set_market_price": {"en":"Set Market Price","yo":"Ṣeto Iye Ọja","ig":"Tọọ ọnụahịa ahịa","ha":"Saita farashin kasuwa","pi":"Set market price"},
    "update_profile": {"en":"Update Profile","yo":"Imudojuiwọn Profaili","ig":"Melite profaịlụ","ha":"Sabunta bayanin martaba","pi":"Update your profile"},
    "logout": {"en":"Logout","yo":"Jade","ig":"Wepụ","ha":"Fice","pi":"Logout"},
    "logged_out": {"en":"Logged out","yo":"Ti jade","ig":"E wepu","ha":"An fita","pi":"You don logout"},

    # Harvest messages
    "harvest_recorded": {"en":"Harvest recorded","yo":"Ikore ti gba","ig":"Edebe ihe ubi","ha":"An rubuta amfanin gona","pi":"Harvest don record"},
    "no_harvests_recorded": {"en":"No harvests recorded","yo":"Ko si ikore ti a gba","ig":"Enweghị ihe ubi edere","ha":"Babu rikodin amfanin gona","pi":"No harvest wey dem post"},
    "market_price_updated": {"en":"Market price updated","yo":"Iye ọja ti ni imudojuiwọn","ig":"Emelitere ọnụahịa ahịa","ha":"An sabunta farashin kasuwa","pi":"Market price don update"},

    # Market / price displays
    "no_market_data": {"en":"No market data for that product yet.","yo":"Ko si data ọja fun ọja yẹn sibẹsibẹ.","ig":"Enweghị data ahịa maka ngwaahịa ahụ ugbu a.","ha":"Babu bayanan kasuwa ga wannan samfurin tukuna.","pi":"No market data for that product yet."},
    "no_farmers_found": {"en":"No farmers found","yo":"Ko si awọn agbe ti a ri","ig":"Enweghị ndị na-akọ achọtara","ha":"Babu manoma an samu","pi":"No farmers wey we find"},
    "crops": {"en":"Crops","yo":"Awọn ọgbin","ig":"Crops","ha":"Amfanin gona","pi":"Crops"},

    # Connections
    "contact_recorded": {"en":"Contact recorded.","yo":"Ibaraẹnisọrọ ti gbasilẹ.","ig":"Akpọtụrụ edebere.","ha":"An rubuta tuntuɓa.","pi":"Contact don record"},
    "farmer_number": {"en":"Farmer number","yo":"Nọmba agbe","ig":"Nọmba onye ọkụ","ha":"Lambar manomi","pi":"Farmer number"},

    # Generic invalid input
    "invalid_input": {"en":"Invalid input, try again.","yo":"Aṣayan ti ko tọ, gbiyanju lẹẹkansi.","ig":"Ntinye ezighi ezi, nwalee ọzọ.","ha":"Shigarwa ba daidai ba, gwada sake.","pi":"No correct, try am again."}
}

def translate(key: str, lang: str = "en") -> str:
    """Return translated text for given key and language; fallback to English."""
    entry = translations.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get("en")
