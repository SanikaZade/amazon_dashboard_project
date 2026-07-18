# Amazon Sales Dashboard — Live Data Project

Interactive dashboard for Amazon India Q2 2022 sales data (128,017 orders,
Mar–Jun 2022). Every chart renders **directly from the dataset** using
Plotly.js — no static PNG images anywhere.

## Project Structure
```
amazon_dashboard_project/
├── dashboard.html            ← open this in any browser — the live dashboard
├── dashboard_template.html   ← HTML/JS template (Plotly charts + layout)
├── build_dashboard.py        ← regenerates data + rebuilds dashboard.html
├── requirements.txt
└── data/
    ├── amazon_clean_Data.csv     ← source dataset
    └── dashboard_data.json      ← aggregated data consumed by the dashboard
```

## How it works
1. `build_dashboard.py` reads `data/amazon_clean_Data.csv`, computes all
   aggregates (revenue trends, category breakdowns, geography, fulfilment,
   order-value distribution, etc.) with pandas/numpy.
2. It writes those aggregates to `data/dashboard_data.json`.
3. It injects that JSON into `dashboard_template.html` to produce the final
   `dashboard.html` — a single self-contained file you can open or share.

## Usage

### Just view it
Open `dashboard.html` in any browser. Done.

### Rebuild after updating the data
Replace `data/amazon_clean_Data.csv` with a new export (same column schema),
then:
```bash
pip install -r requirements.txt
python build_dashboard.py
```
This refreshes `dashboard.html` with numbers from the new file.

## Dashboard sections
- **Overview** — daily/monthly trend, day-of-week orders, week×day heatmap
- **Products** — revenue/orders by category, size distribution, category×size heatmap, top combos
- **Fulfillment & Status** — Amazon vs Merchant split, cancellation rate, status breakdown, return rate by category
- **Geography** — top states/cities by revenue, cancellation rate by state
- **Order Value & Segments** — value distribution, value segments, B2B vs B2C, avg order value by category

## Key figures (current dataset)
- Total revenue: ₹7.83 Cr | Avg order value: ₹623
- Cancellation rate: 14.1% | Return rate: 1.6%
- T-shirt + Shirt = ~78% of orders
- Merchant cancel rate (17.4%) is ~4.8pp higher than Amazon fulfilment (12.6%)
