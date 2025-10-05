import streamlit as st
import pandas as pd
import plotly.express as px

import utils

st.set_page_config(
    layout="wide",
    page_icon="🧓",
)

st.title("To tylko pierwotna wersja prototypu. To nie jest finalna wersja naszej aplikacji!")

st.title("👵 Symulator emerytalny 👴")

st.header("Analiza podstawowa")

st.subheader(
    "Ile faktycznie dostaniesz na emeryturze? "
    "Nie zgaduj – oblicz to w 2 minuty. "
    "Podaj kilka podstawowych informacji i zobacz, czy będzie Cię stać na spokojne życie po 60-tce."
)

goal_pension = st.number_input(
    "Jaka emerytura Ci się marzy? Wpisz kwotę – pokażemy Ci, co zrobić, żeby rzeczywiście tyle dostać.",
    min_value=0.0,
    step=100.0,
)

st.caption(
"Nie musisz brać pod uwagę inflacji. "
"Podaj kwotę, która byłaby dla Ciebie satysfakcjonująca, gdybyś miał(a)byś być na emeryturze właśnie teraz. "
)

def get_pension_custom_message(percentile: int):
    if percentile < 25:
        message = " To może nie wystarczyć na godne życie."
        separator = "aż"
    elif percentile < 50:
        message = "Będziesz musiał mocno się ograniczać."
        separator = "ponad"
    elif percentile < 75:
        message = "Możesz liczyć na komfortową emeryturę"
        separator = "tylko"
    else:
        message = "Będziesz należeć do emerytalnej elity."
        separator = "wyłącznie"
    return message + f" Obecnie {separator} **{round(100 - percentile, 2)}%** Polaków ma emeryturę większą, niż Twoja."


if goal_pension > 0:
    percentile = utils.pension_to_percentile(goal_pension)

    st.subheader("Werdykt 🧑‍⚖️")
    st.markdown(get_pension_custom_message(percentile))

    range_ = 500
    pension_ranges = utils.calculate_pension_ranges_2025(range_)

    df = utils.calculate_pension_ranges_2025(range_)
    df['color'] = df['lower_bound'].apply(lambda x: 'Emerytura mniejsza bądź równa Twojej' if x <= goal_pension else 'Emerytura większa od Twojej')
    first_greater = df.shape[0] - sum([x > goal_pension for x in df.lower_bound.to_list()])

    st.subheader("Procent osób z emeryturą równą, bądź niższą")
    fig = px.bar(
        df,
        x='range',
        y='percentage_cumsum',
        color='color',
        color_discrete_map={'Emerytura większa od Twojej': '#f05e5e', 'Emerytura mniejsza bądź równa Twojej': '#00993f'},
        labels={
            "percentage_cumsum": "",
            "range": "Zakres",
            "color": "",
        },
    )
    fig.add_vline(
        x=3,  # Position between bars (adjust based on your data)
        line_color="black",
        line_dash="dash",
        line_width=2,
        annotation_text=f"Emerytura minimalna 1878 zł",
        annotation_font_color="black",
    )
    fig.add_vline(
        x=15.0,  # Position between bars (adjust based on your data),
        line_color="black",
        line_width=2,
        annotation_text="Mediana zarobków 7262 zł",
        annotation_font_color="black",
    )
    fig.add_vline(
        x=first_greater - 0.5,  # Position between bars (adjust based on your data)
        line_color="#ffb34f",
        line_width=2,
        annotation_text=f"Twoja wymarzona emerytura {int(goal_pension)} zł",
        annotation_position="top",
        annotation_font_color="#ffb34f",
    )
    fig.update_layout(hovermode=False)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Jak to możliwe, że aż 9.5% Polaków otrzymuje świadczenia emerytalne poniżej kwoty minimalnej?",
            icon="😱"
        ):
            st.text(
                "👉 świadczeniobiorcy otrzymujący emeryturę w wysokości poniżej minimalnej wykazywali "
            "się niską aktywnością zawodową, nie przepracowali minimum 25 lat dla mężczyzn i 20 lat "
            "dla kobiet, w związku z tym nie nabyli prawa do gwarancji minimalnej emerytury 👈"
            )
    with col2:
        if st.button(
            "Losuj ciekawostę",
            icon="🎲"
        ):
            st.text(utils.get_random_interesting_fact())

    # st.header("Analiza pogłębiona")
    # st.text()
    #
    # age = st.number_input(
    #     label="Wiek",
    #     value=30,
    #     min_value=16,
    #     max_value=100,
    # )
    #
    # sex = st.radio(
    #     "Płeć",
    #     ["male", "female"],
    # )