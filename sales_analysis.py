"""Reproducible analysis of the bundled retail demonstration dataset."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED = {'order_id', 'order_date', 'customer_id', 'category', 'sub_category', 'sales', 'profit', 'discount'}
BANDS = ['0%', '(0%,10%]', '(10%,20%]', '(20%,30%]', '(30%,40%]', '(40%,100%]']


def clean(raw):
    df = raw.copy()
    df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    if len(set(df.columns)) != len(df.columns):
        raise ValueError('Column normalization creates ambiguous duplicate names.')
    if missing := REQUIRED - set(df.columns):
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    audit = {'raw_rows': len(df), 'exact_duplicates_removed': int(df.duplicated().sum())}
    df = df.drop_duplicates().copy()
    df['order_date'] = pd.to_datetime(df.order_date, format='%m/%d/%Y', errors='coerce')
    for col in ['sales', 'profit', 'discount']:
        df[col] = pd.to_numeric(df[col], errors='coerce').replace([np.inf, -np.inf], np.nan)
    for col in ['order_id', 'customer_id', 'category', 'sub_category']:
        df[col] = df[col].astype('string').str.strip().replace('', pd.NA)
    valid = df[list(REQUIRED)].notna().all(axis=1) & df.discount.between(0, 1) & df.sales.ge(0)
    audit['invalid_rows_removed_after_dedup'] = int((~valid).sum())
    df = df.loc[valid].copy()
    if df.empty:
        raise ValueError('No valid order lines remain after cleaning.')
    if 'row_id' in df and df.row_id.duplicated().any():
        raise ValueError('Conflicting row_id values remain; review rather than silently deduplicating.')
    audit['clean_rows'] = len(df)
    df['order_month'] = df.order_date.dt.to_period('M').dt.to_timestamp()
    return df, audit


def summarize(df):
    monthly = df.groupby('order_month').agg(revenue=('sales', 'sum'), profit=('profit', 'sum'))
    yearly = df.groupby(df.order_date.dt.year.rename('year')).agg(revenue=('sales', 'sum'), profit=('profit', 'sum'))
    yearly['margin'] = yearly.profit / yearly.revenue.replace(0, np.nan)
    sub = df.groupby(['category', 'sub_category']).agg(revenue=('sales', 'sum'), profit=('profit', 'sum')).sort_values('profit')
    bands = pd.cut(df.discount, [-.001, 0, .1, .2, .3, .4, 1], labels=BANDS)
    discount = df.groupby(bands.rename('discount_band'), observed=True).agg(lines=('profit', 'size'), avg_profit_per_line=('profit', 'mean'), profit=('profit', 'sum'), revenue=('sales', 'sum'))
    snapshot = df.order_date.max() + pd.Timedelta(days=1)
    rfm = df.groupby('customer_id', sort=True).agg(recency=('order_date', lambda s: (snapshot-s.max()).days), frequency=('order_id', 'nunique'), monetary=('sales', 'sum'))
    # On tiny input files, still retain all five score labels via percentile ranks.
    for metric, score, ascending in [('recency', 'R', False), ('frequency', 'F', True), ('monetary', 'M', True)]:
        if len(rfm) >= 5:
            labels = [1, 2, 3, 4, 5] if ascending else [5, 4, 3, 2, 1]
            rfm[score] = pd.qcut(rfm[metric].rank(method='first'), 5, labels=labels).astype(int)
        else:
            rfm[score] = np.ceil(rfm[metric].rank(method='first', ascending=ascending, pct=True)*5).astype(int)
    rfm['segment'] = np.select([
        (rfm.R >= 4) & (rfm.F >= 4), (rfm.R >= 3) & (rfm.F >= 3),
        (rfm.R >= 4) & (rfm.F <= 2), (rfm.R <= 2) & (rfm.F >= 3),
    ], ['Champions', 'Loyal', 'New / Promising', 'At Risk'], default='Hibernating')
    segments = rfm.groupby('segment').agg(customers=('segment', 'size'), total_spend=('monetary', 'sum')).sort_values('total_spend', ascending=False)
    return {'monthly': monthly, 'yearly': yearly, 'subcategories': sub, 'discounts': discount, 'customers': rfm, 'segments': segments}


def md_table(frame):
    data = frame.reset_index()
    rows = [list(data.columns)] + [[f'{x:,.2f}' if isinstance(x, (float, np.floating)) else str(x) for x in row] for row in data.itertuples(index=False, name=None)]
    return '\n'.join(['| ' + ' | '.join(rows[0]) + ' |', '| ' + ' | '.join(['---']*len(rows[0])) + ' |'] + ['| '+' | '.join(row)+' |' for row in rows[1:]])


def run(input_path, output_dir):
    input_path, output_dir = Path(input_path), Path(output_dir)
    df, audit = clean(pd.read_csv(input_path))
    tables = summarize(df)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, frame in tables.items():
        frame.to_csv(output_dir / f'{name}.csv', float_format='%.6f')
    revenue, profit = float(df.sales.sum()), float(df.profit.sum())
    summary = {**audit, 'input_sha256': hashlib.sha256(input_path.read_bytes()).hexdigest(),
               'start': str(df.order_date.min().date()), 'end': str(df.order_date.max().date()),
               'orders': int(df.order_id.nunique()), 'customers': int(df.customer_id.nunique()),
               'revenue': revenue, 'profit': profit, 'margin': profit/revenue if revenue else None,
               'negative_subcategory_profit': float(tables['subcategories'].query('profit < 0').profit.sum())}
    (output_dir / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    years = tables['yearly'].copy(); years['margin_percent'] = years.pop('margin')*100
    loss = tables['subcategories'].query('profit < 0')
    negative_bands = ', '.join(str(x) for x in tables['discounts'].query('avg_profit_per_line < 0').index) or 'none'
    margin_label = f'{profit/revenue:.2%}' if revenue else 'undefined (zero revenue)'
    report = f'''# Retail sales and profitability review

Portfolio demonstration by Sena Inankul. Source: the Superstore-style CSV bundled
in this repository; historical/sample data, not a client engagement. Monetary amounts
are interpreted as USD for this demo. No current business performance is implied.

## Questions and results

Period: {summary['start']} to {summary['end']}. {len(df):,} order lines,
{summary['orders']:,} orders and {summary['customers']:,} customers.
Revenue: **${revenue:,.2f}**. Profit: **${profit:,.2f}**. Overall margin: **{margin_label}**.

### 1. Is growth profitable?

{md_table(years)}

Compare annual profit / annual revenue. An overall margin does not demonstrate a
flat margin over time. Report revenue, profit and weighted margin together.

### 2. Which subcategories lose money?

{md_table(loss)}

Review discount mix, prices and costs in these subcategories. Historical aggregate
losses do not prove every additional sale loses money. A pricing test must measure
both margin and demand before broad changes.

### 3. How do discounts relate to profit?

{md_table(tables['discounts'])}

Intervals are right-closed: (20%,30%] excludes 20% and includes 30%.
Bands with negative average profit per line: {negative_bands}. This is an
association, not a causal estimate: product/customer mix differs across bands.
Pilot approval rules on comparable products and measure revenue and profit together.

### 4. Which customers should be reviewed for retention?

{md_table(tables['segments'])}

Scores use quintiles with ties broken deterministically by sorted customer ID.
Segment names use R and F; M is reported separately. The reference date is the day
after the last order. “At Risk” is a heuristic, not a churn prediction. Test a small
win-back campaign against a holdout; ROI needs campaign costs and incremental results.

## Data checks and limits

- Raw rows: {audit['raw_rows']:,}; exact duplicates removed: {audit['exact_duplicates_removed']:,}.
- Invalid rows removed after deduplication: {audit['invalid_rows_removed_after_dedup']:,}; retained: {len(df):,}.
- Critical fields, finite numeric values, nonnegative sales and discounts in [0,1] required.
- Input SHA-256: `{summary['input_sha256']}`.
- Shipping/operating expenses beyond the supplied profit field are not modelled.
- Snapshot reporting; no causal pricing model, revenue forecast or promised savings.

## Next business actions

1. Validate the definition of profit with the data owner.
2. Review loss-making subcategories and discount mix at product level.
3. Run a controlled pricing or retention pilot before changing policy.
'''
    (output_dir / 'report.md').write_text(report)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/superstore.csv')
    parser.add_argument('--output', default='reports/client')
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output), indent=2))
