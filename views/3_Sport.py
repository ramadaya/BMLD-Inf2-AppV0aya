import streamlit as st
import pandas as pd
from functions.cycle_utils import get_current_phase, PHASE_INFO

st.title("👟 Sport")

# Gemeinsame Daten laden
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame()

data_df = st.session_state["data_df"]

# Sport-Notizen aus gemeinsamer Datei filtern
if not data_df.empty and "Typ" in data_df.columns:
    notes_df = data_df[data_df["Typ"] == "Sport-Notiz"]
else:
    notes_df = pd.DataFrame(columns=["Typ", "Datum", "Phase", "Notiz"])

phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum Kalender!")
else:
    info = PHASE_INFO[phase]
    st.markdown(f"## Empfehlungen für die {info['name']}")

    items = "".join(f"<li>{activity}</li>" for activity in info["sports"])

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

    # Notizen
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
                "Typ": "Sport-Notiz",
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

    # Frühere Notizen anzeigen
    data_df = st.session_state["data_df"]

if not data_df.empty and "Typ" in data_df.columns and "Phase" in data_df.columns:
    phase_notes = data_df[
        (data_df["Typ"] == "Sport-Notiz") &
        (data_df["Phase"] == info["name"])
    ]
else:
    phase_notes = pd.DataFrame()

    if not phase_notes.empty:
        st.markdown(f"#### Frühere Notizen in der {info['name']}:")
        for _, row in phase_notes.iloc[::-1].iterrows():
            st.markdown(
                f"""
                <div style="background-color:{info['color']}11; 
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