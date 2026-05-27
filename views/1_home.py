import streamlit as st
import pandas as pd
from datetime import date
from functions.cycle_utils import get_current_phase, PHASE_INFO
from functions.render import get_data_df
col1, col2 = st.columns([1, 5])

with col1:
    st.image("docs/logo.png", width=80)

with col2:
    st.title("Berry Cycle 🍓")

SYMPTOM_COLS = [
    "⚡️ Energie",
    "😣 Schmerzen",
    "🧠 Fokus",
    "🍫 Heißhunger",
    "😴 Müdigkeit",
    "😊 Stimmung",
]

def render_navigation():
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


def render_phase_card(info):
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
        unsafe_allow_html=True,
    )


def render_next_period(data_df):
    st.markdown("### 📅 Nächste Periode")

    if data_df.empty or "Typ" not in data_df.columns:
        st.caption("Noch keine Kalender-Daten vorhanden.")
        return

    calendar_df = data_df[data_df["Typ"] == "Kalender"].copy()
    calendar_df = calendar_df.dropna(subset=["Datum", "Zykluslänge", "Periodendauer"])

    if calendar_df.empty:
        st.caption("Noch keine Kalender-Daten vorhanden.")
        return

    calendar_df["Datum"] = pd.to_datetime(calendar_df["Datum"], errors="coerce").dt.date
    last = calendar_df.iloc[-1]

    last_date = last["Datum"]
    cycle_length = int(last["Zykluslänge"])
    next_period = last_date + pd.Timedelta(days=cycle_length)
    days_left = (next_period - date.today()).days

    if days_left > 0:
        message = f"Noch <b>{days_left} Tage</b> bis zur nächsten Periode"
    elif days_left == 0:
        message = "🔴 Deine Periode könnte heute beginnen!"
    else:
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
        unsafe_allow_html=True,
    )


def get_bar_color(value):
    if value >= 7:
        return "#2a9d8f"
    if value >= 4:
        return "#f4a261"
    return "#e63946"


def show_no_symptoms_message():
    st.markdown(
        """
        <div style="background-color:#f9f9f9;
                    border-radius: 12px;
                    padding: 1.2rem 1.5rem;
                    border: 1px solid #eee;
                    color:#888;">
            Noch keine Symptome für heute eingetragen.
            Gehe zu <b>🩺 Symptome</b> um sie einzutragen!
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_today_symptoms(data_df):
    st.markdown("### 📊 Heutige Symptome")

    if data_df.empty or "Typ" not in data_df.columns:
        show_no_symptoms_message()
        return

    symptoms_df = data_df[data_df["Typ"] == "Symptom"].copy()

    if symptoms_df.empty or "Datum" not in symptoms_df.columns:
        show_no_symptoms_message()
        return

    symptoms_df["Datum"] = pd.to_datetime(symptoms_df["Datum"], errors="coerce").dt.date
    today_date = date.today()
    today_entries = symptoms_df[symptoms_df["Datum"] == today_date]

    if today_entries.empty:
        show_no_symptoms_message()
        return

    today_row = today_entries.iloc[-1]
    cols = st.columns(3)

    for i, symptom in enumerate(SYMPTOM_COLS):
        if symptom not in today_row or pd.isna(today_row[symptom]):
            continue

        value = int(today_row[symptom])
        bar_color = get_bar_color(value)

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
                                    width:{value * 10}%;
                                    height:8px;
                                    border-radius:10px;">
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_footer():
    st.markdown("---")

    st.markdown("## ✨ Unser Team")

    st.markdown(
        """
        Diese App wurde mit viel Herzblut entwickelt von:
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            👩‍💻 **Aya Ramadan**  
            Entwicklung & Design  
            📧 ramadaya@students.zhaw.ch
            """
        )

    with col2:
        st.markdown(
            """
            👩‍💻 **Carolina Tresch**  
            Entwicklung & Daten  
            📧 tresccar@students.zhaw.ch
            """
        )

    with col3:
        st.markdown(
            """
            👩‍💻 **Sofia Lercara**  
            Entwicklung & Inhalte  
            📧 lercasof@students.zhaw.ch
            """
        )

    st.markdown("---")

    st.caption(
        "Diese App ist das leere Gerüst für die "
        "App-Entwicklung im Modul Informatik 2 (BMLD/ZHAW)"
    )

    st.caption("Autor: Samuel Wehrli (wehs@zhaw.ch)")


data_df = get_data_df()
render_navigation()

phase = get_current_phase()

if phase is None:
    st.info("Trage deinen Zyklus im Kalender ein, um loszulegen.")
else:
    info = PHASE_INFO[phase]
    render_phase_card(info)
    render_next_period(data_df)
    render_today_symptoms(data_df)

render_footer()