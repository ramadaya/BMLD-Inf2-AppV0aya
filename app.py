import streamlit as st
import pandas as pd 
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
st.set_page_config(page_title="Meine App", page_icon=":material/home:")

data_manager = DataManager(       
    fs_protocol='webdav',         
    fs_root_folder="Berry_Cycle"  
    )
st.session_state["data_manager"] = data_manager 
login_manager = LoginManager(data_manager) 
login_manager.login_register()             

current_user = st.session_state.get("username")

if st.session_state.get("loaded_user") != current_user:
    st.session_state["data_df"] = data_manager.load_user_data(
        "data.csv",
        initial_value=pd.DataFrame()
    )
    st.session_state["loaded_user"] = current_user

pg_home = st.Page("views/1_home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/2_Kalender.py", title="📆 Kalender")
pg_third = st.Page("views/3_Sport.py", title="👟 Sport")
pg_fourth = st.Page("views/4_Ernährung.py", title="🍓 Ernährung")
pg_fifth = st.Page("views/5_Symptome.py", title="🩺 Symptome")
pg_sixth = st.Page("views/6_Boyfriend.py", title="❤️ Boyfriend")
pg = st.navigation([pg_home, pg_second, pg_third, pg_fourth, pg_fifth, pg_sixth])
pg.run()
