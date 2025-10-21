import streamlit as st
from dataclasses import dataclass

# =========================
# Page and Session Setup
# =========================
st.set_page_config(page_title="Settings", page_icon="⚙️", layout="centered")

# Default session state values
st.session_state.setdefault("role", "guest")
st.session_state.setdefault("theme_mode", "auto")  # "auto" | "light" | "dark"
st.session_state.setdefault("accent", "#3b82f6")  # default accent color
st.session_state.setdefault("font_scale", "base")  # xs | sm | base | lg | xl
st.session_state.setdefault("density", "normal")  # compact | normal | spacious


# =========================
# Theming Helper (CSS)
# =========================
def theme_css(mode: str, accent: str, font_scale: str, density: str) -> str:
    font_scale_map = {
        "xs": "0.90",
        "sm": "0.95",
        "base": "1.00",
        "lg": "1.06",
        "xl": "1.12",
    }
    density_map = {"compact": "6px", "normal": "10px", "spacious": "14px"}

    return f"""
<style>
:root {{
  --bg: #ffffff;
  --bg-alt: #f6f7fb;
  --fg: #111111;
  --muted: #475569;
  --primary: #3b82f6;
  --border: #e5e7eb;

  /* Custom tokens */
  --accent: {accent};
  --font-scale: {font_scale_map.get(font_scale, '1.00')};
  --pad-y: {density_map.get(density, '10px')};
}}

/* Smooth transitions */
@media (prefers-reduced-motion: no-preference) {{
  [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
    transition: background-color .2s ease, color .2s ease, border-color .2s ease;
  }}
}}

/* AUTO mode follows OS dark theme */
{("""
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0E1117;
    --bg-alt: #151923;
    --fg: #E6E9EF;
    --muted: #a0a3ad;
    --primary: #60a5fa;
    --border: #2a2f3a;
  }
}
""" if mode == "auto" else "")}

{("""
/* FORCE LIGHT */
:root {
  --bg: #ffffff;
  --bg-alt: #f6f7fb;
  --fg: #111111;
  --muted: #475569;
  --primary: #3b82f6;
  --border: #e5e7eb;
}
""" if mode == "light" else "")}

{("""
/* FORCE DARK */
:root {
  --bg: #0E1117;
  --bg-alt: #151923;
  --fg: #E6E9EF;
  --muted: #a0a3ad;
  --primary: #60a5fa;
  --border: #2a2f3a;
}
""" if mode == "dark" else "")}

/* === Apply tokens === */
html, body, [data-testid="stAppViewContainer"], .block-container {{
  background: var(--bg);
  color: var(--fg);
  font-size: calc(16px * var(--font-scale));
}}

a, .stMarkdown a {{
  color: var(--accent);
}}

.stButton>button, .stDownloadButton>button {{
  background: var(--bg-alt) !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  padding: calc(var(--pad-y) * 0.9) 16px !important;
}}

div[data-baseweb="input"] input,
textarea, .stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox div[role="combobox"], .stMultiSelect div[role="combobox"] {{
  background: var(--bg-alt) !important;
  color: var(--fg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  padding: var(--pad-y) 12px !important;
}}

hr {{ border-color: var(--border); }}

[data-testid="stSidebar"] {{
  background: var(--bg-alt);
  border-right: 1px solid var(--border);
  color: var(--fg);
}}
[data-testid="stSidebar"] * {{ color: var(--fg) !important; }}
[data-testid="stSidebar"] a {{ color: var(--accent) !important; }}
[data-testid="stSidebar"] .stButton>button,
[data-testid="stSidebar"] .stDownloadButton>button {{
  background: var(--bg) !important;
}}

.badge {{
  display:inline-block; padding: 4px 10px; border-radius: 999px;
  background: color-mix(in srgb, var(--accent) 15%, transparent);
  color: var(--accent); font-weight:600; font-size:12px;
  border: 1px solid color-mix(in srgb, var(--accent) 40%, transparent);
}}

.card {{
  border-radius: 16px; padding: 16px; background: var(--bg);
  border: 1px solid var(--border);
  box-shadow: 0 6px 20px rgba(0,0,0,.06);
}}
.kpi {{
  font-weight:700; font-size: 1.15em;
}}
.hr {{ height:1px; background:var(--border); margin: 8px 0 14px 0; }}
</style>
"""


# Inject CSS immediately
st.markdown(
    theme_css(
        st.session_state.theme_mode,
        st.session_state.accent,
        st.session_state.font_scale,
        st.session_state.density,
    ),
    unsafe_allow_html=True,
)

# =========================
# Sidebar Settings
# =========================
st.sidebar.title("Theme Settings")

# Theme mode
mode = st.sidebar.radio(
    "Color theme",
    options=["auto", "light", "dark"],
    format_func=lambda x: {"auto": "Auto (OS)", "light": "Light", "dark": "Dark"}[x],
    index=["auto", "light", "dark"].index(st.session_state.theme_mode),
    help="Auto follows your operating system preference",
)

# Accent colors
st.sidebar.markdown("**Accent color**")
palette = {
    "Blue": "#3b82f6",
    "Indigo": "#6366f1",
    "Violet": "#8b5cf6",
    "Teal": "#14b8a6",
    "Emerald": "#10b981",
    "Amber": "#f59e0b",
    "Rose": "#f43f5e",
}
accent_choice = st.sidebar.selectbox(
    "Preset",
    options=list(palette.keys()),
    index=(
        list(palette.values()).index(st.session_state.accent)
        if st.session_state.accent in palette.values()
        else 0
    ),
)
custom_hex = st.sidebar.text_input("Or custom HEX", value=st.session_state.accent)

# Density and font scale
density = st.sidebar.radio(
    "Density",
    options=["compact", "normal", "spacious"],
    index=["compact", "normal", "spacious"].index(st.session_state.density),
)
font_scale = st.sidebar.radio(
    "Font size",
    options=["xs", "sm", "base", "lg", "xl"],
    index=["xs", "sm", "base", "lg", "xl"].index(st.session_state.font_scale),
)

st.sidebar.markdown("---")

# Role switcher (for testing)
role = st.sidebar.selectbox(
    "Role (for preview/testing)",
    options=["guest", "PC", "Professor", "Team"],
    index=["guest", "PC", "Professor", "Team"].index(st.session_state.role),
)
st.sidebar.caption("This only changes the session role for preview purposes.")

# Apply changes immediately
new_accent = palette.get(accent_choice, "#3b82f6")
if custom_hex.strip().startswith("#") and len(custom_hex.strip()) in (4, 7):
    new_accent = custom_hex.strip()

if (
    mode != st.session_state.theme_mode
    or new_accent != st.session_state.accent
    or density != st.session_state.density
    or font_scale != st.session_state.font_scale
    or role != st.session_state.role
):
    st.session_state.theme_mode = mode
    st.session_state.accent = new_accent
    st.session_state.density = density
    st.session_state.font_scale = font_scale
    st.session_state.role = role
    st.markdown(
        theme_css(mode, new_accent, font_scale, density), unsafe_allow_html=True
    )

# Reset button
if st.sidebar.button("Reset to defaults"):
    st.session_state.theme_mode = "auto"
    st.session_state.accent = "#3b82f6"
    st.session_state.font_scale = "base"
    st.session_state.density = "normal"
    st.session_state.role = "guest"
    st.markdown(theme_css("auto", "#3b82f6", "base", "normal"), unsafe_allow_html=True)
    st.toast("Settings reset")

# =========================
# Main Content
# =========================
st.title("Settings")
st.write(
    f"You are logged in as **{st.session_state.role}**.  "
    f"<span class='badge'>theme: {st.session_state.theme_mode}</span>  "
    f"<span class='badge'>accent: {st.session_state.accent}</span>  "
    f"<span class='badge'>density: {st.session_state.density}</span>  "
    f"<span class='badge'>font: {st.session_state.font_scale}</span>",
    unsafe_allow_html=True,
)

st.markdown("---")

# =========================
# Live Preview Section
# =========================
st.subheader("Live Preview")

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**Buttons & Inputs**")
    st.text_input("Project name", value="Urban Crime Dynamics")
    st.selectbox("City", ["CDMX", "GDL", "MTY"], index=0)
    st.number_input(
        "Confidence threshold", min_value=0.0, max_value=1.0, step=0.05, value=0.85
    )
    st.button("Run pipeline")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**KPI Cards**")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Incidents (24h)", 124, delta="+12")
    with c2:
        st.metric("AUC (last model)", "0.87", delta="+0.02")
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("**Status**  \nModel registry and dashboards ready.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption(
    "All changes are stored in `st.session_state` and applied immediately through CSS tokens."
)
