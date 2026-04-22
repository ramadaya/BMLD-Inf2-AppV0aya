import streamlit as st

st.title("Berry Cycle 🍓")

# Begrüssung
if "user" in st.session_state:
    st.write(f"Hallo {st.session_state['user']} 👋")

# Zyklustag
zyklustag = st.number_input("An welchem Zyklustag bist du heute?", 1, 28)

# Phase bestimmen
if zyklustag <= 5:
    phase = "Menstruation"
    info = "Dein Körper braucht Ruhe 🧘‍♀️"
elif zyklustag <= 13:
    phase = "Follikelphase"
    info = "Du hast mehr Energie 💪"
elif zyklustag == 14:
    phase = "Ovulation"
    info = "Du bist besonders aktiv ⚡"
else:
    phase = "Lutealphase"
    info = "Nimm dir Zeit für dich 💆‍♀️"

# Anzeigen
st.success(f"Aktuelle Phase: {phase}")
st.info(info)








# !! WICHTIG: Eure Emails müssen in der App erscheinen!!

"""
Diese App wurde von folgenden Personen entwickelt:
- Aya Ramadan (ramadaya@students.zhaw.ch)
- Carolina Tresch (tresccar@students.zhaw.ch)
- Sofia Lercara (lercasof@students.zhaw.ch)

Diese App ist das leere Gerüst für die App-Entwicklung im Modul Informatik 2 (BMLD/ZHAW)

Autor: Samuel Wehrli (wehs@zhaw.ch)
"""
