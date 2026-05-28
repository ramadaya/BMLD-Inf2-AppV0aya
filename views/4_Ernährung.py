import streamlit as st
from functions.cycle_utils import get_current_phase, PHASE_INFO
from functions.data_utils import get_data_df
from functions.render import render_header, render_nutrition_recommendations, render_recipe_list, render_recipe_form
from functions.nutrition_utils import get_phase_recipes

render_header("🍓 Ernährung", logo_width=70)


data_df = get_data_df()
phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum Kalender!")
else:
    info = PHASE_INFO[phase]

    render_nutrition_recommendations(info)
    render_recipe_form(info)

    updated_data_df = get_data_df()
    recipes_df = get_phase_recipes(updated_data_df, info["name"])

    render_recipe_list(recipes_df, info)