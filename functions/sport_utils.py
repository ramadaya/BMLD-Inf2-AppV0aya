import streamlit as st 
import pandas as pd 

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

