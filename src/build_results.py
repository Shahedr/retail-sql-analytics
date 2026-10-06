from pathlib import Path
import sqlite3

import pandas as pd

DATA_DIR = Path("data")
RESULTS_DIR = Path("results")


def load_tables(connection):
    for table_name in ["customers", "products", "orders"]:
        df = pd.read_csv(DATA_DIR / f"{table_name}.csv")
        df.to_sql(
            table_name,
            connection,
            index=False,
            if_exists="replace",
        )


def export_query_results(connection):
    queries = {
        "monthly_revenue": """
            SELECT
                strftime('%Y-%m', order_date) AS month,
                COUNT(*) AS orders,
                ROUND(SUM(revenue), 2) AS revenue,
                ROUND(AVG(revenue), 2) AS avg_order_value
            FROM orders
            GROUP BY month
            ORDER BY month
        """,
        "category_revenue": """
            SELECT
                p.category,
                COUNT(*) AS order_lines,
                ROUND(SUM(o.revenue), 2) AS revenue
            FROM orders o
            JOIN products p USING (product_id)
            GROUP BY p.category
            ORDER BY revenue DESC
        """,
    }

    RESULTS_DIR.mkdir(exist_ok=True)

    for result_name, query in queries.items():
        result = pd.read_sql_query(query, connection)
        result.to_csv(RESULTS_DIR / f"{result_name}.csv", index=False)


def build_summary(connection):
    summary_query = """
        WITH order_counts AS (
            SELECT customer_id, COUNT(*) AS order_count
            FROM orders
            GROUP BY customer_id
        )
        SELECT
            COUNT(*) AS order_lines,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(AVG(revenue), 2) AS avg_order_value,
            ROUND(
                100.0 *
                (SELECT COUNT(*) FROM order_counts WHERE order_count > 1) /
                (SELECT COUNT(*) FROM order_counts),
                1
            ) AS repeat_customer_pct
        FROM orders
    """

    top_category_query = """
        SELECT
            p.category,
            ROUND(SUM(o.revenue), 2) AS revenue
        FROM orders o
        JOIN products p USING (product_id)
        GROUP BY p.category
        ORDER BY revenue DESC
        LIMIT 1
    """

    summary = pd.read_sql_query(summary_query, connection).iloc[0]
    top_category = pd.read_sql_query(top_category_query, connection).iloc[0]

    summary_text = (
        "# Results Snapshot\n\n"
        f"- Total order lines: **{int(summary.order_lines):,}**\n"
        f"- Total revenue: **${summary.total_revenue:,.2f}**\n"
        f"- Average order value: **${summary.avg_order_value:,.2f}**\n"
        f"- Top category by revenue: **{top_category.category} "
        f"(${top_category.revenue:,.2f})**\n"
        f"- Repeat-customer rate: **{summary.repeat_customer_pct:.1f}%**\n\n"
        "These figures come from the reproducible synthetic dataset in "
        "`src/generate_data.py`; they are not real company KPIs.\n"
    )

    output_path = RESULTS_DIR / "summary.md"
    output_path.write_text(summary_text)
    return output_path


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    with sqlite3.connect(":memory:") as connection:
        load_tables(connection)
        export_query_results(connection)
        summary_path = build_summary(connection)

    print(summary_path.read_text())


if __name__ == "__main__":
    main()
