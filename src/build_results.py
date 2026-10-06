from pathlib import Path
import sqlite3
import pandas as pd

DB = sqlite3.connect(':memory:')
for name in ['customers','products','orders']:
    pd.read_csv(f'data/{name}.csv').to_sql(name, DB, index=False, if_exists='replace')

queries = {
    'monthly_revenue': """
        SELECT strftime('%Y-%m', order_date) month, COUNT(*) orders,
               ROUND(SUM(revenue),2) revenue, ROUND(AVG(revenue),2) avg_order_value
        FROM orders GROUP BY month ORDER BY month
    """,
    'category_revenue': """
        SELECT p.category, COUNT(*) order_lines, ROUND(SUM(o.revenue),2) revenue
        FROM orders o JOIN products p USING(product_id)
        GROUP BY p.category ORDER BY revenue DESC
    """
}
Path('results').mkdir(exist_ok=True)
for name, query in queries.items():
    pd.read_sql_query(query, DB).to_csv(f'results/{name}.csv', index=False)

summary = pd.read_sql_query('''
WITH oc AS (SELECT customer_id, COUNT(*) n FROM orders GROUP BY customer_id)
SELECT COUNT(*) order_lines, ROUND(SUM(revenue),2) total_revenue,
       ROUND(AVG(revenue),2) avg_order_value,
       ROUND(100.0*(SELECT COUNT(*) FROM oc WHERE n>1)/(SELECT COUNT(*) FROM oc),1) repeat_customer_pct
FROM orders
''', DB).iloc[0]
top = pd.read_sql_query('''SELECT p.category, ROUND(SUM(o.revenue),2) revenue
FROM orders o JOIN products p USING(product_id)
GROUP BY p.category ORDER BY revenue DESC LIMIT 1''', DB).iloc[0]
Path('results/summary.md').write_text(
    '# Results Snapshot\n\n'
    f"- Total order lines: **{int(summary.order_lines):,}**\n"
    f"- Total revenue: **${summary.total_revenue:,.2f}**\n"
    f"- Average order value: **${summary.avg_order_value:,.2f}**\n"
    f"- Top category by revenue: **{top.category} (${top.revenue:,.2f})**\n"
    f"- Repeat-customer rate: **{summary.repeat_customer_pct:.1f}%**\n\n"
    'Generated from the deterministic synthetic dataset in `src/generate_data.py`.\n'
)
print(Path('results/summary.md').read_text())
