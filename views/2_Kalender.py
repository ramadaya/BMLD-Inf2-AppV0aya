from functions.data_utils import get_data_df, get_calendar_df
from functions.render import render_header
from functions.calendar_utils import render_saved_entries, render_period_form, build_calendar_events, render_calendar, render_legend

render_header("Zyklus-Kalender 🌸", logo_width=70)


data_df = get_data_df()
calendar_df = get_calendar_df(data_df)

render_period_form()

events, next_period = build_calendar_events(calendar_df)

render_calendar(events)
render_legend()
render_saved_entries(calendar_df, next_period)