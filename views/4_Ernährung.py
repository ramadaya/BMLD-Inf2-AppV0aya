import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from functions.cycle_utils import get_current_phase, PHASE_INFO

st.title("🍓 Ernährung")

if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame()

data_df = st.session_state["data_df"]

if not data_df.empty and "Typ" in data_df.columns:
    recipes_df = data_df[data_df["Typ"] == "Ernährung-Rezept"].copy()
else:
    recipes_df = pd.DataFrame(
        columns=["Typ", "Phase", "Rezeptname", "Zutaten", "Zubereitung", "Datum"]
    )

phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum Kalender!")
else:
    info = PHASE_INFO[phase]

    st.markdown(f"## Empfehlungen für die {info['name']}")

    items = "".join(f"<li>{tip}</li>" for tip in info["nutrition"])

    st.markdown(
        f"""
        <div style="background-color:{info['color']}22; 
                    border-left: 5px solid {info['color']}; 
                    padding: 1rem; 
                    border-radius: 8px;">
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.subheader("📖 Mein Phasen-Kochbuch")

    with st.expander("➕ Neues Rezept hinzufügen"):
        with st.form("recipe_form"):
            recipe_name = st.text_input("Rezeptname", placeholder="z.B. Spinat-Linsen-Suppe")
            ingredients = st.text_area(
                "Zutaten",
                placeholder="z.B.\n- 200g Spinat\n- 1 Dose Linsen\n- 1 Zwiebel"
            )
            instructions = st.text_area(
                "Zubereitung",
                placeholder="z.B.\n1. Zwiebel anbraten\n2. Linsen hinzufügen\n..."
            )

            save_recipe = st.form_submit_button("Rezept speichern")

            if save_recipe and recipe_name.strip():
                new_recipe = pd.DataFrame([{
                    "Typ": "Ernährung-Rezept",
                    "Phase": info["name"],
                    "Rezeptname": recipe_name,
                    "Zutaten": ingredients,
                    "Zubereitung": instructions,
                    "Datum": str(pd.Timestamp.today().date())
                }])

                st.session_state["data_df"] = pd.concat(
                    [st.session_state["data_df"], new_recipe],
                    ignore_index=True
                )

                st.session_state["data_manager"].save_user_data(
                    st.session_state["data_df"],
                    "data.csv"
                )

                st.success("✅ Rezept gespeichert!")
                st.rerun()

    data_df = st.session_state["data_df"]

    if not data_df.empty and "Typ" in data_df.columns:
        recipes_df = data_df[
            (data_df["Typ"] == "Ernährung-Rezept") &
            (data_df["Phase"] == info["name"])
        ].copy()
    else:
        recipes_df = pd.DataFrame()

    if not recipes_df.empty:
        st.markdown(f"#### 🍳 Rezepte für die {info['name']}:")

        for index, row in recipes_df.iloc[::-1].iterrows():
            with st.expander(f"🍽 {row['Rezeptname']}"):
                st.markdown(
                    f"""
                    <div style="background-color:{info['color']}11; 
                                border-left: 3px solid {info['color']}; 
                                padding: 0.8rem 1rem; 
                                border-radius: 6px;">
                        <b>🛒 Zutaten:</b><br>
                        <p style="white-space: pre-line;">{row['Zutaten']}</p>
                        <b>👩‍🍳 Zubereitung:</b><br>
                        <p style="white-space: pre-line;">{row['Zubereitung']}</p>
                        <small>📅 Hinzugefügt am {row['Datum']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button("🗑 Löschen", key=f"delete_recipe_{index}"):
                    st.session_state["data_df"] = st.session_state["data_df"].drop(index)

                    st.session_state["data_manager"].save_user_data(
                        st.session_state["data_df"],
                        "data.csv"
                    )

                    st.rerun()
    else:
        st.caption("Noch keine Rezepte für diese Phase gespeichert. Füge dein erstes Rezept hinzu! 🌸")