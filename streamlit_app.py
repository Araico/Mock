# app.py
import streamlit as st
from ui_tokens import inject_tokens, theme_css

# ======= Page config =======
st.set_page_config(
    page_title="Data Analytics AI", page_icon="images/icon_blue.png", layout="wide"
)

# ======= Inject shared tokens =======
inject_tokens()

# ======= Session init =======
if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "PC", "Professor", "Team"]

# ======= Branding =======
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")
st.title("Data Analytics AI")


# ======= LOGIN / LOGOUT =======
def login():
    st.subheader("Log in")
    st.caption("Select your role to enable the corresponding sections.")

    c1, c2, c3 = st.columns(3)
    role_map = {
        "PC": ("PC", "Access to Visualization (Dashboards and Maps)."),
        "Professor": ("Professor", "Full access: EDA, ML, and Visualization."),
        "Team": ("Team", "Access to EDA, ML, and Visualization."),
    }

    def role_card(container, role_key):
        with container:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"**{role_map[role_key][0]}**  \n{role_map[role_key][1]}")
            st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
            if st.button(f"Sign in as {role_key}", key=f"btn_{role_key}"):
                st.session_state.role = role_key
                st.toast(f"Logged in as {role_key}")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    role_card(c1, "PC")
    role_card(c2, "Professor")
    role_card(c3, "Team")

    st.divider()
    with st.expander("Classic selector"):
        role = st.selectbox("Choose your role", ROLES, index=0)
        if st.button("Log in (selector)"):
            st.session_state.role = role
            st.rerun()


def logout():
    st.subheader("Log out")
    st.write("Change role or end the session.")
    if st.button("Log out"):
        st.session_state.role = None
        st.toast("Session cleared")
        st.rerun()


# ======= Pages (original structure, improved icons) =======
role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

visualization = st.Page(
    "Visualization/visualization.py",
    title="Dashboard",
    icon=":material/space_dashboard:",
    default=(role == "Requester"),
)
maps = st.Page(
    "Visualization/maps.py",
    title="Maps",
    icon=":material/map:",
    default=(role == "Requester"),
)
maps2 = st.Page(
    "Visualization/maps2.py",
    title="Other maps",
    icon=":material/layers:",
    default=(role == "Requester"),
)

ml = st.Page(
    "ml/ml_analysis.py",
    title="Machine Learning",
    icon=":material/neurology:",
    default=(role == "Responder"),
)
eda = st.Page(
    "EDA/eda.py",
    title="Exploratory Data Analysis",
    icon=":material/analytics:",
    default=(role == "Admin"),
)

account_pages = [logout_page, settings]
visualization_pages = [visualization, maps, maps2]
ml_pages = [ml]
eda_pages = [eda]

# ======= Sidebar =======
with st.sidebar:
    st.image("images/icon_blue.png", width=64)
    st.markdown("### Navigation")
    if role:
        st.markdown(
            f"**Role:** <span class='badge'>{role}</span>", unsafe_allow_html=True
        )
    else:
        st.caption("Not logged in")

    st.write("")  # spacing
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.caption("Quick tips")
    st.write("- Use the menu to open sections.")
    st.write("- Change your role using **Log out**.")
    st.write("- Customize colors in **Settings**.")
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='footer' style='color:#6b7280; font-size:12px; text-align:center; margin-top: 18px;'>© 2025 Data Analytics AI</div>",
        unsafe_allow_html=True,
    )

# ======= Sections by role =======
page_dict = {}
if role in ["Professor", "Team"]:
    page_dict["EDA"] = eda_pages
if role in ["Professor", "Team", "PC"]:
    page_dict["Visualization"] = visualization_pages
if role in ["Professor", "Team"]:
    page_dict["Machine Learning"] = ml_pages

# ======= Landing vs navigation =======
if len(page_dict) > 0:
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            "<div class='card'>**Status**  \nActive dashboards</div>",
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            "<div class='card'>**Maps**  \nGeospatial layers ready</div>",
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            "<div class='card'>**ML**  \nPipelines configured</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-title' style='font-weight:800; font-size:1.05rem; margin: 0.3rem 0 0.4rem 0; color:#243b53; letter-spacing: .2px;'>Sections</div>",
        unsafe_allow_html=True,
    )

    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Welcome")
    st.write("Sign in by selecting your role to access the project sections.")
    st.markdown("</div>", unsafe_allow_html=True)
    pg = st.navigation([st.Page(login)])

pg.run()
