import sys
import os
from turtle import pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from cycle_utils import get_current_phase, PHASE_INFO

st.title("🍓 Ernährung")

RECIPES_FILE = "recipes.csv"

# --- Load saved recipes ---
if os.path.exists(RECIPES_FILE):
    recipes_df = pd.read_csv(RECIPES_FILE)
else:
    recipes_df = pd.DataFrame(columns=["Name", "Zutaten", "Anleitung"])

phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum Kalender!")
else:
    info = PHASE_INFO[phase]
    st.markdown(f"## Empfehlungen für die {info['name']}")

    items = "".join(f"<li> {tip}</li>" for tip in info["nutrition"])

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

# --- Recipe section ---
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
                "Phase": info["name"],
                "Rezeptname": recipe_name,
                "Zutaten": ingredients,
                "Zubereitung": instructions,
                "Datum": str(pd.Timestamp.today().date())
            }])
            recipes_df = pd.concat([recipes_df, new_recipe], ignore_index=True)
            recipes_df.to_csv(RECIPES_FILE, index=False)
            st.success("✅ Rezept gespeichert!")

# --- Show recipes for current phase ---
phase_recipes = recipes_df[recipes_df["Phase"] == info["name"]]

if not phase_recipes.empty:
    st.markdown(f"#### 🍳 Rezepte für die {info['name']}:")

    for _, row in phase_recipes.iloc[::-1].iterrows():  # newest first
        with st.expander(f"🍽️ {row['Rezeptname']}"):
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

# Delete button
    if st.button(f"🗑️ Löschen", key=f"delete_{row['Rezeptname']}_{row['Datum']}"):
        recipes_df = recipes_df[
            ~((recipes_df["Rezeptname"] == row["Rezeptname"]) &
            (recipes_df["Datum"] == row["Datum"]))
        ]
        recipes_df.to_csv(RECIPES_FILE, index=False)
        st.rerun()
    else:
        st.caption("Noch keine Rezepte für diese Phase gespeichert. Füge dein erstes Rezept hinzu! 🌸")