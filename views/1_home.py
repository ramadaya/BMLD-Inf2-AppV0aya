import streamlit as st

from functions.cycle_utils import get_current_phase, PHASE_INFO
from functions.data_utils import get_data_df
from functions.render import render_header, render_navigation, render_phase_card, render_next_period, render_today_symptoms, render_footer

render_header("Berry Cycle 🍓", logo_width=80)



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
