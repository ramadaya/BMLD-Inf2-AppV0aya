import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from cycle_utils import get_current_phase, PHASE_INFO

st.title("🍓 Ernährung")

phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum Kalender!")
else:
    info = PHASE_INFO[phase]
    st.markdown(f"## Ernährungstipps für die {info['name']}")
    st.markdown(
        f"<div style='background-color:{info['color']}22; border-left: 5px solid {info['color']}; padding: 1rem; border-radius: 8px;'>",
        unsafe_allow_html=True
    )
    for food in info["nutrition"]:
        st.markdown(f"- {food}")
    st.markdown("</div>", unsafe_allow_html=True)