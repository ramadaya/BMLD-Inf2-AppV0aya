import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from datetime import date
from functions.cycle_utils import get_current_phase, PHASE_INFO

st.title("Berry Cycle 🍓")



# Navigation Buttons
st.markdown("### 🔗 Schnellzugriff")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("views/2_Kalender.py", label="📅 Kalender")
    st.page_link("views/3_Sport.py", label="👟 Sport")

with col2:
    st.page_link("views/4_Ernährung.py", label="🍓 Ernährung")
    st.page_link("views/5_Symptome.py", label="🩺 Symptome")

with col3:
    st.page_link("views/6_Boyfriend.py", label="❤️ Boyfriend")

SYMPTOMS_FILE = "symptoms.csv"
EVENTS_FILE = "events.csv"

# Begrüssung
if "user" in st.session_state:
    st.write(f"Hallo {st.session_state['user']} 👋")

phase = get_current_phase()

if phase is None:
    st.info("Trage deinen Zyklus im Kalender ein, um loszulegen.")
else:
    info = PHASE_INFO[phase]

    # --- Current phase card ---
    st.markdown("### 🌀 Deine aktuelle Phase")
    st.markdown(
        f"""
        <div style="background-color:{info['color']}22;
                    border-left: 6px solid {info['color']};
                    border-radius: 12px;
                    padding: 1.2rem 1.5rem;
                    margin-bottom: 1rem;">
            <h2 style="margin:0; color:{info['color']};">{info['name']}</h2>
            <p style="margin-top:0.5rem; font-size:1rem;">💬 {info['mood']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Countdown to next period ---
    st.markdown("### 📅 Nächste Periode")
    if os.path.exists(EVENTS_FILE):
        events_df = pd.read_csv(EVENTS_FILE)
        if not events_df.empty:
            last = events_df.iloc[-1]
            last_date = pd.to_datetime(last["Datum"]).date()
            cycle_length = int(last["Zykluslänge"])
            next_period = last_date + pd.Timedelta(days=cycle_length)
            days_left = (next_period - date.today()).days

            if days_left > 0:
                countdown_color = "#e63946"
                message = f"Noch <b>{days_left} Tage</b> bis zur nächsten Periode"
            elif days_left == 0:
                countdown_color = "#e63946"
                message = "🔴 Deine Periode könnte heute beginnen!"
            else:
                countdown_color = "#e63946"
                message = f"Periode war vor <b>{abs(days_left)} Tagen</b> erwartet"

            st.markdown(
                f"""
                <div style="background-color:#e6394611;
                            border-left: 6px solid #e63946;
                            border-radius: 12px;
                            padding: 1.2rem 1.5rem;
                            margin-bottom: 1rem;">
                    <p style="font-size:1.1rem; margin:0;">🩸 {message}</p>
                    <p style="margin:0.3rem 0 0 0; color:#888; font-size:0.9rem;">
                        Voraussichtlich am {next_period.strftime('%d.%m.%Y')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --- Today's symptom summary ---
    st.markdown("### 📊 Heutige Symptome")
    if os.path.exists(SYMPTOMS_FILE):
        symptoms_df = pd.read_csv(SYMPTOMS_FILE)
        today = str(date.today())

        if not symptoms_df.empty and today in symptoms_df["Datum"].values:
            today_row = symptoms_df[symptoms_df["Datum"] == today].iloc[-1]
            symptom_cols = ["⚡ Energie", "😣 Schmerzen", "🧠 Fokus", "🍫 Heißhunger", "😴 Müdigkeit", "😊 Stimmung"]

            cols = st.columns(3)
            for i, symptom in enumerate(symptom_cols):
                value = int(today_row[symptom])
                # Colour based on value
                if value >= 7:
                    bar_color = "#2a9d8f"
                elif value >= 4:
                    bar_color = "#f4a261"
                else:
                    bar_color = "#e63946"

                with cols[i % 3]:
                    st.markdown(
                        f"""
                        <div style="background-color:#f9f9f9;
                                    border-radius: 10px;
                                    padding: 0.8rem;
                                    margin-bottom: 0.8rem;
                                    text-align: center;
                                    border: 1px solid #eee;">
                            <p style="margin:0; font-size:1rem;">{symptom}</p>
                            <h3 style="margin:0.2rem 0; color:{bar_color};">{value}/10</h3>
                            <div style="background:#eee; border-radius:10px; height:8px;">
                                <div style="background:{bar_color}; 
                                            width:{value*10}%; 
                                            height:8px; 
                                            border-radius:10px;">
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                f"""
                <div style="background-color:#f9f9f9;
                            border-radius: 12px;
                            padding: 1.2rem 1.5rem;
                            border: 1px solid #eee;
                            color:#888;">
                    Noch keine Symptome für heute eingetragen. 
                    Gehe zu <b>🩺 Symptome</b> um sie einzutragen!
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.caption("Noch keine Symptom-Daten vorhanden.")





# !! WICHTIG: Eure Emails müssen in der App erscheinen!!

"""
Diese App wurde von folgenden Personen entwickelt:
- Aya Ramadan (ramadaya@students.zhaw.ch)
- Carolina Tresch (tresccar@students.zhaw.ch)
- Sofia Lercara (lercasof@students.zhaw.ch)

Diese App ist das leere Gerüst für die App-Entwicklung im Modul Informatik 2 (BMLD/ZHAW)

Autor: Samuel Wehrli (wehs@zhaw.ch)
"""
