import re
from pathlib import Path

app_path = Path('app.py')
content = app_path.read_text('utf-8')

new_css = """<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    * { 
        font-family: 'Outfit', -apple-system, sans-serif !important; 
    }
    
    /* Global Background and Typography (Coastal Luxury) */
    .appview-container { 
        background-color: #f4f7f6 !important; /* Soft sand/sea foam base */
        background-image: radial-gradient(circle at top right, rgba(14, 165, 233, 0.1), transparent 500px),
                          radial-gradient(circle at bottom left, rgba(16, 185, 129, 0.05), transparent 500px),
                          radial-gradient(circle at center, rgba(250, 250, 250, 0.8), transparent 800px) !important;
        background-attachment: fixed;
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
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.9);
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
    .hero-title { font-size: 26px; font-weight: 700; margin: 0; color: #0f172a; letter-spacing: -0.03em; }
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
        display: flex;
        align-items: center;
        gap: 8px;
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
        text-align: center;
        transition: all 0.3s ease;
    }
    div[data-testid="stRadio"] label:hover {
        color: #0f172a;
        background: rgba(15, 23, 42, 0.04);
    }
    div[data-testid="stRadio"] label input:checked + div {
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
</style>"""

pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
new_content = pattern.sub(new_css, content)
app_path.write_text(new_content, 'utf-8')
