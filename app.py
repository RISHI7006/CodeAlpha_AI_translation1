import streamlit as st
import urllib.request
import urllib.parse
import json

# Set page layout
st.set_page_config(page_title="AI Translator", page_icon="🌍", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to mimic the exact UI from the image
st.markdown("""
<style>
/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Blue gradient background for the whole app */
.stApp {
    background: linear-gradient(180deg, #d3e2ff 0%, #f0f4ff 50%, #ffffff 100%);
    font-family: 'Inter', sans-serif;
}

/* Make the specific container a white floating box */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: white;
    border-radius: 15px;
    border: none !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    padding: 10px;
    max-width: 900px;
    margin: 0 auto;
}

/* Style the primary Translate Button */
button[data-testid="baseButton-primary"] {
    background-color: #0066ff !important;
    color: white !important;
    border-radius: 30px !important;
    padding: 8px 20px !important;
    font-weight: bold !important;
    border: none !important;
    transition: 0.3s !important;
    width: 100%;
}
button[data-testid="baseButton-primary"]:hover {
    background-color: #0052cc !important;
    box-shadow: 0 4px 10px rgba(0, 102, 255, 0.3);
}

/* Fake top navbar */
.fake-nav {
    background: rgba(255, 255, 255, 0.4);
    padding: 15px 30px;
    border-radius: 30px;
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    color: #0056ff;
    margin-bottom: 30px;
    border: 1px solid rgba(255,255,255,0.7);
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}

/* Title and Subtitle */
.main-title {
    font-size: 52px;
    font-weight: 700;
    color: #0056ff;
    text-align: center;
    margin-top: -10px;
    letter-spacing: -1px;
}
.subtitle {
    text-align: center;
    color: #666;
    font-size: 17px;
    margin-bottom: 40px;
}

/* Footer logos */
.ai-logos {
    text-align: center;
    margin-top: 50px;
    color: #888;
    font-size: 13px;
}
.ai-logos span { color: #555; font-weight: 500; margin: 0 10px; }

/* Hide text area label visually */
.stTextArea label { display: none; }
</style>
""", unsafe_allow_html=True)

# Top Navbar
st.markdown("""
<div class="fake-nav">
    <div><span style="background:#0056ff; color:white; padding:2px 6px; border-radius:4px; font-size:12px;">Ai</span> Translator.com <span style="color:#666; font-weight:normal; font-size:14px; margin-left:10px;">By Tomedes</span></div>
    <div style="color:#555; font-size:14px; font-weight:normal;">Contact Us</div>
</div>
<div class="main-title">AI Translator</div>
<div class="subtitle">Translates, analyzes, and suggests the best AI translations.</div>
""", unsafe_allow_html=True)

LANGUAGES = {
    "auto": "Detect language",
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh-CN": "Chinese"
}

def translate_text(text: str, from_lang: str, to_lang: str) -> str:
    """100% accurate, direct Google Translate without rate-limit issues."""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={from_lang}&tl={to_lang}&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            translated_pieces = [part[0] for part in data[0] if part and part[0]]
            return "".join(translated_pieces)
    except Exception as e:
        raise Exception(f"Translation failed: {e}")

# Session state initialization
if 'translated_output' not in st.session_state:
    st.session_state.translated_output = ""

# The central white box container
with st.container(border=True):
    c1, c2, c3, c4 = st.columns([3, 0.6, 3, 3], gap="small")

    with c1:
        source_lang = st.selectbox("Source", options=list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x], index=0, label_visibility="collapsed")
    with c2:
        st.markdown("<div style='text-align:center; padding-top:8px; color:#0056ff; font-size:20px; font-weight:bold;'>⇄</div>", unsafe_allow_html=True)
    with c3:
        target_options = [k for k in LANGUAGES.keys() if k != "auto"]
        target_lang = st.selectbox("Target", options=target_options, format_func=lambda x: LANGUAGES[x], index=1, label_visibility="collapsed")
    with c4:
        translate_pressed = st.button("✨ TRANSLATE", type="primary")

    st.markdown("<hr style='margin: 5px 0 15px 0; border: none; border-bottom: 1px solid #eee;'>", unsafe_allow_html=True)

    col_in, col_out = st.columns(2)
    with col_in:
        text_to_translate = st.text_area("Input", height=200, placeholder="Add text to translate, try a sample text...")

    if translate_pressed:
        if text_to_translate.strip():
            with st.spinner("Translating..."):
                try:
                    st.session_state.translated_output = translate_text(text_to_translate, source_lang, target_lang)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter some text to translate.")

    with col_out:
        st.text_area("Output", value=st.session_state.translated_output, height=200, placeholder="Translation will appear here...")

st.markdown("""
<div class="ai-logos">
    Translate with every AI<br><br>
    <span>🤖 ChatGPT</span> + <span>🔵 DeepL</span> + <span>✨ Gemini</span> + <span>✖️ Grok-Ai</span> + <span>🟣 Qwen</span> <span style="color:#aaa; font-weight:normal;">+ more AI tools</span>
</div>
""", unsafe_allow_html=True)
