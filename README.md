# Superstore Sales & Profitability Analysis

End-to-end exploratory analysis of ~10K retail order lines (4 years, 793 customers, 5,009 orders): data quality audit, cleaning, profitability deep-dive, discount-policy analysis and RFM customer segmentation.

**The one-line story:** revenue grows, but margin sits at **12.5%** and three sub-categories quietly destroyed **$22K** of profit - and the data says exactly what to do about it.

## Key findings

**1. Growth is real; profitable growth is not.** Revenue shows strong seasonality and YoY growth while profit stays nearly flat. Revenue-first reporting hides this.

![Monthly trend](reports/figures/trend.png)

**2. Three product lines lose money.** Tables, Bookcases and Supplies are loss-making despite meaningful revenue - selling more of them makes the business worse.

![Profit by sub-category](reports/figures/subcategory_profit.png)

**3. The discount cliff is at 20%.** Average profit per order line is healthy up to 20% discount, then collapses; lines at 30%+ are loss-making. A 20% discount ceiling directly protects margin.

![Discount cliff](reports/figures/discount_cliff.png)

**4. A small customer elite drives most value.** RFM segmentation (Recency / Frequency / Monetary quintiles) shows Champions and Loyal customers dominate revenue, while the At Risk segment - previously frequent buyers gone quiet - is the highest-ROI win-back target.

![RFM segments](reports/figures/rfm_segments.png)

## Reproduce

Install dependencies with pip install -r requirements.txt, then open analysis.ipynb - or just read the notebook on GitHub, all outputs are baked in. Every number above is computed in the notebook from the raw CSV in the data folder - nothing is hand-typed.

**Tools:** Python, pandas, matplotlib, Jupyter

**Data:** Public Superstore retail dataset, mirrored in data/superstore.csv
