import streamlit as st 
import pandas as pd


def get_data_df():
    """Return shared app data from session state."""
    if "data_df" not in st.session_state:
        st.session_state["data_df"] = pd.DataFrame()
    return st.session_state["data_df"]

def save_data():
    st.session_state["data_manager"].save_user_data(
        st.session_state["data_df"],
        "data.csv"
    )


def get_calendar_df(data_df):
    """Return cleaned calendar entries."""
    if data_df.empty or "Typ" not in data_df.columns:
        return pd.DataFrame(
            columns=["Typ", "Datum", "Zykluslänge", "Periodendauer"]
        )

    calendar_df = data_df[data_df["Typ"] == "Kalender"].copy()

    calendar_df = calendar_df.dropna(
        subset=["Datum", "Zykluslänge", "Periodendauer"]
    )

    if not calendar_df.empty:
        calendar_df["Datum"] = pd.to_datetime(
            calendar_df["Datum"],
            errors="coerce"
        ).dt.date

    return calendar_df