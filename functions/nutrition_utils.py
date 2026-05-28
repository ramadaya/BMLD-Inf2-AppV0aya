import streamlit as st 
import pandas as pd 

def save_recipe(recipe_name, ingredients, instructions, phase_name):
    """Save a new recipe in shared user data."""
    new_recipe = pd.DataFrame([{
        "Typ": "Ernährung-Rezept",
        "Phase": phase_name,
        "Rezeptname": recipe_name,
        "Zutaten": ingredients,
        "Zubereitung": instructions,
        "Datum": str(pd.Timestamp.today().date()),
    }])

    st.session_state["data_df"] = pd.concat(
        [st.session_state["data_df"], new_recipe],
        ignore_index=True,
    )

    st.session_state["data_manager"].save_user_data(
        st.session_state["data_df"],
        "data.csv",
    )


def get_phase_recipes(data_df, phase_name):
    """Return recipes saved for the current phase."""
    if data_df.empty:
        return pd.DataFrame()

    required_cols = {"Typ", "Phase"}
    if not required_cols.issubset(data_df.columns):
        return pd.DataFrame()

    return data_df[
        (data_df["Typ"] == "Ernährung-Rezept")
        & (data_df["Phase"] == phase_name)
    ].copy()

def delete_recipe(index):
    """Delete a recipe and save updated data."""
    st.session_state["data_df"] = st.session_state["data_df"].drop(index)

    st.session_state["data_manager"].save_user_data(
        st.session_state["data_df"],
        "data.csv",
    )

