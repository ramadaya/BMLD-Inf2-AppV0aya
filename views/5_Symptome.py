import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from functions.cycle_utils import get_current_phase, PHASE_INFO

st.title("🩺 Symptome")

SYMPTOM_COLS = ["⚡️ Energie", "😣 Schmerzen", "🧠 Fokus", "🍫 Heißhunger", "😴 Müdigkeit", "😊 Stimmung"]

if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame()

data_df = st.session_state["data_df"]

if not data_df.empty and "Typ" in data_df.columns:
    symptoms_df = data_df[data_df["Typ"] == "Symptom"].copy()
else:
    symptoms_df = pd.DataFrame(columns=["Typ", "Datum", "Phase"] + SYMPTOM_COLS)

phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum 📅 Kalender!")
else:
    info = PHASE_INFO[phase]

    st.markdown(f"## Typische Symptome in der {info['name']}")

    items = "".join(f"<li>{symptom}</li>" for symptom in info["symptoms"])
    st.markdown(
        f"""
        <div style="background-color:{info['color']}22; 
                    border-left: 5px solid {info['color']}; 
                    padding: 1rem; 
                    border-radius: 8px;">
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.subheader("📊 Tägliches Symptom-Tracking")

    selected_date = st.date_input(
    "Datum",
    value=pd.Timestamp.today()
)

    today = str(selected_date)

    already_logged = (
        not symptoms_df.empty
        and "Datum" in symptoms_df.columns
        and today in symptoms_df["Datum"].astype(str).values
    )

    if already_logged:
        st.success("✅ Du hast heute bereits deine Symptome eingetragen!")

        if st.button("✏️ Heutigen Eintrag bearbeiten"):
            st.session_state["data_df"] = st.session_state["data_df"][
                ~(
                    (st.session_state["data_df"]["Typ"] == "Symptom") &
                    (st.session_state["data_df"]["Datum"].astype(str) == today)
                )
            ]

            st.session_state["data_manager"].save_user_data(
                st.session_state["data_df"],
                "data.csv"
            )

            st.rerun()

    else:
        with st.form("symptoms_form"):
            st.markdown("Wie fühlst du dich heute? (1 = niedrig, 10 = hoch)")

            col1, col2 = st.columns(2)

            with col1:
                energie = st.slider("⚡️ Energie", 1, 10, 5)
                fokus = st.slider("🧠 Fokus", 1, 10, 5)
                muedigkeit = st.slider("😴 Müdigkeit", 1, 10, 5)

            with col2:
                schmerzen = st.slider("😣 Schmerzen", 1, 10, 1)
                heisshunger = st.slider("🍫 Heißhunger", 1, 10, 5)
                stimmung = st.slider("😊 Stimmung", 1, 10, 5)

            save_symptoms = st.form_submit_button("💾 Speichern")

            if save_symptoms:
                new_entry = pd.DataFrame([{
                    "Typ": "Symptom",
                    "Datum": today,
                    "Phase": info["name"],
                    "⚡️ Energie": energie,
                    "😣 Schmerzen": schmerzen,
                    "🧠 Fokus": fokus,
                    "🍫 Heißhunger": heisshunger,
                    "😴 Müdigkeit": muedigkeit,
                    "😊 Stimmung": stimmung
                }])

                st.session_state["data_df"] = pd.concat(
                    [st.session_state["data_df"], new_entry],
                    ignore_index=True
                )

                st.session_state["data_manager"].save_user_data(
                    st.session_state["data_df"],
                    "data.csv"
                )

                st.success("✅ Gespeichert!")
                st.rerun()

    st.markdown("---")
    st.subheader("📈 Statistiken über Zeit")

    data_df = st.session_state["data_df"]

    if not data_df.empty and "Typ" in data_df.columns:
        symptoms_df = data_df[data_df["Typ"] == "Symptom"].copy()
    else:
        symptoms_df = pd.DataFrame(columns=["Typ", "Datum", "Phase"] + SYMPTOM_COLS)

    if symptoms_df.empty:
        st.caption("Noch keine Daten vorhanden. Trage täglich deine Symptome ein! 🌸")
    else:
        symptoms_df["Datum"] = pd.to_datetime(symptoms_df["Datum"])

        tab1, tab2, tab3 = st.tabs(["📅 Verlauf", "🌀 Phasen-Vergleich", "📋 Durchschnitt"])

        with tab1:
            selected = st.multiselect(
                "Symptome auswählen:",
                SYMPTOM_COLS,
                default=["⚡️ Energie", "😊 Stimmung"]
            )

            if selected:
                fig = px.line(
                    symptoms_df.sort_values("Datum"),
                    x="Datum",
                    y=selected,
                    title="Symptomverlauf über Zeit",
                    markers=True,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )

                fig.update_layout(
                    yaxis=dict(range=[0, 10]),
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend_title="Symptom"
                )

                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            if "Phase" in symptoms_df.columns:
                phase_avg = symptoms_df.groupby("Phase")[SYMPTOM_COLS].mean().round(1).reset_index()

                fig2 = px.bar(
                    phase_avg.melt(id_vars="Phase", var_name="Symptom", value_name="Durchschnitt"),
                    x="Symptom",
                    y="Durchschnitt",
                    color="Phase",
                    barmode="group",
                    title="Durchschnitt pro Phase",
                    color_discrete_sequence=["#e63946", "#f4a261", "#2a9d8f", "#6a4c93"]
                )

                fig2.update_layout(
                    yaxis=dict(range=[0, 10]),
                    plot_bgcolor="rgba(0,0,0,0)"
                )

                st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            avg = symptoms_df[SYMPTOM_COLS].mean().round(1).reset_index()
            avg.columns = ["Symptom", "Durchschnitt"]

            fig3 = px.bar(
                avg,
                x="Symptom",
                y="Durchschnitt",
                title="Gesamtdurchschnitt aller Symptome",
                color="Symptom",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            fig3.update_layout(
                yaxis=dict(range=[0, 10]),
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )

            st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.subheader("📝 Meine Notizen")

    with st.form("notes_form"):
        note_text = st.text_area(
            "Wie fühlst du dich heute?",
            placeholder="z.B. viel Energie, Kopfschmerzen, gute Stimmung..."
        )

        note_date = st.date_input("Datum", value=pd.Timestamp.today())
        save_note = st.form_submit_button("Notiz speichern")

        if save_note and note_text.strip():
            new_note = pd.DataFrame([{
                "Typ": "Symptom-Notiz",
                "Datum": str(note_date),
                "Phase": info["name"],
                "Notiz": note_text
            }])

            st.session_state["data_df"] = pd.concat(
                [st.session_state["data_df"], new_note],
                ignore_index=True
            )

            st.session_state["data_manager"].save_user_data(
                st.session_state["data_df"],
                "data.csv"
            )

            st.success("✅ Notiz gespeichert!")
            st.rerun()

    data_df = st.session_state["data_df"]

    if not data_df.empty and "Typ" in data_df.columns:
        phase_notes = data_df[
            (data_df["Typ"] == "Symptom-Notiz") &
            (data_df["Phase"] == info["name"])
        ]
    else:
        phase_notes = pd.DataFrame()

    if not phase_notes.empty:
        st.markdown(f"#### Frühere Notizen in der {info['name']}:")
        for _, row in phase_notes.iloc[::-1].iterrows():
            st.markdown(
                f"""<div style="background-color:{info['color']}11; 
                            border-left: 3px solid {info['color']}; 
                            padding: 0.6rem 1rem; 
                            border-radius: 6px;
                            margin-bottom: 0.5rem;">
                    <small>📅 {row['Datum']}</small><br>{row['Notiz']}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.caption("Noch keine Notizen für diese Phase gespeichert.")