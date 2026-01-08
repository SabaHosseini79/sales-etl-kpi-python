# src/kpi.py
from __future__ import annotations

import pandas as pd


def compute_kpis(df: pd.DataFrame):
    df = df.copy()
    kpis: dict[str, float | int] = {}
    tables: dict[str, pd.DataFrame] = {}

    # KPI: Total Revenue
    if "revenue" in df.columns:
        kpis["total_revenue"] = float(df["revenue"].fillna(0).sum())

    # KPI: Orders / Rows
    if "order_id" in df.columns:
        kpis["total_orders"] = int(df["order_id"].nunique(dropna=True))
    else:
        kpis["total_rows"] = int(len(df))

    # KPI: AOV
    if "order_id" in df.columns and "revenue" in df.columns:
        order_rev = df.groupby("order_id", dropna=True)["revenue"].sum()
        kpis["aov"] = float(order_rev.mean()) if len(order_rev) else 0.0

    # Tables: Top Products
    if "product" in df.columns and "revenue" in df.columns:
        tables["top_products"] = (
            df.groupby("product", dropna=True)["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

    # Tables: Top Regions
    if "region" in df.columns and "revenue" in df.columns:
        tables["top_regions"] = (
            df.groupby("region", dropna=True)["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

    # Tables: Monthly Revenue + MoM Growth
    if "date" in df.columns and "revenue" in df.columns:
        tmp = df.dropna(subset=["date"]).set_index("date").sort_index()
        monthly = tmp.resample("MS")["revenue"].sum()

        mom_pct = monthly.pct_change() * 100

        tables["monthly_revenue"] = monthly.reset_index(name="monthly_revenue")
        tables["monthly_mom_growth_pct"] = mom_pct.reset_index(name="mom_growth_pct")

    return kpis, tables
