import pandas as pd
import pytest
from sales_analysis import clean, summarize, run


def test_cleaning_audit_and_totals_reconcile(tmp_path):
    result = run('data/superstore.csv', tmp_path)
    assert result['raw_rows'] == 10800
    assert result['exact_duplicates_removed'] == 504
    assert result['invalid_rows_removed_after_dedup'] == 302
    assert result['clean_rows'] == 9994
    assert result['revenue'] == pytest.approx(2297200.8603)
    assert result['profit'] == pytest.approx(286397.0217)
    for table, field in [('yearly', 'revenue'), ('monthly', 'revenue'), ('segments', 'total_spend'), ('discounts', 'revenue')]:
        assert pd.read_csv(tmp_path / f'{table}.csv')[field].sum() == pytest.approx(result['revenue'])


def test_discount_boundaries_and_frequency_are_not_line_count():
    raw = pd.DataFrame({
        'order_id': ['a', 'a', 'b', 'c'], 'order_date': ['01/01/2018']*4,
        'customer_id': ['x']*4, 'category': ['c']*4, 'sub_category': ['s']*4,
        'sales': [10, 20, 30, 40], 'profit': [1, 2, -3, -4], 'discount': [0, .2, .3, .4],
    })
    df, _ = clean(raw)
    result = summarize(df)
    assert result['customers'].loc['x', 'frequency'] == 3
    assert result['discounts'].loc['(10%,20%]', 'lines'] == 1
    assert result['discounts'].loc['(20%,30%]', 'avg_profit_per_line'] == -3


def test_invalid_rows_do_not_silently_become_zero():
    raw = pd.DataFrame({
        'order_id': ['a','b','c','d'], 'order_date': ['01/01/2018']*4,
        'customer_id': ['x']*4, 'category': ['c']*4, 'sub_category': ['s']*4,
        'sales': [10,'bad',float('inf'),20], 'profit': [1]*4, 'discount': [0,0,0,1.1],
    })
    df, audit = clean(raw)
    assert audit['invalid_rows_removed_after_dedup'] == 3
    assert df.sales.sum() == 10
