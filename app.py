import streamlit as st
import pandas as pd
# Ostateczna poprawka wyświetlania dla iPhone
st.markdown(
    """
    <style>
    /* 1. Rozszerzenie głównego kontenera */
    .main .block-container {
        max-width: 100%;
        padding-top: 1rem;
        /* Dodajemy ogromny margines na dole - 80% wysokości ekranu */
        padding-bottom: 80vh !important; 
    }
    
    /* 2. Fix dla przewijania na iOS */
    html, body, [data-testid="stAppViewContainer"] {
        height: auto !important;
        min-height: 180vh !important; /* Strona będzie prawie dwa razy dłuższa niż ekran */
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch; /* Płynne przewijanie palcem */
    }

    /* 3. Ukrycie zbędnych elementów blokujących miejsce */
    [data-testid="stHeader"], footer {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Konfiguracja strony (żeby dobrze wyglądała na telefonie)
st.set_page_config(page_title="Setter Pro", page_icon="⚙️")

st.title("⚙️ Asystent Ustawiacza")

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
tab1, tab2, tab3, tab4 = st.tabs(["Diagnostyka", "Materiały", "Kalkulatory", "Optymalizacja"])
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
    calc_type = st.selectbox("Wybierz kalkulator:", 
                             ["Siła Zwarcia", "Wydajność Produkcji", "Zapotrzebowanie Materiału"])
    
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
            hours = st.selectbox("Czas pracy (godziny)", [1, 7.5, 8, 12, 24, 168], index=2)
            efficiency = st.slider("Wydajność maszyny (%)", 50, 100, 95)

        total_shots = (3600 / cycle_time) * hours
        total_parts = total_shots * cavities * (efficiency / 100)
        st.metric("Planowana liczba detali (Szt.)", f"{int(total_parts)}")

    elif calc_type == "Zapotrzebowanie Materiału":
        st.info("Oblicz ilość materiału potrzebną do realizacji zlecenia.")
        
        col1, col2 = st.columns(2)
        with col1:
            part_weight = st.number_input("Waga 1 detalu (gramy)", min_value=0.01, value=10.0, step=0.1)
            runner_weight = st.number_input("Waga wlewka (gramy)", min_value=0.0, value=2.0, step=0.1)
            cavities_mat = st.number_input("Liczba gniazd ", min_value=1, value=1, step=1)
        
        with col2:
            order_qty = st.number_input("Ilość do wyprodukowania (Szt.)", min_value=1, value=1000, step=100)
            scrap_rate = st.slider("Zakładany odpad (%)", 0, 20, 2)

        # Obliczenia:
        # Waga jednego wtrysku (detale + wlewek)
        shot_weight = (part_weight * cavities_mat) + runner_weight
        # Całkowita waga netto dla zlecenia w gramach
        total_weight_g = (order_qty / cavities_mat) * shot_weight
        # Uwzględnienie odpadu i zamiana na kg
        total_weight_kg = (total_weight_g / 1000) * (1 + scrap_rate / 100)
        
        st.divider()
        st.metric("Potrzebny materiał (kg)", f"{round(total_weight_kg, 2)} kg")
        
        st.write("📊 **Rozbicie wagowe:**")
        st.write(f"- Waga wtrysku: {round(shot_weight, 2)} g")
        st.write(f"- Waga netto zlecenia (bez odpadu): {round(total_weight_g / 1000, 2)} kg")
        st.write(f"- Dodatek na odpad: {round((total_weight_g / 1000) * (scrap_rate / 100), 2)} kg")
# --- TAB 4: OPTYMALIZACJA ---
with tab4:
    st.subheader("🚀 Strategie Optymalizacji Procesu")
    
    opt_choice = st.selectbox("Wybierz obszar optymalizacji:", 
                              ["Skracanie Czasu Cyklu", "Stabilizacja Wagi Wtrysku", "Oszczędność Energii"])
    
    if opt_choice == "Skracanie Czasu Cyklu":
        st.success("Cel: Zwiększenie wydajności bez utraty jakości.")
        
        st.markdown("### ⚖️ Optymalizacja czasu docisku (Gate Freeze Study)")
        st.write("Wpisuj wagę detalu wraz z wlewkiem dla coraz dłuższego czasu docisku:")
        
        # Tworzenie tabeli do wpisywania danych
        data_weight = pd.DataFrame({
            "Czas docisku [s]": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "Waga wtrysku [g]": [0.0] * 6
        })
        
        # Interaktywna tabela
        edited_df = st.data_editor(data_weight, num_rows="dynamic", key="gate_freeze_editor")
        
        # Prosta analiza
        max_w = edited_df["Waga wtrysku [g]"].max()
        if max_w > 0:
            # Szukamy pierwszego czasu, przy którym waga przestała rosnąć
            stable_time = edited_df[edited_df["Waga wtrysku [g]"] == max_w]["Czas docisku [s]"].min()
            st.info(f"💡 **Wniosek:** Przewężka zastygła prawdopodobnie przy **{stable_time} s**. Ustaw czas docisku na **{stable_time + 0.5} s** (margines bezpieczeństwa).")

        st.divider()
        st.info("""
        **Pozostałe rady:**
        * **Czas chłodzenia:** Obniżaj o 0.5s, aż detale zaczną się deformować.
        * **Ruchy równoległe:** Jeśli maszyna pozwala, otwieraj formę podczas dozowania.
        * **Prędkość otwierania:** Zwiększ prędkość w środkowej fazie ruchu.
        """)

    elif opt_choice == "Stabilizacja Wagi Wtrysku":
        st.warning("Cel: Wyeliminowanie wahań wymiarowych.")
        st.write("""
        * **Poduszka (Cushion):** Musi być stabilna (np. 3-5 mm).
        * **Dekompresja:** Ustaw minimalną możliwą.
        * **Punkt przełączenia:** Ustaw tak, aby wypełnić 95-98% objętości detalu.
        """)

    elif opt_choice == "Oszczędność Energii":
        st.info("Cel: Obniżenie kosztów.")
        st.write("""
        * **Izolacja cylindra:** Zastosuj koce termoizolacyjne.
        * **Siła zwarcia:** Nie używaj maksymalnej, jeśli nie jest potrzebna.
        """)


