import streamlit as st
import pandas as pd
from functions.cycle_utils import get_current_phase, PHASE_INFO
from functions.data_utils import get_data_df
from functions.render import render_header, render_sport_recommendations, render_note_form, render_phase_notes
from functions.sport_utils import get_phase_notes

render_header("👟 Sport", logo_width=70)


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