# ui_tokens.py
import streamlit as st


def theme_css(
    mode: str,
    accent: str = "#3b82f6",
    font_scale: str = "base",
    density: str = "normal",
) -> str:
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

  /* New tokens */
  --accent: {accent};
  --font-scale: {font_scale_map.get(font_scale, '1.00')};
  --pad-y: {density_map.get(density, '10px')};
}}

@media (prefers-reduced-motion: no-preference) {{
  [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
    transition: background-color .2s ease, color .2s ease, border-color .2s ease;
  }}
}}

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
:root {
  --bg: #0E1117;
  --bg-alt: #151923;
  --fg: #E6E9EF;
  --muted: #a0a3ad;
  --primary: #60a5fa;
  --border: #2a2f3a;
}
""" if mode == "dark" else "")}

/* ===== Apply tokens ===== */
html, body, [data-testid="stAppViewContainer"], .block-container {{
  background: var(--bg);
  color: var(--fg);
  font-size: calc(16px * var(--font-scale));
}}

a, .stMarkdown a {{ color: var(--accent); }}

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
.kpi {{ font-weight:700; font-size: 1.15em; }}
.hr {{ height:1px; background:var(--border); margin: 8px 0 14px 0; }}
</style>
"""


def inject_tokens():
    st.session_state.setdefault("theme_mode", "auto")
    st.session_state.setdefault("accent", "#3b82f6")
    st.session_state.setdefault("font_scale", "base")
    st.session_state.setdefault("density", "normal")
    st.markdown(
        theme_css(
            st.session_state["theme_mode"],
            st.session_state["accent"],
            st.session_state["font_scale"],
            st.session_state["density"],
        ),
        unsafe_allow_html=True,
    )
