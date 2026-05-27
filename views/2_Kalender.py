import streamlit as st
import pandas as pd
from datetime import date, timedelta
from streamlit_calendar import calendar
from utils.data_manager import DataManager
from functions.render import get_data_df
col1, col2 = st.columns([1, 5])

with col1:
    st.image("docs/logo.png", width=70)

with col2:
    st.title("Zyklus-Kalender 🌸")


PHASE_COLORS = {
    "menstruation": "#e63946",
    "follikel": "#f4a261",
    "eisprung": "#2a9d8f",
    "luteal": "#6a4c93",
}


def calculate_cycle_phases(
    period_start: date,
    cycle_length: int = 28,
    period_length: int = 5,
):
    """Calculate calendar events for the four cycle phases."""
    events = []

    for i in range(period_length):
        events.append({
            "title": "🔴 Menstruation",
            "start": str(period_start + timedelta(days=i)),
            "color": PHASE_COLORS["menstruation"],
        })

    ovulation_day = period_start + timedelta(days=cycle_length - 14)

    follicular_start = period_start + timedelta(days=period_length)
    follicular_end = ovulation_day - timedelta(days=1)

    for i in range((follicular_end - follicular_start).days + 1):
        events.append({
            "title": "🌱 Follikelphase",
            "start": str(follicular_start + timedelta(days=i)),
            "color": PHASE_COLORS["follikel"],
        })

    for i in range(3):
        events.append({
            "title": "🐣 Eisprung",
            "start": str(ovulation_day + timedelta(days=i)),
            "color": PHASE_COLORS["eisprung"],
        })

    luteal_start = ovulation_day + timedelta(days=3)
    next_period = period_start + timedelta(days=cycle_length)
    luteal_days = (next_period - luteal_start).days

    for i in range(luteal_days):
        events.append({
            "title": "🌙 Lutealphase",
            "start": str(luteal_start + timedelta(days=i)),
            "color": PHASE_COLORS["luteal"],
        })

    return events, next_period


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

    return calculate_cycle_phases(
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