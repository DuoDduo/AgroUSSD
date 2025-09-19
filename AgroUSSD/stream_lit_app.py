# streamlit_agroussd_gui.py
import streamlit as st
from services.user_service import UserService
from services.harvest_service import HarvestService
from services.market_service import MarketService
from services.connection_service import ConnectionService
from utils.translators import translate

# Initialize services

user_service = UserService()
harvest_service = HarvestService()
market_service = MarketService()
conn_service = ConnectionService()

# Session defaults
if "language" not in st.session_state:
    st.session_state.language = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "menu_step" not in st.session_state:
    st.session_state.menu_step = "dial"


# Translation helper
def t(key):
    return translate(key, st.session_state.language or "en")


# Step 1: Dial USSD
if st.session_state.menu_step == "dial":
    st.title("🌾 AgroUSSD Web Simulator")
    ussd = st.text_input("Dial *882# to start (or type 'exit' to quit):")
    if ussd.strip() == "*882#":
        st.session_state.menu_step = "select_language"
    elif ussd.lower() == "exit":
        st.stop()
    else:
        st.warning("Invalid USSD code")


# Step 2: Language selection

if st.session_state.menu_step == "select_language":
    st.subheader("Select Language / Yan Ede / Họrọ Asụsụ / Zaɓi Harshe / Pidgin")
    lang_option = st.radio(
        "", ["English", "Yoruba", "Igbo", "Hausa", "Pidgin"]
    )
    if st.button("Set Language"):
        lang_codes = {"English":"en", "Yoruba":"yo", "Igbo":"ig", "Hausa":"ha", "Pidgin":"pcm"}
        st.session_state.language = lang_codes[lang_option]
        st.success(f"Language set to {lang_option}")
        st.session_state.menu_step = "main_menu"

# Step 3: Main Menu

if st.session_state.menu_step == "main_menu":
    st.subheader(t("welcome_message"))
    option = st.radio(
        t("select_option"),
        [
            t("register_farmer"),
            t("register_buyer"),
            t("login"),
            t("browse_market_prices"),
            t("search_farmers"),
            t("exit")
        ]
    )

    if st.button(t("confirm")):
        if option == t("register_farmer"):
            st.session_state.menu_step = "register_farmer"
        elif option == t("register_buyer"):
            st.session_state.menu_step = "register_buyer"
        elif option == t("login"):
            st.session_state.menu_step = "login"
        elif option == t("browse_market_prices"):
            st.session_state.menu_step = "market_prices"
        elif option == t("search_farmers"):
            st.session_state.menu_step = "search_farmers"
        elif option == t("exit"):
            st.info(t("thank_you_bye"))
            st.stop()

# Register Farmer
if st.session_state.menu_step == "register_farmer":
    st.subheader(t("register_farmer"))
    with st.form("farmer_form"):
        name = st.text_input(t("enter_name"))
        phone = st.text_input(t("enter_phone"))
        location = st.text_input(t("enter_location"))
        farm_size = st.number_input(t("enter_farm_size"), min_value=0.0)
        crops = st.text_input(t("enter_primary_crops"))
        pin = st.text_input(t("enter_pin"), type="password")
        pin_confirm = st.text_input(t("confirm_pin"), type="password")
        submitted = st.form_submit_button(t("submit"))

        if submitted:
            if pin != pin_confirm:
                st.error(t("pin_mismatch"))
            else:
                try:
                    crops_list = [c.strip() for c in crops.split(",") if c.strip()]
                    f = user_service.register_farmer(name, phone, location, pin, farm_size, crops_list)
                    st.success(f"{t('farmer_registered')}: {f.name} ({f.phone})")
                    st.session_state.menu_step = "main_menu"
                except Exception as e:
                    st.error(f"{t('error')}: {e}")


# Register Buyer
if st.session_state.menu_step == "register_buyer":
    st.subheader(t("register_buyer"))
    with st.form("buyer_form"):
        name = st.text_input(t("enter_name"))
        phone = st.text_input(t("enter_phone"))
        location = st.text_input(t("enter_location"))
        business = st.text_input(t("enter_business_name"))
        pin = st.text_input(t("enter_pin"), type="password")
        pin_confirm = st.text_input(t("confirm_pin"), type="password")
        submitted = st.form_submit_button(t("submit"))

        if submitted:
            if pin != pin_confirm:
                st.error(t("pin_mismatch"))
            else:
                try:
                    b = user_service.register_buyer(name, phone, location, pin, business)
                    st.success(f"{t('buyer_registered')}: {b.name} ({b.phone})")
                    st.session_state.menu_step = "main_menu"
                except Exception as e:
                    st.error(f"{t('error')}: {e}")


# Login
if st.session_state.menu_step == "login":
    st.subheader(t("login"))
    phone = st.text_input(t("enter_phone"))
    pin = st.text_input(t("enter_pin"), type="password")
    if st.button(t("login_button")):
        u = user_service.authenticate(phone, pin)
        if not u:
            st.error(t("invalid_credentials"))
        else:
            st.success(t("login_success"))
            st.session_state.current_user = u
            st.session_state.menu_step = "farmer_menu" if u["type"]=="farmer" else "buyer_menu"


# Farmer GUI
if st.session_state.menu_step == "farmer_menu":
    st.subheader(f"{t('welcome')} {st.session_state.current_user.get('name')} ({t('farmer_role')})")
    farmer_options = st.radio("", [t("record_harvest"), t("my_harvests"), t("set_market_price"), t("update_profile"), t("logout")])

    if farmer_options == t("record_harvest"):
        with st.form("harvest_form"):
            product = st.text_input(t("enter_product_name"))
            quantity = st.number_input(t("enter_quantity"), min_value=0.0)
            quality = st.selectbox(t("select_quality"), ["good","fair","poor"])
            price = st.number_input(t("enter_price"), min_value=0.0)
            submitted = st.form_submit_button(t("submit"))
            if submitted:
                try:
                    h = harvest_service.record_harvest(
                        farmer_phone=st.session_state.current_user["phone"],
                        product_name=product,
                        quantity=quantity,
                        quality=quality,
                        asking_price=price
                    )
                    st.success(f"{t('harvest_recorded')}: {product} ({quantity} units)")
                except Exception as e:
                    st.error(f"{t('error')}: {e}")

    elif farmer_options == t("my_harvests"):
        hs = harvest_service.list_harvest(st.session_state.current_user["phone"])
        if not hs:
            st.info(t("no_harvests"))
        else:
            st.table(hs)

    elif farmer_options == t("set_market_price"):
        with st.form("market_form"):
            prod = st.text_input(t("enter_product_name"))
            loc = st.text_input(t("market_location"))
            price = st.number_input(t("enter_price"), min_value=0.0)
            submitted = st.form_submit_button(t("submit"))
            if submitted:
                market_service.set_price(prod, loc, price)
                st.success(t("market_price_updated"))

    elif farmer_options == t("update_profile"):
        with st.form("update_profile_form"):
            name = st.text_input(t("enter_name"), value=st.session_state.current_user.get("name"))
            location = st.text_input(t("enter_location"), value=st.session_state.current_user.get("location"))
            submitted = st.form_submit_button(t("submit"))
            if submitted:
                user = st.session_state.current_user
                user["name"] = name
                user["location"] = location
                user_service.update_user(user)
                st.session_state.current_user = user
                st.success(t("profile_updated"))

    elif farmer_options == t("logout"):
        st.session_state.current_user = None
        st.session_state.menu_step = "main_menu"
        st.experimental_rerun()

# Buyer GUI options
if st.session_state.menu_step == "buyer_menu":
    st.subheader(f"{t('welcome')} {st.session_state.current_user.get('name')} ({t('buyer_role')})")
    buyer_options = st.radio(
        "",
        [
            t("search_produce"),
            t("browse_farmers"),
            t("contact_farmer"),
            t("update_profile"),
            t("logout")
        ]
    )

    if buyer_options == t("search_produce"):
        prod = st.text_input(t("enter_product_name"))
        if st.button(t("search")):
            res = market_service.compare_prices(prod)
            if not res:
                st.warning(t("no_market_data"))
            else:
                for r in res:
                    st.write(f"{r['location']}: ₦{r['price']}")

    elif buyer_options == t("browse_farmers"):
        loc = st.text_input(t("search_location"))
        prod = st.text_input(t("search_product"))
        if st.button(t("search")):
            farmers = user_service.list_farmers(location=loc or None, product=prod or None)
            if not farmers:
                st.info(t("no_farmers_found"))
            else:
                st.table(farmers)

    elif buyer_options == t("contact_farmer"):
        st.info("This feature can allow messaging/calling farmers (to be implemented)")

    elif buyer_options == t("update_profile"):
        with st.form("buyer_update_form"):
            name = st.text_input(t("enter_name"), value=st.session_state.current_user.get("name"))
            location = st.text_input(t("enter_location"), value=st.session_state.current_user.get("location"))
            submitted = st.form_submit_button(t("submit"))
            if submitted:
                user = st.session_state.current_user
                user["name"] = name
                user["location"] = location
                user_service.update_user(user)
                st.session_state.current_user = user
                st.success(t("profile_updated"))

    elif buyer_options == t("logout"):
        st.session_state.current_user = None
        st.session_state.menu_step = "main_menu"
        st.experimental_rerun()
