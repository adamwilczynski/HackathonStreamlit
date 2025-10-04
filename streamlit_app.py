import streamlit as st
import pandas as pd
import plotly.express as px

import utils

st.set_page_config(layout="wide")

st.title("Symulator emerytalny")

st.text("Ciekawy swojej emerytalnej przyszłości? Odpowiedz na kilka prostych pytań i zajrzyj w przyszłość.")

goal_pension = st.number_input(
    "Ile miesięcznie chciałbyś dostawać z emerytury?",
    min_value=0.0,
    step=100.0,
)
st.caption(
"Nie musisz brać pod uwagę inflacji."
"Podaj kwotę, która byłaby dla Ciebie satysfakcjonująca, gdybyś był emerytem właśnie teraz."
)

def get_pension_custom_message(percentile: int):
    if percentile < 25:
        message = "Źle to wygląda."
    elif percentile < 50:
        message = "Nie jest najlepiej."
    elif percentile < 75:
        message = "Wygląda to dobrze."
    else:
        message = "Wygląda to świetnie."
    return message + f" Obecnie {round(100 - percentile, 2)}% Polaków ma emeryturę większą, niż Twoja."


if goal_pension > 0:
    percentile = utils.pension_to_percentile(goal_pension)
    st.write(get_pension_custom_message(percentile))

    range_ = 500
    pension_ranges = utils.caclulate_pension_ranges_2025(range_)

    df = utils.caclulate_pension_ranges_2025(range_)
    df['color'] = df['lower_bound'].apply(lambda x: 'emerytura mniejsza bądź równa' if goal_pension >= x else 'emerytura większa')

    st.header("Procent osób z emeryturą równą, bądź niższą")
    fig = px.bar(
        df,
        x='range',
        y='percent_cumsum',
        color='color',
        color_discrete_map={'emerytura większa': '#f05e5e', 'emerytura mniejsza bądź równa': '#00993f'},
        labels={
            "percent_cumsum": "",
            "range": "Zakres"
        },
    )
    fig.update_layout(hovermode=False)
    st.plotly_chart(fig, use_container_width=True)

