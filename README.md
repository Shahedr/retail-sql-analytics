# Retail SQL Analytics

I made this project to practice answering business questions directly in SQL instead of doing the analysis first in pandas.

The dataset is synthetic by design: it gives me a small, reproducible retail schema with customers, products, and orders that I can rebuild locally and query from scratch. The numbers below are therefore **SQL exercise results, not real company performance**.

## Questions I worked through

- How is revenue changing month to month?
- Which product categories contribute the most revenue?
- Who are the highest-value customers?
- What share of purchasing customers ordered more than once?
- How do regions compare on revenue and average order value?
- What does discount usage look like?
- How can products be ranked within category?
- How can customers be segmented into spend quartiles?

## Dataset

The generator creates:

- **900** order records
- **220** customers
- **12** products across four categories
- one year of order dates
- quantity and discount variation

A fixed random seed is used so the same data and results can be reproduced.

## Results snapshot

- Total order lines: **900**
- Total revenue: **$85,032.45**
- Average order value: **$94.48**
- Highest-revenue category: **Electronics ($44,947.00)**
- Repeat-customer rate in the generated data: **92.2%**

That repeat rate is intentionally treated as a property of the generated sample—not as a realistic retail benchmark.

## SQL covered

The query set uses joins, grouped KPIs, CTEs, `DENSE_RANK()`, `NTILE()`, customer-level aggregation, and repeat-purchase logic.

I kept a SQLite-oriented query file for quick local use and added a PostgreSQL version so the date functions match the database instead of pretending the syntax is identical.

## Files

```text
retail-sql-analytics/
├── src/
│   ├── generate_data.py
│   └── build_results.py
├── sql/
│   ├── schema.sql
│   ├── analysis_queries.sql
│   └── analysis_queries_postgres.sql
├── results/
│   └── summary.md
├── requirements.txt
└── README.md
```

## Run it

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/build_results.py
```

`sql/analysis_queries.sql` uses SQLite date syntax. Use `sql/analysis_queries_postgres.sql` when loading the same generated tables into PostgreSQL.

## Stack

SQL · SQLite · PostgreSQL · Python · pandas

## What I would change with real retail data

With a real transactional dataset, I would spend more time validating order grain, returns/cancellations, customer identity, product history, and the definition of “repeat customer” before turning these queries into business KPIs.
