import streamlit as st
from functions.cycle_utils import get_current_phase, PHASE_INFO
from functions.render import render_header
from functions.symptom_render import render_typical_symptoms,render_symptom_tracking, render_statistics, render_notes

render_header("🩺 Symptome", logo_width=70)


phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum 📅 Kalender!")
else:
    info = PHASE_INFO[phase]

    render_typical_symptoms(info)
    render_symptom_tracking(info)
    render_statistics()
    render_notes(info)
