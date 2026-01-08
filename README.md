# Sales ETL + KPI Automation (Python)

Python ETL pipeline to clean sales data, compute KPIs, and export Excel reports + a monthly revenue chart.

This project:
- Loads sales data (CSV)
- Cleans & standardizes columns (ETL)
- Computes KPIs (Total Revenue, Orders, AOV, MoM growth)
- Exports Excel reports + a monthly revenue chart

## Run
```bash
pip install pandas openpyxl matplotlib
python -m src.main
