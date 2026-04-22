import streamlit as st
import pandas as pd 
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
st.set_page_config(page_title="Meine App", page_icon=":material/home:")

# --- NEW CODE: import and initialize data manager and login manager ---


data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="Berry_Cycle"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in
# --- END OF NEW CODE ---

# --- CODE UPDATE: load user data from data manager if not already present in session state --
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---
pg_home = st.Page("views/1_home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/2_Kalender.py", title="Kalender", icon=":calendar:")
pg_third = st.Page("views/3_Sport.py", title="Sport", icon=":athletic_shoe:")
pg_fourth = st.Page("views/4_Ernährung.py", title="Ernährung", icon=":strawberry:")
pg_fifth = st.Page("views/5_Symptome.py", title="Symptome", icon=":crying_cat_face:")
pg_sixth = st.Page("views/6_Unterseite_e.py", title="Unterseite E", icon=":material/info:")


pg = st.navigation([pg_home, pg_second, pg_third, pg_fourth, pg_fifth, pg_sixth])
pg.run()
