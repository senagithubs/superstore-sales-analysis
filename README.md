# Superstore Sales & Profitability Analysis

An end-to-end exploratory analysis of ~10K retail order lines that turns raw sales data into concrete pricing and customer-retention recommendations.

## What it does

- Runs a full data quality audit on ~10,800 raw order lines (4 years, 793 customers, 5,009 orders), then cleans duplicates and unparseable rows down to a reliable analysis set.
- Breaks down revenue and profit trends over time to check whether growth is actually profitable.
- Analyzes profit by category and sub-category to find which product lines quietly destroy margin.
- Models the relationship between discount level and profit to find the point where discounting stops being worth it.
- Segments customers with RFM (Recency, Frequency, Monetary) quintiles to identify the highest-value and highest-risk customer groups.

## Key findings

- Growth is real, profitable growth is not. Revenue shows strong seasonality and year-over-year growth, but overall profit margin stays flat at 12.5% - a revenue-first view hides this.
- Three sub-categories quietly destroy profit. Tables, Bookcases and Supplies lose money overall despite meaningful revenue, having destroyed roughly $22K of profit between them - selling more of them makes results worse, not better.
- There is a discount cliff at 20%. Average profit per order line stays healthy up to a 20% discount, then collapses, with lines discounted 30% or more running at a loss - a 20% discount ceiling (with manager approval required beyond it) would directly protect margin.
- Value is concentrated in a small customer elite. RFM segmentation shows that Champions and Loyal customers drive most revenue, while the At Risk segment - customers who used to buy frequently and have gone quiet - is the highest-ROI win-back target.

## Recommendations

| Finding | Action |
|---|---|
| 12.5% flat margin under growing revenue | Report profit-first, not revenue-first |
| Tables / Bookcases / Supplies lose money | Reprice, renegotiate, or de-emphasize in promotions |
| Profit collapses beyond 20% discount | Enforce a 20% discount ceiling |
| Value concentrated in RFM elite | Protect Champions; targeted win-back for At Risk |

## Tech stack

- Python
- pandas
- matplotlib
- Jupyter

## Quickstart

```bash
pip install -r requirements.txt
jupyter notebook analysis.ipynb
```

The notebook can also be read directly on GitHub without running it - every table and chart in it is already baked in from a previous run.

Data: public Superstore retail dataset (mirrored in data/superstore.csv).
