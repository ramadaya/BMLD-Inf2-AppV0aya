import streamlit as st
import pandas as pd
import plotly.express as px
from functions.cycle_utils import get_current_phase, PHASE_INFO
from functions.data_utils import get_data_df
from functions.render import render_header

SYMPTOM_COLS = [
    "⚡️ Energie",
    "😣 Schmerzen",
    "🧠 Fokus",
    "🍫 Heißhunger",
    "😴 Müdigkeit",
    "😊 Stimmung",
]

render_header("🩺 Symptome", logo_width=70)


def save_data():
    st.session_state["data_manager"].save_user_data(
        st.session_state["data_df"],
        "data.csv"
    )


def get_phase_name_for_date(selected_date):
    data_df = st.session_state["data_df"]

    if data_df.empty or "Typ" not in data_df.columns:
        return None

    calendar_df = data_df[data_df["Typ"] == "Kalender"].copy()
    calendar_df = calendar_df.dropna(
        subset=["Datum", "Zykluslänge", "Periodendauer"]
    )

    if calendar_df.empty:
        return None

    calendar_df["Datum"] = pd.to_datetime(
        calendar_df["Datum"],
        errors="coerce"
    ).dt.date

    last = calendar_df.iloc[-1]

    period_start = last["Datum"]
    cycle_length = int(last["Zykluslänge"])
    period_length = int(last["Periodendauer"])

    selected_date = pd.to_datetime(selected_date).date()
    day_of_cycle = ((selected_date - period_start).days % cycle_length) + 1
    ovulation_day = cycle_length - 14

    if day_of_cycle <= period_length:
        return "🔴 Menstruation"

    if day_of_cycle <= ovulation_day - 1:
        return "🌱 Follikelphase"

    if day_of_cycle <= ovulation_day + 2:
        return "✨ Eisprung"

    return "🌙 Lutealphase"


def get_symptoms_df():
    data_df = st.session_state["data_df"]

    if data_df.empty or "Typ" not in data_df.columns:
        return pd.DataFrame(columns=["Typ", "Datum", "Phase"] + SYMPTOM_COLS)

    return data_df[data_df["Typ"] == "Symptom"].copy()


def render_typical_symptoms(info):
    st.markdown(f"## Typische Symptome in der {info['name']}")

    items = "".join(
        f"<li>{symptom}</li>"
        for symptom in info["symptoms"]
    )

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


def render_symptom_tracking(info):
    st.markdown("---")
    st.subheader("📊 Tägliches Symptom-Tracking")

    symptoms_df = get_symptoms_df()

    selected_date = st.date_input(
        "Datum",
        value=pd.Timestamp.today()
    )

    selected_date_str = str(selected_date)
    selected_phase = get_phase_name_for_date(selected_date)

    if selected_phase:
        st.caption(f"Phase an diesem Datum: {selected_phase}")

    already_logged = (
        not symptoms_df.empty
        and "Datum" in symptoms_df.columns
        and selected_date_str in symptoms_df["Datum"].astype(str).values
    )

    if already_logged:
        st.success("✅ Für dieses Datum wurden bereits Symptome eingetragen.")

        if st.button("✏️ Eintrag bearbeiten"):
            st.session_state["data_df"] = st.session_state["data_df"][
                ~(
                    (st.session_state["data_df"]["Typ"] == "Symptom")
                    & (
                        st.session_state["data_df"]["Datum"].astype(str)
                        == selected_date_str
                    )
                )
            ]

            save_data()
            st.rerun()

        return

    with st.form("symptoms_form"):
        st.markdown("Wie fühlst du dich? (1 = niedrig, 10 = hoch)")

        col1, col2 = st.columns(2)

        with col1:
            energie = st.slider("⚡️ Energie", 1, 10, 5)
            fokus = st.slider("🧠 Fokus", 1, 10, 5)
            muedigkeit = st.slider("😴 Müdigkeit", 1, 10, 5)

        with col2:
            schmerzen = st.slider("😣 Schmerzen", 1, 10, 1)
            heisshunger = st.slider("🍫 Heißhunger", 1, 10, 5)
            stimmung = st.slider("😊 Stimmung", 1, 10, 5)

        save_symptoms = st.form_submit_button("💾 Speichern")

        if save_symptoms:
            new_entry = pd.DataFrame([{
                "Typ": "Symptom",
                "Datum": selected_date_str,
                "Phase": selected_phase,
                "⚡️ Energie": energie,
                "😣 Schmerzen": schmerzen,
                "🧠 Fokus": fokus,
                "🍫 Heißhunger": heisshunger,
                "😴 Müdigkeit": muedigkeit,
                "😊 Stimmung": stimmung,
            }])

            st.session_state["data_df"] = pd.concat(
                [st.session_state["data_df"], new_entry],
                ignore_index=True,
            )

            save_data()
            st.success("✅ Gespeichert!")
            st.rerun()


def render_statistics():
    st.markdown("---")
    st.subheader("📈 Statistiken über Zeit")

    symptoms_df = get_symptoms_df()

    if symptoms_df.empty:
        st.caption("Noch keine Daten vorhanden. Trage täglich deine Symptome ein! 🌸")
        return

    symptoms_df["Datum"] = pd.to_datetime(
        symptoms_df["Datum"],
        errors="coerce"
    )

    symptoms_df = symptoms_df.dropna(subset=["Datum"])

    for symptom in SYMPTOM_COLS:
        symptoms_df[symptom] = pd.to_numeric(
            symptoms_df[symptom],
            errors="coerce"
        )

    tab1, tab2, tab3 = st.tabs(
        ["📅 Verlauf", "🌀 Phasen-Vergleich", "📋 Durchschnitt"]
    )

    with tab1:
        selected = st.multiselect(
            "Symptome auswählen:",
            SYMPTOM_COLS,
            default=["⚡️ Energie", "😊 Stimmung"]
        )

        if selected:
            fig = px.line(
                symptoms_df.sort_values("Datum"),
                x="Datum",
                y=selected,
                title="Symptomverlauf über Zeit",
                markers=True,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            fig.update_layout(
                yaxis=dict(range=[0, 10]),
                plot_bgcolor="rgba(0,0,0,0)",
                legend_title="Symptom"
            )

            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if "Phase" not in symptoms_df.columns:
            st.caption("Noch keine Phasen-Daten vorhanden.")
            return

        phase_avg = (
            symptoms_df.groupby("Phase")[SYMPTOM_COLS]
            .mean()
            .round(1)
            .reset_index()
        )

        fig = px.bar(
            phase_avg.melt(
                id_vars="Phase",
                var_name="Symptom",
                value_name="Durchschnitt"
            ),
            x="Symptom",
            y="Durchschnitt",
            color="Phase",
            barmode="group",
            title="Durchschnitt pro Phase",
            color_discrete_sequence=[
                "#e63946",
                "#f4a261",
                "#2a9d8f",
                "#6a4c93"
            ]
        )

        fig.update_layout(
            yaxis=dict(range=[0, 10]),
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        avg = (
            symptoms_df[SYMPTOM_COLS]
            .mean()
            .round(1)
            .reset_index()
        )

        avg.columns = ["Symptom", "Durchschnitt"]

        fig = px.bar(
            avg,
            x="Symptom",
            y="Durchschnitt",
            title="Gesamtdurchschnitt aller Symptome",
            color="Symptom",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig.update_layout(
            yaxis=dict(range=[0, 10]),
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)


def render_notes(info):
    st.markdown("---")
    st.subheader("📝 Meine Notizen")

    note_date = st.date_input(
        "Notiz-Datum",
        value=pd.Timestamp.today()
    )

    note_phase = get_phase_name_for_date(note_date)

    if note_phase:
        st.caption(f"Phase an diesem Datum: {note_phase}")

    with st.form("notes_form"):
        note_text = st.text_area(
            "Wie fühlst du dich heute?",
            placeholder="z.B. viel Energie, Kopfschmerzen, gute Stimmung..."
        )

        save_note = st.form_submit_button("Notiz speichern")

        if save_note:
            if not note_text.strip():
                st.warning("Bitte schreibe zuerst eine Notiz.")
            else:
                new_note = pd.DataFrame([{
                    "Typ": "Symptom-Notiz",
                    "Datum": str(note_date),
                    "Phase": note_phase,
                    "Notiz": note_text
                }])

                st.session_state["data_df"] = pd.concat(
                    [st.session_state["data_df"], new_note],
                    ignore_index=True
                )

                save_data()
                st.success("✅ Notiz gespeichert!")
                st.rerun()

    data_df = st.session_state["data_df"]

    if data_df.empty or "Typ" not in data_df.columns or "Phase" not in data_df.columns:
        st.caption("Noch keine Notizen für diese Phase gespeichert.")
        return

    phase_notes = data_df[
        (data_df["Typ"] == "Symptom-Notiz")
        & (data_df["Phase"] == info["name"])
    ]

    if phase_notes.empty:
        st.caption("Noch keine Notizen für diese Phase gespeichert.")
        return

    st.markdown(f"#### Frühere Notizen in der {info['name']}:")

    for _, row in phase_notes.iloc[::-1].iterrows():
        st.markdown(
            f"""
            <div style="background-color:{info['color']}11;
                        border-left: 3px solid {info['color']};
                        padding: 0.6rem 1rem;
                        border-radius: 6px;
                        margin-bottom: 0.5rem;">
                <small>📅 {row['Datum']}</small><br>
                {row['Notiz']}
            </div>
            """,
            unsafe_allow_html=True
        )


phase = get_current_phase()

if phase is None:
    st.info("Noch keine Periode eingetragen. Gehe zum 📅 Kalender!")
else:
    info = PHASE_INFO[phase]

    render_typical_symptoms(info)
    render_symptom_tracking(info)
    render_statistics()
    render_notes(info)
