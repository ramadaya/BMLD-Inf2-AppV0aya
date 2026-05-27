import streamlit as st 
import pandas as pd


def get_data_df():
    """Return shared app data from session state."""
    if "data_df" not in st.session_state:
        st.session_state["data_df"] = pd.DataFrame()
    return st.session_state["data_df"]
