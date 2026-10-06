-- PostgreSQL version of the retail analysis queries

-- 1. Monthly revenue and order volume
SELECT
  TO_CHAR(order_date, 'YYYY-MM') AS month,
  COUNT(*) AS orders,
  ROUND(SUM(revenue)::numeric, 2) AS revenue,
  ROUND(AVG(revenue)::numeric, 2) AS avg_order_value
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month;

-- 2. Revenue by product category
SELECT
  p.category,
  COUNT(*) AS order_lines,
  ROUND(SUM(o.revenue)::numeric, 2) AS revenue
FROM orders o
JOIN products p USING (product_id)
GROUP BY p.category
ORDER BY revenue DESC;

-- 3. Top 10 customers by lifetime revenue
SELECT
  c.customer_id,
  c.region,
  COUNT(o.order_id) AS orders,
  ROUND(SUM(o.revenue)::numeric, 2) AS lifetime_revenue
FROM customers c
JOIN orders o USING (customer_id)
GROUP BY c.customer_id, c.region
ORDER BY lifetime_revenue DESC
LIMIT 10;

-- 4. Repeat customer rate
WITH order_counts AS (
  SELECT customer_id, COUNT(*) AS order_count
  FROM orders
  GROUP BY customer_id
)
SELECT
  COUNT(*) AS purchasing_customers,
  SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
  ROUND(
    100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*),
    1
  ) AS repeat_customer_pct
FROM order_counts;

-- 5. Revenue by region
SELECT
  c.region,
  COUNT(o.order_id) AS orders,
  ROUND(SUM(o.revenue)::numeric, 2) AS revenue,
  ROUND(AVG(o.revenue)::numeric, 2) AS avg_order_value
FROM orders o
JOIN customers c USING (customer_id)
GROUP BY c.region
ORDER BY revenue DESC;

-- 6. Discount usage and revenue
SELECT
  CASE
    WHEN discount_pct = 0 THEN 'No discount'
    ELSE 'Discounted'
  END AS discount_group,
  COUNT(*) AS order_lines,
  ROUND(AVG(revenue)::numeric, 2) AS avg_revenue,
  ROUND(SUM(revenue)::numeric, 2) AS total_revenue
FROM orders
GROUP BY discount_group;

-- 7. Product ranking within category
WITH product_revenue AS (
  SELECT
    p.category,
    p.product_name,
    SUM(o.revenue) AS revenue
  FROM orders o
  JOIN products p USING (product_id)
  GROUP BY p.category, p.product_name
)
SELECT
  category,
  product_name,
  ROUND(revenue::numeric, 2) AS revenue,
  DENSE_RANK() OVER (
    PARTITION BY category
    ORDER BY revenue DESC
  ) AS category_rank
FROM product_revenue
ORDER BY category, category_rank;

-- 8. Customer segmentation by spend quartile
WITH customer_spend AS (
  SELECT customer_id, SUM(revenue) AS total_spend
  FROM orders
  GROUP BY customer_id
),
ranked AS (
  SELECT
    customer_id,
    total_spend,
    NTILE(4) OVER (ORDER BY total_spend DESC) AS spend_quartile
  FROM customer_spend
)
SELECT
  spend_quartile,
  COUNT(*) AS customers,
  ROUND(AVG(total_spend)::numeric, 2) AS avg_spend
FROM ranked
GROUP BY spend_quartile
ORDER BY spend_quartile;
