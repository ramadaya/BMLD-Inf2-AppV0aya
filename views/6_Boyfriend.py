import streamlit as st 
from functions.data_utils import get_data_df, get_calendar_df 
from functions.cycle_utils import get_current_phase
from functions.calendar_utils import build_calendar_events, render_calendar
from functions.render import render_header, render_partner_tips



render_header("❤️ Boyfriend", logo_width=70)




data_df = get_data_df()
calendar_df = get_calendar_df(data_df)

events, _ = build_calendar_events(calendar_df)
render_calendar(events)

phase = get_current_phase()
render_partner_tips(phase)