import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from cycle_utils import get_current_phase, PHASE_INFO

st.title("Berry Cycle 🍓")

# Begrüssung
if "user" in st.session_state:
    st.write(f"Hallo {st.session_state['user']} 👋")

phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum 📅 Kalender und trage deinen Zyklus ein!")
else:
    info = PHASE_INFO[phase]
    st.markdown(f"## Du bist gerade in der {info['name']}")
    st.markdown(
        f"<div style='background-color:{info['color']}22; border-left: 5px solid {info['color']}; padding: 1rem; border-radius: 8px;'>"
        f"<b>💬 Mood:</b> {info['mood']}</div>",
        unsafe_allow_html=True
    )

# !! WICHTIG: Eure Emails müssen in der App erscheinen!!

"""
Diese App wurde von folgenden Personen entwickelt:
- Aya Ramadan (ramadaya@students.zhaw.ch)
- Carolina Tresch (tresccar@students.zhaw.ch)
- Sofia Lercara (lercasof@students.zhaw.ch)

Diese App ist das leere Gerüst für die App-Entwicklung im Modul Informatik 2 (BMLD/ZHAW)

Autor: Samuel Wehrli (wehs@zhaw.ch)
"""
