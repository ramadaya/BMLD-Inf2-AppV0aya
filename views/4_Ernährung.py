import streamlit as st
import pandas as pd
from functions.cycle_utils import get_current_phase, PHASE_INFO


def render_header():
    """Show page logo and title."""
    col1, col2 = st.columns([1, 5])

    with col1:
        st.image("docs/logo.png", width=70)

    with col2:
        st.title("🍓 Ernährung")


def get_data_df():
    """Return shared app data from session state."""
    if "data_df" not in st.session_state:
        st.session_state["data_df"] = pd.DataFrame()
    return st.session_state["data_df"]


def render_nutrition_recommendations(info):
    """Show nutrition tips for the current phase."""
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
        unsafe_allow_html=True,
    )


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


def render_recipe_form(info):
    """Show form for adding a new recipe."""
    st.markdown("---")
    st.subheader("📖 Mein Phasen-Kochbuch")

    with st.expander("➕ Neues Rezept hinzufügen"):
        with st.form("recipe_form"):
            recipe_name = st.text_input(
                "Rezeptname",
                placeholder="z.B. Spinat-Linsen-Suppe",
            )

            ingredients = st.text_area(
                "Zutaten",
                placeholder="z.B.\n- 200g Spinat\n- 1 Dose Linsen\n- 1 Zwiebel",
            )

            instructions = st.text_area(
                "Zubereitung",
                placeholder="z.B.\n1. Zwiebel anbraten\n2. Linsen hinzufügen\n...",
            )

            save_button = st.form_submit_button("Rezept speichern")

            if save_button:
                if recipe_name.strip():
                    save_recipe(
                        recipe_name=recipe_name,
                        ingredients=ingredients,
                        instructions=instructions,
                        phase_name=info["name"],
                    )
                    st.success("✅ Rezept gespeichert!")
                    st.rerun()
                else:
                    st.warning("Bitte gib zuerst einen Rezeptnamen ein.")


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


def render_recipe_list(recipes_df, info):
    """Show saved recipes for the current phase."""
    if recipes_df.empty:
        st.caption(
            "Noch keine Rezepte für diese Phase gespeichert. "
            "Füge dein erstes Rezept hinzu! 🌸"
        )
        return

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
                unsafe_allow_html=True,
            )

            if st.button("🗑 Löschen", key=f"delete_recipe_{index}"):
                delete_recipe(index)
                st.rerun()


render_header()

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