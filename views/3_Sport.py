import sys
import os
from turtle import pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from cycle_utils import get_current_phase, PHASE_INFO

st.title("👟 Sport")

NOTES_FILE = "notes.csv"

# --- Load saved notes ---
if os.path.exists(NOTES_FILE):
    notes_df = pd.read_csv(NOTES_FILE)
else:
    notes_df = pd.DataFrame(columns=["Datum", "Phase", "Notiz"])

phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum Kalender!")
else:
    info = PHASE_INFO[phase]
    st.markdown(f"## Empfehlungen für die {info['name']}")

    items = "".join(f"<li> {activity}</li>" for activity in info["sports"])

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

# --- Notes section ---
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
            "Datum": str(note_date),
            "Phase": info["name"],
            "Notiz": note_text
        }])
        notes_df = pd.concat([notes_df, new_note], ignore_index=True)
        notes_df.to_csv(NOTES_FILE, index=False)
        st.success("✅ Notiz gespeichert!")

    # --- Show past notes for current phase ---
    phase_notes = notes_df[notes_df["Phase"] == info["name"]]

    if not phase_notes.empty:
        st.markdown(f"#### Frühere Notizen in der {info['name']}:")
        for _, row in phase_notes.iloc[::-1].iterrows():  # newest first
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