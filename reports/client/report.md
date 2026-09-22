# Retail sales and profitability review

Portfolio demonstration by Sena Inankul. Source: the Superstore-style CSV bundled
in this repository; historical/sample data, not a client engagement. Monetary amounts
are interpreted as USD for this demo. No current business performance is implied.

## Questions and results

Period: 2015-01-03 to 2018-12-30. 9,994 order lines,
5,009 orders and 793 customers.
Revenue: **$2,297,200.86**. Profit: **$286,397.02**. Overall margin: **12.47%**.

### 1. Is growth profitable?

| year | revenue | profit | margin_percent |
| --- | --- | --- | --- |
| 2015 | 484,247.50 | 49,543.97 | 10.23 |
| 2016 | 470,532.51 | 61,618.60 | 13.10 |
| 2017 | 609,205.60 | 81,795.17 | 13.43 |
| 2018 | 733,215.26 | 93,439.27 | 12.74 |

Compare annual profit / annual revenue. An overall margin does not demonstrate a
flat margin over time. Report revenue, profit and weighted margin together.

### 2. Which subcategories lose money?

| category | sub_category | revenue | profit |
| --- | --- | --- | --- |
| Furniture | Tables | 206,965.53 | -17,725.48 |
| Furniture | Bookcases | 114,880.00 | -3,472.56 |
| Office Supplies | Supplies | 46,673.54 | -1,189.10 |

Review discount mix, prices and costs in these subcategories. Historical aggregate
losses do not prove every additional sale loses money. A pricing test must measure
both margin and demand before broad changes.

### 3. How do discounts relate to profit?

| discount_band | lines | avg_profit_per_line | profit | revenue |
| --- | --- | --- | --- | --- |
| 0% | 4798 | 66.90 | 320,987.60 | 1,087,908.47 |
| (0%,10%] | 94 | 96.06 | 9,029.18 | 54,369.35 |
| (10%,20%] | 3709 | 24.74 | 91,756.30 | 792,152.89 |
| (20%,30%] | 227 | -45.68 | -10,369.28 | 103,226.65 |
| (30%,40%] | 233 | -109.22 | -25,448.19 | 130,911.24 |
| (40%,100%] | 933 | -106.71 | -99,558.59 | 128,632.25 |

Intervals are right-closed: (20%,30%] excludes 20% and includes 30%.
Bands with negative average profit per line: (20%,30%], (30%,40%], (40%,100%]. This is an
association, not a causal estimate: product/customer mix differs across bands.
Pilot approval rules on comparable products and measure revenue and profit together.

### 4. Which customers should be reviewed for retention?

| segment | customers | total_spend |
| --- | --- | --- |
| Champions | 167 | 675,849.82 |
| Loyal | 163 | 534,269.94 |
| At Risk | 146 | 497,495.99 |
| Hibernating | 229 | 430,195.68 |
| New / Promising | 88 | 159,389.43 |

Scores use quintiles with ties broken deterministically by sorted customer ID.
Segment names use R and F; M is reported separately. The reference date is the day
after the last order. “At Risk” is a heuristic, not a churn prediction. Test a small
win-back campaign against a holdout; ROI needs campaign costs and incremental results.

## Data checks and limits

- Raw rows: 10,800; exact duplicates removed: 504.
- Invalid rows removed after deduplication: 302; retained: 9,994.
- Critical fields, finite numeric values, nonnegative sales and discounts in [0,1] required.
- Input SHA-256: `75264adc0cf180c493a2c56ef97e4087b32ad48fe663d600ed4a9f9ca7c183e9`.
- Shipping/operating expenses beyond the supplied profit field are not modelled.
- Snapshot reporting; no causal pricing model, revenue forecast or promised savings.

## Next business actions

1. Validate the definition of profit with the data owner.
2. Review loss-making subcategories and discount mix at product level.
3. Run a controlled pricing or retention pilot before changing policy.
