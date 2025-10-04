import pandas as pd
import functools

def get_pension_ranges_2025():
    return (
        pd.read_excel("./data/emerytury-marzec-2025.xlsx", header=6)
        .iloc[1:]
        .assign(
            lower_bound=lambda x: x.range.str.replace(',', '.').str.split(' - ').str[0].astype(float),
            upper_bound=lambda x: x.range.str.replace(',', '.').str.split(' - ').str[1].astype(float),
            men_number=lambda x: x.number * x.men_percentage // 100,
            men_number_cumsum=lambda x: x.men_number.cumsum(),
            women_number=lambda x: x.number * x.women_percentage // 100,
            women_number_cumsum=lambda x: x.women_number.cumsum(),
            number_cumsum=lambda x: x.number.cumsum(),
            percentage_cumsum=lambda x: x.percentage.cumsum(),
        )
    )

@functools.cache
def calculate_pension_ranges_2025(range_=100):
    """
    https://psz.zus.pl/kategorie/emerytury/struktura-wysokosci-emerytur-po-waloryzacji-w-marcu
    """
    return (
        get_pension_ranges_2025()
        .assign(
            range_group=lambda x: (x.lower_bound // range_).astype(int),
        )
        .groupby('range_group').agg({
            'lower_bound': 'min',
            'upper_bound': 'max',
            'men_number': 'sum',
            'women_number': 'sum',
            'number': 'sum',
            'percentage': 'sum',
        })
        .assign(
            range=lambda x: x.lower_bound.astype(str).str.cat(x.upper_bound.astype(str), sep=" - "),
            men_number_cumsum=lambda x: x.men_number.cumsum(),
            women_number_cumsum=lambda x: x.women_number.cumsum(),
            number_cumsum=lambda x: x.number.cumsum(),
            percentage_cumsum=lambda x: x.percentage.cumsum(),
        )
        .reset_index(drop=True)
    )

@functools.cache
def pension_to_percentile(pension):
    range_ = 100
    row = int(pension // range_)
    df = calculate_pension_ranges_2025(range_)
    df_value = (
        df
        .iloc[min(row, df.shape[0] - 1)]
        ["percentage_cumsum"]
    )
    return min(
        df_value,
        100
    )
