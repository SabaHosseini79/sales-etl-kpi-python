# src/main.py
from pathlib import Path

from .etl import load_data, clean_data
from .kpi import compute_kpis
from .viz import build_charts
from .export import export_outputs

RAW_PATH = Path("data/raw/sales_data_sample.csv")
OUT_DIR = Path("outputs")


def run():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"فایل ورودی پیدا نشد: {RAW_PATH.resolve()}")

    df = load_data(RAW_PATH)
    df_clean = clean_data(df)

    kpis, kpi_tables = compute_kpis(df_clean)
    chart_paths = build_charts(df_clean, OUT_DIR)

    export_outputs(
        df_clean=df_clean,
        kpis=kpis,
        kpi_tables=kpi_tables,
        chart_paths=chart_paths,
        out_dir=OUT_DIR,
    )

    print("Done. Outputs saved to:", OUT_DIR.resolve())


if __name__ == "__main__":
    run()
