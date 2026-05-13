import streamlit as st
from datetime import date, timedelta
from streamlit_calendar import calendar
import pandas as pd
import os
from utils.data_manager import DataManager

st.title("Zyklus-Kalender 🌸")


# --- Cycle phase calculation ---
def calculate_cycle_phases(period_start: date, cycle_length: int = 28, period_length: int = 5):
    """
    Returns a list of calendar events for all 4 cycle phases.
    Default: 28-day cycle, 5-day period.
    """
    events = []

    # Phase 1: Menstruation
    for i in range(period_length):
        events.append({
            "title": "🔴 Menstruation",
            "start": str(period_start + timedelta(days=i)),
            "color": "#e63946"
        })

    # Phase 2: Follicular phase (after period until ovulation)
    follicular_start = period_start + timedelta(days=period_length)
    follicular_end = period_start + timedelta(days=13)  # ~Day 6–12
    for i in range((follicular_end - follicular_start).days + 1):
        events.append({
            "title": "🌱 Follikelphase",
            "start": str(follicular_start + timedelta(days=i)),
            "color": "#f4a261"
        })

    # Phase 3: Ovulation (~Day 13–15)
    ovulation_day = period_start + timedelta(days=cycle_length - 14)  # LH surge offset
    for i in range(3):
        events.append({
            "title": "🐣 Eisprung",
            "start": str(ovulation_day + timedelta(days=i)),
            "color": "#2a9d8f"
        })

    # Phase 4: Luteal phase (after ovulation until next period)
    luteal_start = ovulation_day + timedelta(days=3)
    next_period = period_start + timedelta(days=cycle_length)
    luteal_days = (next_period - luteal_start).days
    for i in range(luteal_days):
        events.append({
            "title": "🌙 Lutealphase",
            "start": str(luteal_start + timedelta(days=i)),
            "color": "#6a4c93"
        })

    return events, next_period

# --- Load saved data ---
####Ka Men######
df = st.session_state.data_df

if len(df) !=0 :
    df["Datum"] = pd.to_datetime(df["Datum"]).dt.date
else:
    df = pd.DataFrame(columns=["Datum", "Zykluslänge", "Periodendauer"])
################################

# --- Input form ---
with st.form("period_form"):
    st.subheader("Periode eingeben")
    period_start = st.date_input("Erster Tag der Periode", value=date.today())
    cycle_length = st.slider("Zykluslänge (Tage)", min_value=21, max_value=35, value=28)
    period_length = st.slider("Periodendauer (Tage)", min_value=2, max_value=8, value=5)

    submitted = st.form_submit_button("Speichern & Berechnen")

    ## Ka Men##
    data_manager = DataManager()
    ##########
    if submitted:
        new_row = pd.DataFrame([{
            "Datum": period_start,
            "Zykluslänge": cycle_length,
            "Periodendauer": period_length
        }])

    #####Ka Men######
        st.session_state['data_df'] = pd.concat([st.session_state['data_df'], new_row])
        #df = pd.concat([df, new_row], ignore_index=True)
        data_manager.save_user_data(st.session_state["data_df"],"data.csv" )
        #df.to_csv(FILE, index=False)
    ###########
        st.success("✅ Gespeichert!")
        st.rerun()
all_events = []

# --- Build calendar events ---
if df.empty:
    st.warning("⚠️ Bitte trage deine Periode ein, um den Kalender anzuzeigen.")

else:

    # Only use the last entry for the calendar
    last_row = df.iloc[-1]
    phase_events, _ = calculate_cycle_phases(
        period_start=last_row["Datum"],
        cycle_length=int(last_row["Zykluslänge"]),
        period_length=int(last_row["Periodendauer"])
    )
    all_events = phase_events


# --- Display calendar ---
calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "de",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek"
    }
}

calendar(events=all_events, options=calendar_options)


# --- Legend ---
st.markdown("""
---
**Legende:**
🔴 Menstruation &nbsp;|&nbsp; 🌱 Follikelphase &nbsp;|&nbsp; ✨ Eisprung &nbsp;|&nbsp; 🌙 Lutealphase
""")


# --- Show saved entries ---
if not df.empty:
    st.subheader("📋 Gespeicherte Einträge")
    st.dataframe(df)

    # Show next predicted period
    last_row = df.iloc[-1]
    _, next_period = calculate_cycle_phases(
        period_start=last_row["Datum"],
        cycle_length=int(last_row["Zykluslänge"]),
        period_length=int(last_row["Periodendauer"])
    )
    st.info(f"📅 Nächste voraussichtliche Periode: **{next_period.strftime('%d.%m.%Y')}**")