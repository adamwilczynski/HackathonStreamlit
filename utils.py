import pandas as pd
import functools

@functools.cache
def caclulate_pension_ranges_2025(range_=100):
    """
    https://psz.zus.pl/kategorie/emerytury/struktura-wysokosci-emerytur-po-waloryzacji-w-marcu
    """
    return (
    pd.read_excel("./data/emerytury-marzec-2025.xlsx", header=6)
    .iloc[1:]
    .assign(
        lower_bound=lambda x: x.range.str.replace(',', '.').str.split(' - ').str[0].astype(float),
        upper_bound=lambda x: x.range.str.replace(',', '.').str.split(' - ').str[1].astype(float),
        range_group=lambda x: (x.lower_bound // range_).astype(int),
    )
    .groupby('range_group').agg({
            'lower_bound': 'min',
            'upper_bound': 'max',
            'number': 'sum',
            'percent': 'sum',
            'women_percentage': 'mean',
            'men_percentage': 'mean',
    })
    .reset_index(drop=True)
    .assign(
        men_number=lambda x: x.number * x.men_percentage // 100,
        men_number_cumsum=lambda x: x.men_number.cumsum(),
        women_number=lambda x: x.number * x.women_percentage // 100,
        women_number_cumsum=lambda x: x.women_number.cumsum(),
        number_cumsum=lambda x: x.number.cumsum(),
        percent_cumsum=lambda x: x.percent.cumsum(),
        range=lambda x: x.lower_bound.astype(str).str.cat(x.upper_bound.astype(str), sep=" - "),
    )
    )

@functools.cache
def pension_to_percentile(pension):
    row = int(pension // 100)
    df = caclulate_pension_ranges_2025()
    return min(
        (
            df
            .iloc[min(row, df.shape[0] - 1)]
            ["percent_cumsum"]
        ),
        100
    )
