import streamlit as st
import math
import uuid
import folium
from streamlit_folium import st_folium
from deep_translator import GoogleTranslator

st.set_page_config(page_title="⚓ Deniz Radar AI", layout="wide")

class Gemi:
    def __init__(self, gemi_id, kaptan, lat, lon, dil):
        self.gemi_id = gemi_id
        self.kaptan = kaptan
        self.lat = lat
        self.lon = lon
        self.dil = dil

def mesafe_hesapla(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def ceviri_yap(metin, kaynak, hedef):
    try:
        if not metin.strip():
            return ""
        return GoogleTranslator(source=kaynak, target=hedef).translate(metin)
    except Exception as e:
        return f"(Çeviri başarısız)"

# SESSION
if "gemiler" not in st.session_state:
    st.session_state.gemiler = [
        Gemi(1, "Kaptan Ahmet", 41.01, 28.95, "tr"),
        Gemi(2, "Captain John", 41.05, 28.90, "en"),
    ]

if "chat_odasi" not in st.session_state:
    st.session_state.chat_odasi = {}
if "aktif_oda" in st.session_state and st.session_state.aktif_oda not in st.session_state.chat_odasi:
    del st.session_state.aktif_oda
    if "karsi_dil" in st.session_state:
        del st.session_state.karsi_dil
st.title("⚓ Deniz Radar AI")

menzil = st.sidebar.slider("Radar Menzili", 1, 50, 15)

k_lat = st.number_input("Enlem", value=41.00)
k_lon = st.number_input("Boylam", value=28.95)
kullanici_dil = st.selectbox("Dil", ["tr", "en"])

harita = folium.Map(location=[k_lat, k_lon], zoom_start=9)

for gemi in st.session_state.gemiler:
    mesafe = mesafe_hesapla(k_lat, k_lon, gemi.lat, gemi.lon)
    if mesafe <= menzil:

        folium.Marker(
            [gemi.lat, gemi.lon],
            popup=f"{gemi.kaptan} ({mesafe:.2f} km)",
            icon=folium.Icon(color="red")
        ).add_to(harita)

        if st.button(f"{gemi.kaptan} ile konuş", key=gemi.gemi_id):
            oda = str(uuid.uuid4())
            st.session_state.chat_odasi[oda] = []
            st.session_state.aktif_oda = oda
            st.session_state.karsi_dil = gemi.dil

st_folium(harita)

if "aktif_oda" in st.session_state:
    mesaj = st.text_input("Mesaj")

    if st.button("Gönder") and mesaj.strip():
        hedef = st.session_state.karsi_dil
        if hedef != kullanici_dil:
            ceviri = ceviri_yap(mesaj, kullanici_dil, hedef)
            kayit = f"Sen: {mesaj} → {ceviri}"
        else:
            kayit = f"Sen: {mesaj}"

        st.session_state.chat_odasi[st.session_state.aktif_oda].append(kayit)

    for m in st.session_state.chat_odasi[st.session_state.aktif_oda]:
        st.write("📨", m)