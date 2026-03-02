# =========================================
# 🚢 SHIP CHAT SYSTEM - FINAL WORKING APP
# =========================================

import streamlit as st
from supabase import create_client
import uuid, math, folium, time, html
from datetime import datetime
from pathlib import Path
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# =========================================
# 🔹 SUPABASE
# =========================================
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
OPENAI_KEY = os.environ.get("OPENAI_KEY")

try:
    if not SUPABASE_URL and "SUPABASE_URL" in st.secrets:
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
    if not SUPABASE_KEY and "SUPABASE_KEY" in st.secrets:
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    if not OPENAI_KEY and "OPENAI_KEY" in st.secrets:
        OPENAI_KEY = st.secrets["OPENAI_KEY"]
except Exception:
    pass

# Fallbacks for local testing if not provided in env docs
if not SUPABASE_URL:
    SUPABASE_URL = "https://fdqbwszbiespnxgpmbam.supabase.co"
if not SUPABASE_KEY:
    SUPABASE_KEY = "sb_publishable_5mphuTJ4NLXUNvGmgjf7Iw_1gmhIFE7"
if not OPENAI_KEY:
    OPENAI_KEY = ""

st.set_page_config(
    page_title="Deniz Radar | Ship Chat",
    page_icon="⚓",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Global Background and Typography (Coastal Luxury) */
    html, body, .stApp, h1, h2, h3, p, span, div, label { 
        font-family: 'Outfit', -apple-system, sans-serif; 
    }
    /* Explicitly protect Streamlit's material icons from being overridden */
    span.material-symbols-rounded, .material-icons, i, svg text {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }
    
    /* Global Background and Typography (Coastal Luxury) */
    .appview-container { 
        background: linear-gradient(135deg, #e0f2fe 0%, #f1f5f9 50%, #dbeafe 100%) !important; 
        background-attachment: fixed !important;
    }
    .block-container { 
        padding-top: 2rem; 
        padding-bottom: 7rem; 
        max-width: 480px; 
    }
    header, footer { visibility: hidden; height: 0; }
    #MainMenu { visibility: hidden; }
    
    h1, h2, h3 { 
        color: #0f172a; /* Deep Navy Blue for headings */
        letter-spacing: -0.03em; 
        font-weight: 700; 
    }
    p, label, .stTextInput label, .stNumberInput label, .stSelectbox label { 
        color: #475569 !important; /* Slate Gray */
        font-weight: 500; 
        font-size: 14px;
    }
    
    /* Cards (Bright Frosted Glassmorphism) */
    .card {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(32px);
        -webkit-backdrop-filter: blur(32px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-bottom: 1px solid rgba(255, 255, 255, 0.4);
        border-right: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 10px 40px rgba(15, 23, 42, 0.04);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 50px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(255, 255, 255, 1);
    }
    
    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(2, 132, 199, 0.2));
        color: #0284c7; /* Ocean Blue */
        border: 1px solid rgba(14, 165, 233, 0.25);
        margin-right: 8px;
    }
    
    /* Standard Buttons */
    .stButton button {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important; /* Ocean blue gradient */
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.8rem 1.6rem !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important; 
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(2, 132, 199, 0.35) !important;
    }
    .stButton button:active {
        transform: translateY(0) !important;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.2) !important;
    }
    
    /* Text secondary style button overrides */
    div[data-testid="stFormSubmitButton"] button, 
    .stButton button[kind="secondary"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        color: #334155 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover, 
    .stButton button[kind="secondary"]:hover {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        padding: 0.8rem 1rem !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.15) !important;
        background: #ffffff !important;
    }
    
    .stSuccess, .stError, .stWarning { 
        border-radius: 16px !important; 
        font-weight: 600;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 1) !important;
        color: #0f172a !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
    }
    
    .section-title { 
        font-size: 15px; 
        font-weight: 600; 
        margin-bottom: 16px; 
        margin-top: 8px;
        color: #64748b; 
        text-transform: uppercase;
        letter-spacing: 0.08em; 
    }
    .soft-text { color: #64748b; font-size: 14px; line-height: 1.6; }
    
    /* Hero Section */
    .hero {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 12px;
    }
    .hero-title { font-size: 26px; font-weight: 700; margin: 0; color: #0284c7; letter-spacing: -0.03em; }
    .hero-sub { font-size: 14px; color: #64748b; margin-top: 6px; font-weight: 400;}
    
    /* Chips */
    .chip {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
        background: rgba(14, 165, 233, 0.1);
        color: #0284c7;
        border: 1px solid rgba(14, 165, 233, 0.15);
        transition: background 0.2s;
    }
    .chip:hover {
        background: rgba(14, 165, 233, 0.2);
    }
    
    /* KPI Stats Grid */
    .stat-grid, .home-kpi { 
        display: grid; 
        grid-template-columns: repeat(2, 1fr); 
        gap: 16px; 
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 20px;
        padding: 20px;
        transition: transform 0.2s ease, background 0.2s;
        box-shadow: 0 6px 24px rgba(15, 23, 42, 0.04);
    }
    .stat-card:hover {
        background: rgba(255, 255, 255, 0.95);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    }
    .stat-label { font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;}
    .stat-value { font-size: 28px; font-weight: 700; color: #0f172a; letter-spacing: -0.02em; }
    
    .filter-row { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
    
    /* Ship List Cards */
    .ship-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 14px;
        padding: 16px 20px;
        border-radius: 18px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .ship-card:hover {
        border-color: #bae6fd;
        box-shadow: 0 6px 16px rgba(14, 165, 233, 0.1);
        transform: translateX(4px);
    }
    .ship-title { font-weight: 600; color: #0f172a; font-size: 16px; margin-bottom: 2px; }
    .ship-sub { font-size: 13px; color: #64748b; }
    
    .home-hero { background: rgba(255, 255, 255, 0.8); }
    
    /* Expanders */
    div[data-testid="stExpander"] > details {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 12px 18px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(15,23,42,0.02);
    }
    div[data-testid="stExpander"] > details:hover {
        background: #ffffff;
        border-color: #e2e8f0;
    }
    div[data-testid="stExpander"] > details > summary {
        list-style: none;
        cursor: pointer;
        color: #0f172a;
        font-weight: 600;
        font-size: 15px;
        padding: 4px 0;
    }
    div[data-testid="stExpander"] > details > summary svg {
        margin-right: 8px;
        color: #475569 !important;
        fill: #475569 !important;
    }
    div[data-testid="stExpander"] > details[open] {
        background: #ffffff;
        border-color: #cbd5e1;
        box-shadow: 0 8px 24px rgba(15,23,42,0.06);
    }
    
    /* Chat UI - Modernized for Light Theme */
    .chat-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-radius: 28px 28px 0 0;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 1);
        border-bottom: none;
        box-shadow: 0 -8px 40px rgba(15,23,42,0.05);
    }
    .chat-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 18px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #f1f5f9;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .chat-header-title { font-weight: 700; color: #0f172a; font-size: 17px; letter-spacing: -0.01em;}
    .chat-header-status { 
        font-size: 13px; 
        color: #10b981; 
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .chat-header-status::before {
        content: '';
        display: block;
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        animation: pulse 2s infinite;
    }
    
    .chat-messages {
        padding: 24px;
        min-height: 400px;
        max-height: 480px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
    }
    /* Scrollbar for chat */
    .chat-messages::-webkit-scrollbar { width: 6px; }
    .chat-messages::-webkit-scrollbar-track { background: transparent; }
    .chat-messages::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    
    .chat-row { display: flex; margin-bottom: 12px; width: 100%;}
    .chat-row.me { justify-content: flex-end; }
    .chat-row.other { justify-content: flex-start; }
    
    .chat-bubble {
        max-width: 80%;
        padding: 14px 18px;
        border-radius: 22px;
        font-size: 15px;
        line-height: 1.5;
        position: relative;
        word-wrap: break-word;
        box-shadow: 0 4px 12px rgba(15,23,42,0.04);
        animation: fadeIn 0.3s ease-out forwards;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-bubble.me {
        background: linear-gradient(135deg, #0ea5e9, #0284c7); /* Sea blue */
        color: #ffffff;
        border-bottom-right-radius: 6px;
    }
    .chat-bubble.other {
        background: #ffffff;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 6px;
    }
    .chat-bubble .chat-time {
        font-size: 11px;
        color: rgba(255,255,255,0.8);
        margin-top: 6px;
        text-align: right;
        font-weight: 500;
    }
    .chat-bubble.other .chat-time { color: #64748b; }
    
    .chat-input-wrap {
        padding: 0 24px 18px 24px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 1);
        border-top: none;
        border-radius: 0 0 28px 28px;
        margin-top: -1px;
        box-shadow: 0 8px 32px rgba(15,23,42,0.08);
    }
    
    .nav-pill {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        margin-right: 8px;
        border-radius: 999px;
        background: rgba(14, 165, 233, 0.1);
        color: #0284c7;
        border: 1px solid rgba(14, 165, 233, 0.15);
        font-size: 13px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .nav-pill:hover {
        background: rgba(14, 165, 233, 0.15);
        transform: translateY(-1px);
    }
    
    /* Bottom Navigation - Floating Glass Navigation Light Mode */
    div[data-testid="stRadio"] > div {
        position: fixed;
        left: 50%;
        transform: translateX(-50%);
        bottom: 24px;
        width: calc(100% - 40px);
        max-width: 400px;
        z-index: 50;
        padding: 8px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 28px;
        display: flex;
        justify-content: space-between;
        gap: 8px;
        box-shadow: 0 12px 40px rgba(15,23,42,0.12);
    }
    div[data-testid="stRadio"] label {
        background: transparent;
        border-radius: 20px;
        padding: 12px 14px;
        border: none;
        color: #64748b;
        font-weight: 600;
        font-size: 14px;
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }
    /* Hide the default radio circle completely */
    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] label [data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        text-align: center !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
    }
    div[data-testid="stRadio"] label:hover {
        color: #0f172a;
        background: rgba(15, 23, 42, 0.04);
    }
    div[data-testid="stRadio"] label input:checked + div,
    div[data-testid="stRadio"] label:has(input:checked) {
        background: #ffffff;
        color: #0284c7; /* Ocean blue active state */
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(15,23,42,0.06);
        border: 1px solid #e0f2fe;
    }
    
    /* Ensure Streamlit elements that inject backgrounds adapt */
    .stSelectbox div[data-baseweb="popover"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .stSelectbox div[data-baseweb="popover"] li:hover {
        background: #f1f5f9;
        color: #0ea5e9;
    }
    
    @media (max-width: 768px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; padding-bottom: 8rem; }
        .stButton button { width: 100%; }
        .stat-grid, .home-kpi { grid-template-columns: 1fr; gap: 12px;}
        .filter-row { grid-template-columns: 1fr; gap: 12px; }
        section[data-testid="stSidebar"] { display: none; }
        
        .chat-container { border-radius: 20px 20px 0 0; }
        .chat-input-wrap { border-radius: 0 0 20px 20px; padding: 14px; }
        .chat-messages { padding: 16px; min-height: 300px; max-height: 400px;}
    }
</style>
""", unsafe_allow_html=True)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Oturum token'larını sakla (RLS için her sayfa yüklemesinde auth gerekli)
if "sb_access_token" not in st.session_state:
    st.session_state.sb_access_token = None
if "sb_refresh_token" not in st.session_state:
    st.session_state.sb_refresh_token = None
TEMPLATES_DIR = Path(__file__).parent / "templates"

def render_template(name, **kwargs):
    path = TEMPLATES_DIR / name
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8")
    if kwargs:
        try:
            content = content.format(**kwargs)
        except KeyError:
            pass
    return content

st.markdown(render_template("app_header.html"), unsafe_allow_html=True)

# =========================================
# 🔹 MESAFE
# =========================================
def mesafe(a,b,c,d):
    R=6371
    return 2*R*math.asin(math.sqrt(
        math.sin(math.radians(c-a)/2)**2 +
        math.cos(math.radians(a))*math.cos(math.radians(c))*
        math.sin(math.radians(d-b)/2)**2
    ))

def format_ts(ts):
    if not ts:
        return ""
    try:
        if isinstance(ts, str):
            ts = ts.replace("Z", "+00:00")
            dt = datetime.fromisoformat(ts)
        elif isinstance(ts, datetime):
            dt = ts
        else:
            return ""
        return dt.strftime("%H:%M")
    except Exception:
        return ""

# =========================================
# 🔹 LOGIN
# =========================================
if "user" not in st.session_state:
    st.session_state.user=None
if "page" not in st.session_state:
    st.session_state.page = "Home"

if not st.session_state.user:
    # ⚓ Premium Landing / Hero Header
    st.markdown("""
        <div style='text-align: center; margin: 2rem 0 2.5rem 0;'>
            <div style='font-size: 3.5rem; filter: drop-shadow(0 4px 12px rgba(56, 189, 248, 0.4)); margin-bottom: 8px;'>⚓</div>
            <h1 style='font-size: 2.6rem; letter-spacing: -0.04em; margin-bottom: 6px; background: linear-gradient(135deg, #0284c7, #0ea5e9); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Deniz Radar</h1>
            <p style='color: #64748b; font-size: 1.05rem; margin-top: 0; font-weight: 500;'>Kaptanların güvenli ve hızlı iletişim ağı.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="card" style="margin: 0 auto; padding: 28px;">', unsafe_allow_html=True)
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"
        
    st.markdown('<div style="display:flex; gap:8px; margin-bottom: 24px;">', unsafe_allow_html=True)
    col_t1, col_t2, col_t3 = st.columns(3)
    def set_auth(mode):
        st.session_state.auth_mode = mode
    
    with col_t1:
        if st.button("Giriş Yap", key="btn_tab_login", type="primary" if st.session_state.auth_mode == "login" else "secondary", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()
    with col_t2:
        if st.button("Kayıt Ol", key="btn_tab_signup", type="primary" if st.session_state.auth_mode == "signup" else "secondary", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.rerun()
    with col_t3:
        if st.button("Şifre Sıfırla", key="btn_tab_reset", type="primary" if st.session_state.auth_mode == "reset" else "secondary", use_container_width=True):
            st.session_state.auth_mode = "reset"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.auth_mode == "login":
        st.markdown('<div style="margin-bottom: 20px;"><div class="hero-title" style="font-size: 22px;">Tekrar Hoşgeldin</div><div class="hero-sub">Radara bağlanmak için giriş yap.</div></div>', unsafe_allow_html=True)
        email_login = st.text_input("Email", key="login_email")
        pw_login = st.text_input("Şifre", type="password", key="login_pw")
        email_login_clean = email_login.strip().lower()
        pw_login_clean = pw_login.strip()
        remember_me = st.checkbox("Beni Hatırla", value=True, key="login_remember")

        st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
        if st.button("Sisteme Giriş Yap", key="login_btn"):
            try:
                if not email_login_clean or not pw_login_clean:
                    st.error("Email ve şifre gerekli.")
                else:
                    r = supabase.auth.sign_in_with_password({
                        "email": email_login_clean,
                        "password": pw_login_clean
                    })
                    if not r.user:
                        st.error("Giriş başarısız. Bilgilerini kontrol et.")
                    elif r.session:
                        st.session_state.user = r.user
                        st.session_state.sb_access_token = r.session.access_token
                        st.session_state.sb_refresh_token = r.session.refresh_token
                        st.session_state.page = "Home"
                        st.rerun()
            except Exception as e:
                msg = str(e)
                if "Email not confirmed" in msg:
                    st.error("Email doğrulanmamış. Lütfen mailini doğrula.")
                elif "Invalid login credentials" in msg:
                    st.error("Email/şifre hatalı.")
                else:
                    st.error(e)
                    
    elif st.session_state.auth_mode == "signup":
        st.markdown('<div style="margin-bottom: 20px;"><div class="hero-title" style="font-size: 22px;">Aramıza Katıl</div><div class="hero-sub">Gemini radara ekle ve çevrenle iletişime geç.</div></div>', unsafe_allow_html=True)
        email_signup = st.text_input("Email", key="signup_email")
        pw_signup = st.text_input("Şifre", type="password", key="signup_pw")
        pw2_signup = st.text_input("Şifre (Tekrar)", type="password", key="signup_pw2")
        email_signup_clean = email_signup.strip().lower()
        pw_signup_clean = pw_signup.strip()

        st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
        if st.button("Hesap Oluştur", key="signup_btn"):
            if not email_signup_clean or not pw_signup_clean:
                st.error("Email ve şifre gerekli.")
            elif pw_signup_clean != pw2_signup:
                st.error("Şifreler uyuşmuyor.")
            else:
                try:
                    r = supabase.auth.sign_up({
                        "email": email_signup_clean,
                        "password": pw_signup_clean
                    })
                    # Use r.user safely to check if successful
                    if r.user:
                        if r.session:
                            st.session_state.user = r.user
                            st.session_state.sb_access_token = r.session.access_token
                            st.session_state.sb_refresh_token = r.session.refresh_token
                            st.session_state.page = "Home"
                            st.rerun()
                        else:
                            # User created but no session -> Email Confirmation is required by Supabase settings
                            st.success("Kayıt başarılı! Lütfen email adresinize gelen doğrulama bağlantısına tıklayın.")
                    else:
                        st.error("Kayıt tamamlanamadı.")
                except Exception as e:
                    st.error(str(e))
                    
    elif st.session_state.auth_mode == "reset":
        st.markdown('<div style="margin-bottom: 20px;"><div class="hero-title" style="font-size: 22px;">Şifre Kurtarma</div><div class="hero-sub">Hesabını geri almak için mail adresini gir.</div></div>', unsafe_allow_html=True)
        reset_email = st.text_input("Kayıtlı Email", key="reset_email")
        
        st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
        if st.button("Bağlantı Gönder"):
            try:
                em = reset_email.strip().lower()
                if not em:
                    st.error("Email gerekli.")
                else:
                    supabase.auth.reset_password_for_email(em)
                    st.success("Sıfırlama bağlantısı gönderildi!")
                    time.sleep(1.5)
                    st.rerun()
            except Exception as e:
                st.error(str(e))
                
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

user = st.session_state.user

# RLS için oturum token'ını Supabase client'a her sayfa yüklemesinde ver
if st.session_state.sb_access_token and st.session_state.sb_refresh_token:
    try:
        supabase.auth.set_session(st.session_state.sb_access_token, st.session_state.sb_refresh_token)
    except Exception:
        pass

# Preload ship data for badges and labels
ships = supabase.table("ships").select("*").execute().data
captain_by_user = {str(s["user_id"]): s["captain"] for s in ships}
pending_invites = supabase.table("invites")\
    .select("*")\
    .eq("to_user", user.id)\
    .eq("status", "pending")\
    .execute().data
own_ship = next((s for s in ships if str(s["user_id"]) == str(user.id)), None)

# Kabul edilmiş davetler = kalıcı konuşmalar (hem gönderdiğim hem aldığım)
inv_from = supabase.table("invites").select("*").eq("from_user", user.id).eq("status", "accepted").execute().data
inv_to = supabase.table("invites").select("*").eq("to_user", user.id).eq("status", "accepted").execute().data
accepted_invites = (inv_from or []) + (inv_to or [])
# Partner'a göre tek konuşma (aynı kişi birden fazla kez görünmesin)
conversations = {}
for inv in accepted_invites:
    rid = inv.get("room_id")
    if not rid:
        continue
    other_id = str(inv["to_user"]) if str(inv["from_user"]) == str(user.id) else str(inv["from_user"])
    partner_name = captain_by_user.get(other_id, "Kaptan")
    if other_id not in conversations:
        conversations[other_id] = {"room_id": rid, "partner": partner_name}

room_to_conv = {c["room_id"]: c for c in conversations.values()}

# =========================================
# 🔹 NAV
# =========================================
home_badge = f" 🔴{len(pending_invites)}" if len(pending_invites) > 0 else ""
chat_badge = f" 🔴{len(conversations)}" if conversations else ""
pages = ["Home", "Harita", "Chat"]
labels = [f"🏠 Home{home_badge}", "🗺️ Harita", f"💬 Chat{chat_badge}"]
label_to_page = dict(zip(labels, pages))
nav = st.radio(
    "Navigasyon",
    labels,
    index=pages.index(st.session_state.page),
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.page = label_to_page.get(nav, "Home")
current_page = st.session_state.page

if current_page == "Home":
    st.markdown(render_template("home.html"), unsafe_allow_html=True)

    invites = pending_invites
    nearby_count = 0
    if own_ship:
        for s in ships:
            if str(s["user_id"]) == str(user.id):
                continue
            d = mesafe(own_ship["lat"], own_ship["lon"], s["lat"], s["lon"])
            if d <= 25:
                nearby_count += 1

    # Özet başlığını kaldırdım, template içindeki yeni ui tasarımı zaten yeterli
    st.markdown(
        render_template(
            "home_summary.html",
            nearby_count=nearby_count,
            invite_count=len(invites),
            active_room="Var" if "room" in st.session_state else "Yok"
        ),
        unsafe_allow_html=True
    )

    activity_items = []
    recent_msgs = supabase.table("messages")\
        .select("*")\
        .eq("sender", user.id)\
        .order("created_at", desc=True)\
        .limit(5)\
        .execute().data
    if recent_msgs:
        for m in recent_msgs:
            t = format_ts(m.get("created_at"))
            activity_items.append(f"• {t} — {m.get('message', '')}")
    else:
        activity_items.append("Henüz aktivite yok.")
    st.markdown(
        render_template(
            "home_activity.html",
            activity_items="<br/>".join(activity_items)
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        render_template(
            "home_profile.html",
            user_id=user.id,
            active_ship=own_ship["captain"] if own_ship else "Kayıt yok"
        ),
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-title" id="shortcut-section" style="margin-top: 32px; font-size: 16px;">Hızlı Kısayollar</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("🗺️ Harita", key="shortcut_map"):
            st.session_state.page = "Harita"
            st.rerun()
    with col_b:
        if st.button("💬 Chat", key="shortcut_chat"):
            st.session_state.page = "Chat"
            st.rerun()
    with col_c:
        if st.button("📨 Davetler", key="shortcut_invites"):
            st.session_state.page = "Home"
            st.rerun()
            
    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    if st.button("🚪 Çıkış Yap", key="home_logout", type="secondary", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# =========================================
# 🔹 GPS
# =========================================
if "gps_requested" not in st.session_state:
    st.session_state.gps_requested = False
if current_page in ["Home", "Harita"] and st.session_state.gps_requested:
    components.html("""
<script>
navigator.geolocation.getCurrentPosition((pos)=>{
  var lat=pos.coords.latitude, lon=pos.coords.longitude;
  var u=new URL(window.parent.location.href);
  u.searchParams.set('lat',lat);
  u.searchParams.set('lon',lon);
  window.parent.location.href=u.toString();
}, ()=>{});
</script>
<span style="color:#94a3b8;">Konum alınıyor...</span>
""", height=40)

# URL'den konum (GPS ile güncellenmiş)
qp = st.query_params
lat_default = float(qp.get("lat")) if qp.get("lat") else 41.0
lon_default = float(qp.get("lon")) if qp.get("lon") else 29.0

if current_page in ["Home", "Harita"]:
    st.markdown('<div class="section-title">Konum & Radar Ayarları</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    loc_col1, loc_col2 = st.columns([3, 1])
    with loc_col1:
        lat = st.number_input("Enlem", value=lat_default, format="%.6f")
        lon = st.number_input("Boylam", value=lon_default, format="%.6f")
    with loc_col2:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("📍 Konumum Al"):
            st.session_state.gps_requested = True
            st.rerun()
    menzil_km = st.slider("Radar Menzili (km)", 1, 100, 25)
    zoom = st.slider("Harita Yakınlığı", 5, 12, 7)
    st.markdown('<div class="soft-text">İpucu: Mobil kullanımda menzili 15-30 km aralığında tut.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    lat = 41.0
    lon = 29.0
    menzil_km = 25
    zoom = 7

# =========================================
# 🔹 SHIP EKLE / GÜNCELLE / SİL
# =========================================
if current_page == "Home":
    st.markdown('<div class="section-title">🚢 Gemi Kaydet</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if own_ship:
        name = st.text_input("Kaptan", value=own_ship.get("captain", ""), key="ship_edit_name")
        safe_lat = float(own_ship.get("lat") or 41.0)
        safe_lon = float(own_ship.get("lon") or 29.0)
        edit_lat = st.number_input("Enlem", value=safe_lat, format="%.6f", key="ship_edit_lat")
        edit_lon = st.number_input("Boylam", value=safe_lon, format="%.6f", key="ship_edit_lon")
        col_upd, col_del = st.columns(2)
        with col_upd:
            if st.button("Güncelle"):
                supabase.table("ships").update({
                    "captain": name,
                    "lat": edit_lat,
                    "lon": edit_lon
                }).eq("id", own_ship["id"]).eq("user_id", user.id).execute()
                st.success("Gemi güncellendi")
                time.sleep(1.5)
                st.rerun()
        with col_del:
            if st.button("Gemi Sil", type="secondary"):
                supabase.table("ships").delete().eq("id", own_ship["id"]).eq("user_id", user.id).execute()
                st.success("Gemi silindi")
                time.sleep(1.5)
                st.rerun()
    else:
        name = st.text_input("Kaptan")
        if st.button("Ship Kaydet"):
            supabase.table("ships").insert({
                "captain": name,
                "lat": lat,
                "lon": lon,
                "user_id": user.id
            }).execute()
            st.success("Ship kaydedildi")
            time.sleep(1.5)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    name = ""

# =========================================
# 🔹 HARİTA
# =========================================
if current_page == "Harita":
    st.markdown(render_template("map.html"), unsafe_allow_html=True)
    st.markdown(render_template("map_filter.html"), unsafe_allow_html=True)
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        filter_menzil = st.slider("Menzil (km)", 1, 100, menzil_km)
    with filter_col2:
        filter_only_near = st.checkbox("Sadece Yakınlar", value=True)
    st.markdown('<div class="section-title">🗺️ Radar</div>', unsafe_allow_html=True)

    m = folium.Map(location=[lat, lon], zoom_start=zoom)
    nearby = []

    for s in ships:
        d = mesafe(lat, lon, s["lat"], s["lon"])
        limit = filter_menzil if filter_only_near else 10_000
        if d <= limit:
            nearby.append({
                "captain": s["captain"],
                "distance": d,
                "is_self": s["user_id"] == user.id
            })
            color = "blue" if s["user_id"] == user.id else "red"
            folium.Marker(
                [s["lat"], s["lon"]],
                popup=f"{s['captain']} • {d:.1f} km",
                icon=folium.Icon(color=color)
            ).add_to(m)

    st.markdown(
        render_template(
            "map_floating.html",
            menzil_km=filter_menzil,
            nearby_count=len(nearby)
        ),
        unsafe_allow_html=True
    )
    st_folium(m, use_container_width=True, height=480)

    if nearby:
        nearby_items = []
        for item in sorted(nearby, key=lambda x: x["distance"]):
            tag = " (Sen)" if item["is_self"] else ""
            nearby_items.append(f"<div><strong>{item['captain']}</strong>{tag} • {item['distance']:.1f} km</div>")
        nearby_html = "<br/>".join(nearby_items)
        cards_html = "<div class='soft-text'>Aşağıdaki listeden hızlı davet gönderebilirsin.</div>"
    else:
        nearby_html = "Radar menzili içinde gemi yok."
        cards_html = "Menzil içinde önerilecek gemi yok."
    st.markdown(
        render_template("map_list.html", nearby_items=nearby_html),
        unsafe_allow_html=True
    )
    st.markdown(
        render_template("map_cards.html", ship_cards=cards_html),
        unsafe_allow_html=True
    )
    if nearby:
        for item in sorted(nearby, key=lambda x: x["distance"]):
            if item["is_self"]:
                continue
            with st.expander(f"🚢 {item['captain']} • {item['distance']:.1f} km"):
                st.markdown(
                    f"<div class='ship-card' style='margin-top: 8px;'><div><div class='ship-title'>{item['captain']}</div>"
                    f"<div class='ship-sub'>{item['distance']:.1f} km uzaklıkta</div></div></div>",
                    unsafe_allow_html=True
                )
                st.write("Detaylar: Menzil içinde ve davet edilebilir.")
                target = next((s for s in ships if str(s.get("captain","")) == str(item.get("captain",""))), None)
                if target:
                    existing_room = conversations.get(str(target["user_id"]), {}).get("room_id")
                    btn_text = "💬 Sohbete Git" if existing_room else "Davet Et"
                    if st.button(btn_text, key=f"card-invite-{item['captain']}-{item['distance']:.2f}"):
                        if existing_room:
                            st.session_state.room = existing_room
                            st.session_state.chat_partner = target["captain"]
                            st.session_state.page = "Chat"
                            st.rerun()
                        else:
                            try:
                                supabase.table("invites").insert({
                                    "from_user": str(user.id),
                                    "to_user": str(target["user_id"]),
                                    "room_id": str(uuid.uuid4()),
                                    "status": "pending"
                                }).execute()
                                st.success("Davet gönderildi")
                                time.sleep(1.5)
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Davet gönderilemedi: {ex}")

    st.markdown('<div class="section-title">📨 Hızlı Davet</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    invited_any = False
    for s in ships:
        d = mesafe(lat, lon, s["lat"], s["lon"])
        if str(s["user_id"]) != str(user.id) and d <= menzil_km:
            invited_any = True
            existing_room = conversations.get(str(s["user_id"]), {}).get("room_id")
            btn_text = f"💬 {s['captain']} ile sohbet" if existing_room else f"{s['captain']} Davet Et"
            if st.button(btn_text, key=f"harita-{s['id']}"):
                if existing_room:
                    st.session_state.room = existing_room
                    st.session_state.chat_partner = s["captain"]
                    st.session_state.page = "Chat"
                    st.rerun()
                else:
                    try:
                        supabase.table("invites").insert({
                            "from_user": str(user.id),
                            "to_user": str(s["user_id"]),
                            "room_id": str(uuid.uuid4()),
                            "status": "pending"
                        }).execute()
                        st.success("Davet gönderildi")
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Davet gönderilemedi: {ex}")
    if not invited_any:
        st.write("Menzil içinde davet edilecek gemi yok.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        render_template("map_legend.html", menzil_km=menzil_km),
        unsafe_allow_html=True
    )

# =========================================
# 🔹 DAVET GÖNDER
# =========================================
if current_page == "Home":
    st.markdown(render_template("invites.html"), unsafe_allow_html=True)
    st.markdown('<div class="section-title">📨 Davet Gönder</div>', unsafe_allow_html=True)

    for s in ships:
        if str(s["user_id"]) != str(user.id):
            existing_room = conversations.get(str(s["user_id"]), {}).get("room_id")
            btn_text = "💬 Sohbete Git" if existing_room else f"{s['captain']} Davet Et"
            if st.button(btn_text, key=str(s["id"])):
                if existing_room:
                    st.session_state.room = existing_room
                    st.session_state.chat_partner = captain_by_user.get(str(s["user_id"]), "Kaptan")
                    st.session_state.page = "Chat"
                    st.rerun()
                else:
                    try:
                        supabase.table("invites").insert({
                            "from_user": str(user.id),
                            "to_user": str(s["user_id"]),
                            "room_id": str(uuid.uuid4()),
                            "status": "pending"
                        }).execute()
                        st.success("Davet gönderildi")
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Davet gönderilemedi: {ex}")

    # =========================================
    # 🔹 GELEN DAVETLER
    # =========================================
    st.markdown('<div class="section-title">📥 Gelen Davetler</div>', unsafe_allow_html=True)

    invites = pending_invites

    for i in invites:
        col1, col2, col3 = st.columns([3,1,1])
        from_name = captain_by_user.get(str(i["from_user"]), "Bir kullanıcı")
        col1.write(f"{from_name} seni davet etti")

        if col2.button("Kabul", key=str(i["id"])+"k"):
            supabase.table("invites").update({"status": "accepted"}).eq("id", i["id"]).execute()
            rid = i.get("room_id")
            if rid:
                st.session_state.room = rid
                st.session_state.chat_partner = captain_by_user.get(str(i["from_user"]), "Kaptan")
                st.session_state.page = "Chat"
                st.success("Bağlandı")
                time.sleep(1.5)
                st.rerun()
            else:
                st.warning("Bu davet için room_id bulunamadı. invites tablosuna room_id kolonu ekleyip daveti yeniden gönder.")

        if col3.button("Reddet", key=str(i["id"])+"r"):
            supabase.table("invites").update({"status": "rejected"}).eq("id", i["id"]).execute()
            st.rerun()

# =========================================
# 🔹 CHAT
# =========================================
if current_page == "Chat":
    if "room" in st.session_state and st.session_state.room:
        # Açık sohbet
        if st.button("← Geri", key="chat_back"):
            st.session_state.room = None
            st.session_state.chat_partner = None
            st.rerun()

        st.markdown(render_template("chat.html"), unsafe_allow_html=True)
        chats = supabase.table("messages")\
            .select("*")\
            .eq("room_id", st.session_state.room)\
            .order("created_at")\
            .execute().data

        partner = st.session_state.get("chat_partner")
        if not partner and st.session_state.room in room_to_conv:
            partner = room_to_conv[st.session_state.room]["partner"]
        if not partner and chats:
            other = next((str(c["sender"]) for c in chats if str(c["sender"]) != str(user.id)), None)
            partner = captain_by_user.get(other, "Kaptan") if other else "Kaptan"
        partner = partner or "Kaptan"

        seen_ids = set()
        msgs_html = []
        for c in chats:
            mid = c.get("id")
            if mid and mid in seen_ids:
                continue
            if mid:
                seen_ids.add(mid)
            is_me = str(c["sender"]) == str(user.id)
            row_class = "me" if is_me else "other"
            bubble_class = "chat-bubble me" if is_me else "chat-bubble other"
            t = format_ts(c.get("created_at"))
            msg_safe = html.escape(str(c.get("message", "")))
            msgs_html.append(
                f'<div class="chat-row {row_class}"><div class="{bubble_class}">'
                f'<div>{msg_safe}</div><div class="chat-time">{t}</div></div></div>'
            )

        partner_safe = html.escape(str(partner))
        msgs_body = "".join(msgs_html) if msgs_html else '<div style="text-align:center;color:#64748b;padding:24px;">Henüz mesaj yok. İlk mesajı sen gönder!</div>'
        chat_html = f'''<div class="chat-container">
            <div class="chat-header">
                <span class="chat-header-title">🛳️ {partner_safe}</span>
                <span class="chat-header-status">● çevrimiçi</span>
            </div>
            <div class="chat-messages">{msgs_body}</div>
        </div>'''
        st.markdown(chat_html, unsafe_allow_html=True)
        
        def send_message_callback():
            msg_text = st.session_state.chat_msg_input
            if msg_text and msg_text.strip():
                try:
                    supabase.table("messages").insert({
                        "room_id": st.session_state.room,
                        "sender": user.id,
                        "message": msg_text.strip()
                    }).execute()
                except Exception:
                    pass
            # Clear input after sending
            st.session_state.chat_msg_input = ""

        st.markdown('<div class="chat-input-wrap" style="margin-top:0;">', unsafe_allow_html=True)
        st.text_input("Mesaj", placeholder="Mesaj yazıp Enter'a basın...", key="chat_msg_input", label_visibility="collapsed", on_change=send_message_callback)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:12px;display:flex;gap:8px;align-items:center;">', unsafe_allow_html=True)
        auto_refresh = st.checkbox("Otomatik yenile (5 sn)", key="chat_auto")
        if st.button("Yenile", key="chat_refresh"):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if auto_refresh:
            time.sleep(5)
            st.rerun()
    elif conversations:
        # Son mesajları çek (konuşma listesinde önizleme için)
        last_msgs = {}
        for rid in {c["room_id"] for c in conversations.values()}:
            r = supabase.table("messages").select("message,created_at,sender").eq("room_id", rid).order("created_at", desc=True).limit(1).execute()
            if r.data and r.data[0]:
                m = r.data[0]
                last_msgs[rid] = {
                    "msg": (m.get("message") or "")[:50] + ("..." if len(str(m.get("message") or "")) > 50 else ""),
                    "is_me": str(m.get("sender")) == str(user.id),
                    "ts": format_ts(m.get("created_at"))
                }
        st.markdown('<div class="section-title">💬 Konuşmalar</div>', unsafe_allow_html=True)
        st.markdown('<div class="soft-text">Devam etmek için bir konuşma seç</div>', unsafe_allow_html=True)
        for pid, conv in conversations.items():
            rid = conv["room_id"]
            lm = last_msgs.get(rid)
            preview = ""
            if lm:
                prefix = "Sen: " if lm["is_me"] else ""
                preview = f" — {prefix}{lm['msg']}"
            btn_label = f"🛳️ {conv['partner']}{preview}"
            if st.button(btn_label, key=f"conv_{pid}"):
                st.session_state.room = rid
                st.session_state.chat_partner = conv["partner"]
                st.rerun()
    else:
        st.info("Önce bir daveti kabul ederek konuşma başlat. Home sayfasından davet gönder veya gelen davetleri kabul et.")

st.sidebar.markdown("### Profil")
st.sidebar.write("User:", str(user.id)[:20] + "...")
st.sidebar.write("Aktif gemi:", own_ship["captain"] if own_ship else "Kayıt yok")
st.sidebar.markdown("---")
if st.sidebar.button("Çıkış yap"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()