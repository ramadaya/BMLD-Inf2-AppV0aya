import streamlit as st
import pandas as pd
from datetime import date, timedelta
from streamlit_calendar import calendar
from utils.data_manager import DataManager
from functions.data_utils import get_data_df, get_calendar_df
from functions.cycle_utils import calculate_cycle_phases
from functions.render import render_header

render_header("Zyklus-Kalender 🌸", logo_width=70)


PHASE_COLORS = {
    "menstruation": "#e63946",
    "follikel": "#f4a261",
    "eisprung": "#2a9d8f",
    "luteal": "#6a4c93",
}


def save_calendar_entry(period_start, cycle_length, period_length):
    """Save a new calendar entry."""
    new_row = pd.DataFrame([{
        "Typ": "Kalender",
        "Datum": period_start,
        "Zykluslänge": cycle_length,
        "Periodendauer": period_length,
    }])

    st.session_state["data_df"] = pd.concat(
        [st.session_state["data_df"], new_row],
        ignore_index=True,
    )

    data_manager = DataManager()
    data_manager.save_user_data(
        st.session_state["data_df"],
        "data.csv",
    )


def render_period_form():
    """Show form for cycle input."""
    with st.form("period_form"):
        st.subheader("Periode eingeben")

        period_start = st.date_input(
            "Erster Tag der Periode",
            value=date.today(),
        )

        cycle_length = st.slider(
            "Zykluslänge (Tage)",
            min_value=21,
            max_value=35,
            value=28,
        )

        period_length = st.slider(
            "Periodendauer (Tage)",
            min_value=2,
            max_value=8,
            value=5,
        )

        submitted = st.form_submit_button("Speichern & Berechnen")

        if submitted:
            save_calendar_entry(
                period_start,
                cycle_length,
                period_length,
            )

            st.success("✅ Gespeichert!")
            st.rerun()


def build_calendar_events(calendar_df):
    """Build events for the latest calendar entry."""
    if calendar_df.empty:
        return [], None

    last_row = calendar_df.iloc[-1]

    return calculate_cycle_phases(PHASE_COLORS,
        period_start=last_row["Datum"],
        cycle_length=int(last_row["Zykluslänge"]),
        period_length=int(last_row["Periodendauer"]),
    )


def render_calendar(events):
    """Display the interactive calendar."""
    calendar_options = {
        "initialView": "dayGridMonth",
        "locale": "de",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek",
        },
    }

    calendar(events=events, options=calendar_options)


def render_legend():
    """Show phase legend."""
    st.markdown(
        """
        ---
        **Legende:**  
        🔴 Menstruation &nbsp;|&nbsp;
        🌱 Follikelphase &nbsp;|&nbsp;
        🐣 Eisprung &nbsp;|&nbsp;
        🌙 Lutealphase
        """
    )


def render_saved_entries(calendar_df, next_period):
    """Show saved calendar entries and next predicted period."""
    if calendar_df.empty:
        st.warning("⚠️ Bitte trage deine Periode ein, um den Kalender anzuzeigen.")
        return

    st.subheader("📋 Gespeicherte Einträge")
    st.dataframe(calendar_df)

    if next_period is not None:
        st.info(
            f"📅 Nächste voraussichtliche Periode: "
            f"{next_period.strftime('%d.%m.%Y')}"
        )


data_df = get_data_df()
calendar_df = get_calendar_df(data_df)

render_period_form()

events, next_period = build_calendar_events(calendar_df)

render_calendar(events)
render_legend()
render_saved_entries(calendar_df, next_period)