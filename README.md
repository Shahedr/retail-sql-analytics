# Retail SQL Analytics

SQL case study focused on revenue, customer behavior, product performance, and repeat purchasing using a deterministic synthetic retail dataset.

## Business questions
- How is revenue trending by month?
- Which product categories contribute the most revenue?
- Who are the highest-value customers?
- What percentage of customers purchase more than once?
- How do regions compare on revenue and average order value?
- How does discount usage affect order economics?

## Tools
**SQL · SQLite/PostgreSQL-compatible concepts · CTEs · Window Functions · Aggregations · Joins · Python · pandas**

## Dataset snapshot
- **900** order records
- **220** customers
- **12** products across four categories
- Deterministic synthetic data generated locally; no private company data

## Repository structure
```text
retail-sql-analytics/
├── src/
│   ├── generate_data.py
│   └── build_results.py
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── results/
│   └── summary.md
└── README.md
```

## Run
```bash
pip install pandas numpy
python src/generate_data.py
python src/build_results.py
```

Then load the generated CSVs into SQLite/PostgreSQL and run the queries in `sql/analysis_queries.sql`.

## Current results snapshot
- Total order lines: **900**
- Total revenue: **$85,032.45**
- Average order value: **$94.48**
- Top category by revenue: **Electronics ($44,947.00)**
- Repeat-customer rate: **92.2%**

## What this demonstrates
Relational thinking, joins, KPI calculations, CTEs, window functions, ranking, customer segmentation, repeat-purchase analysis, and translating business questions into reusable SQL.
