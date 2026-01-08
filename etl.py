# src/etl.py
import pandas as pd


def load_data(path):
    path = str(path)

    # اول utf-8
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        pass

    # اگر نشد: cp1252 (خیلی وقت‌ها برای فایل‌های ویندوز جواب می‌دهد)
    try:
        return pd.read_csv(path, encoding="cp1252")
    except UnicodeDecodeError:
        pass

    # اگر باز هم نشد: latin1 (تقریباً همیشه باز می‌کند)
    return pd.read_csv(path, encoding="latin1")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # استانداردسازی نام ستون‌ها
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # مپ کردن ستون‌های رایج دیتاست sales_data_sample
    rename_map = {}

    if "ordernumber" in df.columns and "order_id" not in df.columns:
        rename_map["ordernumber"] = "order_id"

    if "sales" in df.columns and "revenue" not in df.columns:
        rename_map["sales"] = "revenue"

    if "orderdate" in df.columns and "date" not in df.columns:
        rename_map["orderdate"] = "date"

    if "productline" in df.columns and "product" not in df.columns:
        rename_map["productline"] = "product"

    if "territory" in df.columns and "region" not in df.columns:
        rename_map["territory"] = "region"
    elif "country" in df.columns and "region" not in df.columns:
        rename_map["country"] = "region"

    if rename_map:
        df = df.rename(columns=rename_map)

    # تاریخ
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # حذف ردیف‌های خالی و تکراری
    df = df.dropna(how="all")
    df = df.drop_duplicates()

    # عددی‌سازی ستون‌های رایج
    for col in ["qty", "quantity", "price", "revenue", "amount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # اگر revenue نبود و qty/price داشتیم
    if "revenue" not in df.columns and "qty" in df.columns and "price" in df.columns:
        df["revenue"] = df["qty"] * df["price"]

    return df
