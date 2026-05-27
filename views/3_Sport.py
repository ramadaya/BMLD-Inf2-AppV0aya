import streamlit as st
import pandas as pd
from functions.cycle_utils import get_current_phase, PHASE_INFO
from functions.render import get_data_df

def render_header():
    """Show page logo and title."""
    col1, col2 = st.columns([1, 5])

    with col1:
        st.image("docs/logo.png", width=70)

    with col2:
        st.title("👟 Sport")


def render_sport_recommendations(info):
    """Show sport recommendations for the current phase."""
    st.markdown(f"## Empfehlungen für die {info['name']}")

    items = "".join(
        f"<li>{activity}</li>"
        for activity in info["sports"]
    )

    st.markdown(
        f"""
        <div style="background-color:{info['color']}22;
                    border-left: 5px solid {info['color']};
                    padding: 1rem;
                    border-radius: 8px;">
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def save_sport_note(note_text, note_date, phase_name):
    """Save sport note in shared user data."""
    new_note = pd.DataFrame([{
        "Typ": "Sport-Notiz",
        "Datum": str(note_date),
        "Phase": phase_name,
        "Notiz": note_text,
    }])

    st.session_state["data_df"] = pd.concat(
        [st.session_state["data_df"], new_note],
        ignore_index=True,
    )

    st.session_state["data_manager"].save_user_data(
        st.session_state["data_df"],
        "data.csv",
    )


def render_note_form(info):
    """Show form for adding sport notes."""
    st.markdown("---")
    st.subheader("📝 Meine Notizen")

    with st.form("sport_notes_form"):
        note_text = st.text_area(
            "Wie fühlst du dich heute?",
            placeholder="z.B. viel Energie, Kopfschmerzen, gute Stimmung...",
        )

        note_date = st.date_input(
            "Datum",
            value=pd.Timestamp.today(),
        )

        save_note = st.form_submit_button("Notiz speichern")

        if save_note:
            if note_text.strip():
                save_sport_note(
                    note_text=note_text,
                    note_date=note_date,
                    phase_name=info["name"],
                )
                st.success("✅ Notiz gespeichert!")
                st.rerun()
            else:
                st.warning("Bitte schreibe zuerst eine Notiz.")


def get_phase_notes(data_df, phase_name):
    """Return saved sport notes for the current phase."""
    if data_df.empty:
        return pd.DataFrame()

    required_cols = {"Typ", "Phase"}
    if not required_cols.issubset(data_df.columns):
        return pd.DataFrame()

    return data_df[
        (data_df["Typ"] == "Sport-Notiz")
        & (data_df["Phase"] == phase_name)
    ].copy()


def render_phase_notes(phase_notes, info):
    """Show previous notes for the current phase."""
    if phase_notes.empty:
        st.caption("Noch keine Notizen für diese Phase gespeichert.")
        return

    st.markdown(f"#### Frühere Notizen in der {info['name']}:")

    for _, row in phase_notes.iloc[::-1].iterrows():
        st.markdown(
            f"""
            <div style="background-color:{info['color']}11;
                        border-left: 3px solid {info['color']};
                        padding: 0.6rem 1rem;
                        border-radius: 6px;
                        margin-bottom: 0.5rem;">
                <small>📅 {row['Datum']}</small><br>
                {row['Notiz']}
            </div>
            """,
            unsafe_allow_html=True,
        )


render_header()

data_df = get_data_df()
phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum Kalender!")
else:
    info = PHASE_INFO[phase]

    render_sport_recommendations(info)
    render_note_form(info)

    updated_data_df = get_data_df()
    phase_notes = get_phase_notes(
        updated_data_df,
        info["name"],
    )

    render_phase_notes(phase_notes, info)