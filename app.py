import streamlit as st
import pandas as pd

# Konfiguracja strony (żeby dobrze wyglądała na telefonie)
st.set_page_config(page_title="Setter Pro", page_icon="🏗️")

st.title("🏗️ Setter Pro - Asystent Ustawiacza")

# --- BAZA DANYCH ---
defects_info = {
    "Wypływki (Flash)": ["Zmniejsz ciśnienie wtrysku/docisku", "Zwiększ siłę zwarcia", "Obniż temp. stopu", "Wyczyść formę"],
    "Niedolania": ["Zwiększ dawkę/poduszkę", "Zwiększ ciśnienie wtrysku", "Podnieś temp. stopu", "Sprawdź odpowietrzenia"],
    "Wciągi": ["Zwiększ ciśnienie/czas docisku", "Obniż temp. stopu", "Wydłuż chłodzenie"],
    "Ślady spalenia (Diesel)": ["Zmniejsz prędkość wtrysku", "Wyczyść odpowietrzenia", "Zmniejsz dekompresję"],
    "Srebrzenie (Silver)": ["Sprawdź suszenie!", "Obniż temp. stopu", "Zmniejsz obroty ślimaka"],
    "Linie łączenia": ["Podnieś temp. stopu i formy", "Zwiększ prędkość wtrysku"],
    "Deformacje": ["Wydłuż chłodzenie", "Zrównoważ temp. połówek formy", "Zmniejsz docisk"]
}

materials_data = {
    "Materiał": ["PP", "PE-HD", "ABS", "PA6", "PC", "POM", "PS", "PET"],
    "T. Stopu": ["200-260°C", "200-280°C", "220-260°C", "230-280°C", "280-320°C", "190-210°C", "180-260°C", "260-300°C"],
    "T. Formy": ["20-60°C", "20-60°C", "40-80°C", "70-110°C", "80-120°C", "80-120°C", "20-60°C", "120-140°C"],
    "Suszenie": ["Brak", "Brak", "80°C / 3h", "80°C / 4h", "120°C / 4h", "80°C / 2h", "Brak", "160°C / 5h"]
}

# --- NAWIGACJA ---
tab1, tab2, tab3 = st.tabs(["🔍 Diagnostyka", "🧪 Materiały", "🧮 Kalkulator"])

# --- TAB 1: DIAGNOSTYKA ---
with tab1:
    st.subheader("Wybierz defekt z listy:")
    defect = st.selectbox("Co widzisz na wyprasce?", list(defects_info.keys()))
    
    st.info(f"**Rozwiązania dla: {defect}**")
    for step in defects_info[defect]:
        st.write(f"- {step}")

# --- TAB 2: MATERIAŁY ---
with tab2:
    st.subheader("Parametry Przetwórstwa")
    df = pd.DataFrame(materials_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- TAB 3: KALKULATOR ---
with tab3:
    st.subheader("Siła Zwarcia (szacunkowa)")
    area = st.number_input("Powierzchnia rzutu (cm²)", min_value=1.0, value=100.0)
    pressure = st.number_input("Ciśnienie w gnieździe (bar)", min_value=1, value=300)
    
    force = (area * pressure) / 10
    st.metric("Sugerowana Siła Zwarcia", f"{force} kN")
    st.caption("Wzór: F = (A * p) / 10")