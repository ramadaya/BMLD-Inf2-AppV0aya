import streamlit as st
from cycle_utils import get_current_phase, PHASE_INFO

st.title("🩺 Symptome")

phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum 📅 Kalender!")
else:
    info = PHASE_INFO[phase]
    st.markdown(f"## Typische Symptome in der {info['name']}")
    st.markdown(
        f"<div style='background-color:{info['color']}22; border-left: 5px solid {info['color']}; padding: 1rem; border-radius: 8px;'>",
        unsafe_allow_html=True
    )
    for symptom in info["symptoms"]:
        st.markdown(f"- 🔍 {symptom}")
    st.markdown("</div>", unsafe_allow_html=True)