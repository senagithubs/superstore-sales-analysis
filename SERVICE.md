# Sales data cleanup and profitability report

A scoped service for converting a sales CSV into a reproducible business report.

## Pilot scope

- One CSV with up to 50,000 rows, one currency, and one agreed date range.
- Up to three business questions, such as monthly revenue, loss-making categories,
  and the relationship between discounts and profit.
- One revision within the agreed scope.

## Deliverables

- Clean CSV and a documented data-quality log.
- Revenue and profitability summary tables.
- A two-page report with findings, limitations, and recommended next steps.
- A reproducible Python script.

## Indicative pricing and delivery

The initial pilot quote is USD 150 fixed. Scope, final price, and delivery date
are agreed after reviewing a sample and confirming metric definitions. The
proposed delivery window is three business days after that agreement, subject
to availability.

An expanded package may include customer segmentation, five questions, and a
recorded walkthrough, with an indicative quote of USD 350. Recurring refreshes
are quoted separately after the first delivery. These are proposed service
offers, not claims about market rates or completed paid engagements.

## Required inputs

1. An anonymized sample and column definitions.
2. The meaning of one row and the order, line, and customer identifiers.
3. Currency, date format, and the treatment of returns and refunds.
4. Sales and profit definitions, including the costs already included.
5. The three decisions the report should support.

## Boundaries

If cost or profit data is unavailable, the scope covers revenue analysis only.
API integrations, live dashboards, forecasting, and causal pricing studies require
a separate estimate. Observed discount/profit relationships do not establish causation.

## Portfolio example

The [retail analysis report](reports/client/report.md) documents a historical sample
dataset: 10,800 source rows, 504 exact duplicates, 302 invalid rows, and 9,994 valid
order lines. It is a reproducible demonstration, not a paying-client case study.
