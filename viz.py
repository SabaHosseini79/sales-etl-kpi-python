# src/viz.py
from pathlib import Path
import matplotlib.pyplot as plt


def build_charts(df, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    chart_paths = []

    if "date" in df.columns and "revenue" in df.columns:
        tmp = df.dropna(subset=["date"]).copy()
        if not tmp.empty:
            tmp = tmp.set_index("date").sort_index()
            series = tmp.resample("MS")["revenue"].sum()

            x = series.index.astype(str).to_list()
            y = series.to_list()

            fig = plt.figure()
            plt.plot(x, y)
            plt.title("Monthly Revenue")
            plt.xlabel("Month")
            plt.ylabel("Revenue")
            plt.xticks(rotation=45)

            p = out_dir / "monthly_revenue.png"
            fig.savefig(p, bbox_inches="tight", dpi=200)
            plt.close(fig)

            chart_paths.append(p)

    return chart_paths
