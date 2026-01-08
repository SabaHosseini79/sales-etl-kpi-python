# src/export.py
from __future__ import annotations

from pathlib import Path
import pandas as pd


def export_outputs(df_clean, kpis, kpi_tables, chart_paths, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Cleaned data
    cleaned_path = out_dir / "cleaned_data.xlsx"
    df_clean.to_excel(cleaned_path, index=False)

    # 2) KPI summary + tables
    summary_path = out_dir / "kpi_summary.xlsx"
    with pd.ExcelWriter(summary_path, engine="openpyxl") as writer:
        pd.DataFrame([kpis]).to_excel(writer, sheet_name="kpis", index=False)

        for name, table in kpi_tables.items():
            sheet = name[:31]  # محدودیت اسم شیت در Excel
            table.to_excel(writer, sheet_name=sheet, index=False)

    # 3) Note file
    note = out_dir / "OUTPUTS_README.txt"
    note.write_text(
        "Generated outputs:\n"
        f"- {cleaned_path.name}\n"
        f"- {summary_path.name}\n"
        + "".join([f"- {Path(p).name}\n" for p in chart_paths])
    )
