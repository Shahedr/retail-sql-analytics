from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path('data')
OUT.mkdir(exist_ok=True)
RNG = np.random.default_rng(42)

regions = ['Midwest', 'Northeast', 'South', 'West']
customers = pd.DataFrame({
    'customer_id': range(1, 221),
    'region': RNG.choice(regions, 220, p=[0.28, 0.22, 0.28, 0.22]),
    'signup_date': pd.to_datetime('2024-01-01') + pd.to_timedelta(RNG.integers(0, 500, 220), unit='D')
})

products = pd.DataFrame([
    (1, 'Wireless Headphones', 'Electronics', 129.00),
    (2, 'Smart Speaker', 'Electronics', 99.00),
    (3, 'Fitness Tracker', 'Electronics', 149.00),
    (4, 'Desk Lamp', 'Home', 45.00),
    (5, 'Throw Blanket', 'Home', 55.00),
    (6, 'Storage Set', 'Home', 39.00),
    (7, 'Running Shoes', 'Apparel', 89.00),
    (8, 'Everyday Hoodie', 'Apparel', 64.00),
    (9, 'Performance Tee', 'Apparel', 34.00),
    (10, 'Travel Mug', 'Lifestyle', 28.00),
    (11, 'Notebook Set', 'Lifestyle', 18.00),
    (12, 'Backpack', 'Lifestyle', 72.00),
], columns=['product_id','product_name','category','unit_price'])

order_dates = pd.to_datetime('2025-01-01') + pd.to_timedelta(RNG.integers(0, 365, 900), unit='D')
product_ids = RNG.choice(products.product_id, 900, p=[.13,.10,.10,.07,.07,.06,.09,.08,.07,.06,.07,.10])
quantities = RNG.choice([1,2,3], 900, p=[.72,.23,.05])
discounts = RNG.choice([0, 5, 10, 15, 20], 900, p=[.55,.12,.18,.10,.05])
price_map = products.set_index('product_id').unit_price
revenue = [price_map.loc[p] * q * (1-d/100) for p,q,d in zip(product_ids, quantities, discounts)]
orders = pd.DataFrame({
    'order_id': range(1, 901),
    'customer_id': RNG.integers(1, 221, 900),
    'product_id': product_ids,
    'order_date': order_dates,
    'quantity': quantities,
    'discount_pct': discounts,
    'revenue': np.round(revenue, 2),
})

customers.to_csv(OUT/'customers.csv', index=False, date_format='%Y-%m-%d')
products.to_csv(OUT/'products.csv', index=False)
orders.sort_values('order_date').to_csv(OUT/'orders.csv', index=False, date_format='%Y-%m-%d')
print('Generated customers.csv, products.csv, and orders.csv')
