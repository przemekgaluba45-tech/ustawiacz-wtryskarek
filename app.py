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
    "Deformacje": ["Wydłuż chłodzenie", "Zrównoważ temp. połówek formy", "Zmniejsz docisk"],
    "Rozwarstwienia": ["Sprawdź czystość/zawilgocenie", "Podnieś temp. stopu", "Zmniejsz prędkość wtrysku"],
    "Jetting (Zmatowienia)": ["Zmniejsz prędkość wtrysku na starcie", "Podnieś temp. stopu", "Zwiększ temp. formy"],
    "Pęcherze powietrza": ["Zwiększ ciśnienie i czas docisku", "Obniż temp. stopu", "Zmniejsz dekompresję"],
    "Smugi barwnika": ["Zwiększ ciśnienie spiętrzenia", "Zwiększ obroty ślimaka", "Podnieś temp. w strefie dozowania"],
    "Zimne wlewy": ["Podnieś temp. dyszy", "Zwiększ odskok (dekompresję)", "Sprawdź grzałkę dyszy"],
    "Łuszczenie powierzchni": ["Zwiększ temp. stopu", "Wysusz materiał", "Zmniejsz ilość regranulatu"],
    "Efekt gramofonowy": ["Zwiększ prędkość wtrysku", "Zwiększ temp. stopu", "Podnieś temp. formy"]
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
    st.subheader("🧮 Obliczenia Techniczne")
    
    # Wybór rodzaju kalkulatora
    calc_type = st.radio("Wybierz kalkulator:", ["Siła Zwarcia", "Wydajność Produkcji"])
    
    if calc_type == "Siła Zwarcia":
        area = st.number_input("Powierzchnia rzutu detali (cm²)", min_value=1.0, value=100.0)
        pressure = st.number_input("Ciśnienie w gnieździe (bar)", min_value=1, value=300)
        force = (area * pressure) / 10
        st.metric("Sugerowana Siła Zwarcia", f"{force} kN")
        st.caption("Wzór: F = (A * p) / 10")
        
    elif calc_type == "Wydajność Produkcji":
        st.info("Oblicz, ile detali wyprodukujesz w określonym czasie.")
        
        col1, col2 = st.columns(2)
        with col1:
            cycle_time = st.number_input("Czas cyklu (sekundy)", min_value=0.1, value=20.0, step=0.1)
            cavities = st.number_input("Liczba gniazd w formie", min_value=1, value=1, step=1)
        
        with col2:
            hours = st.selectbox("Czas pracy (godziny)", [1, 7.5, 8, 12, 24], index=2)
            efficiency = st.slider("Wydajność maszyny (%)", 50, 100, 95)

        # Obliczenia: (3600s / czas cyklu) * liczba gniazd * godziny * wydajność
        total_shots = (3600 / cycle_time) * hours
        total_parts = total_shots * cavities * (efficiency / 100)
        
        st.divider()
        st.metric("Planowana liczba detali (Szt.)", f"{int(total_parts)}")
        
        st.write(f"📊 **Szczegóły:**")
        st.write(f"- Liczba wtrysków: {int(total_shots)}")
        st.write(f"- Detale na godzinę (100%): {int((3600 / cycle_time) * cavities)}")
