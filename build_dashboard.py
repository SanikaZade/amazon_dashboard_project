"""
Amazon Sales Dashboard — build script
Regenerates data/dashboard_data.json from data/amazon_clean_Data.csv
and injects it into dashboard.html (Plotly.js, fully data-driven, no images).

Run:  python build_dashboard.py
Then open dashboard.html in any browser.
"""
import json
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent
CSV_PATH = ROOT / "data" / "amazon_clean_Data.csv"
JSON_PATH = ROOT / "data" / "dashboard_data.json"
TEMPLATE_PATH = ROOT / "dashboard_template.html"
OUTPUT_PATH = ROOT / "dashboard.html"


def build_aggregates(df: pd.DataFrame) -> dict:
    df["Date"] = pd.to_datetime(df["Date"])
    out = {}

    valid = df[df["Amount_Zero_Flag"] == False]
    out["kpis"] = {
        "total_orders": int(len(df)),
        "total_revenue": float(valid["Amount"].sum()),
        "avg_order_value": float(valid["Amount"].mean()),
        "total_qty": int(df["Qty"].sum()),
        "cancel_rate": float((df["Status_Group"] == "Cancelled").mean() * 100),
        "return_rate": float((df["Status_Group"] == "Returned").mean() * 100),
        "b2b_pct": float((df["B2B"] == True).mean() * 100),
        "states": int(df["Ship_State"].nunique()),
        "cities": int(df["Ship_City"].nunique()),
        "categories": int(df["Category"].nunique()),
    }

    daily = (
        df.groupby(df["Date"].dt.date)
        .agg(orders=("Order_ID", "count"), revenue=("Amount", "sum"))
        .reset_index()
    )
    daily["Date"] = daily["Date"].astype(str)
    out["daily_trend"] = daily.to_dict("records")

    monthly = (
        df.groupby(["Order_Month", "Order_MonthNum"])
        .agg(orders=("Order_ID", "count"), revenue=("Amount", "sum"))
        .reset_index()
        .sort_values("Order_MonthNum")
    )
    out["monthly"] = monthly.to_dict("records")

    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow = (
        df.groupby("Order_DayOfWeek")
        .agg(orders=("Order_ID", "count"), revenue=("Amount", "sum"))
        .reindex(dow_order)
        .reset_index()
    )
    out["dow"] = dow.to_dict("records")

    heat = df.groupby(["Order_Week", "Order_DayOfWeek"]).size().reset_index(name="count")
    out["weekly_heatmap"] = heat.to_dict("records")

    cat = (
        df.groupby("Category")
        .agg(orders=("Order_ID", "count"), revenue=("Amount", "sum"), qty=("Qty", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    out["category"] = cat.to_dict("records")

    size = df.groupby("Size").size().reset_index(name="count").sort_values("count", ascending=False)
    out["size_dist"] = size.to_dict("records")

    catsize = df.groupby(["Category", "Size"]).size().reset_index(name="count")
    out["category_size"] = catsize.to_dict("records")

    fulfil = df.groupby("Fulfilment").size().reset_index(name="count")
    out["fulfilment"] = fulfil.to_dict("records")

    cancel_fulfil = (
        df.groupby("Fulfilment")
        .apply(lambda x: (x["Status_Group"] == "Cancelled").mean() * 100, include_groups=False)
        .reset_index(name="cancel_rate")
    )
    out["cancel_by_fulfilment"] = cancel_fulfil.to_dict("records")

    status_fulfil = df.groupby(["Fulfilment", "Status_Group"]).size().reset_index(name="count")
    out["status_by_fulfilment"] = status_fulfil.to_dict("records")

    ship_level = df.groupby("Shipping_Level").size().reset_index(name="count")
    out["shipping_level"] = ship_level.to_dict("records")

    ret_cat = (
        df.groupby("Category")
        .apply(lambda x: (x["Status_Group"] == "Returned").mean() * 100, include_groups=False)
        .reset_index(name="return_rate")
    )
    out["return_rate_category"] = ret_cat.to_dict("records")

    state = (
        df.groupby("Ship_State")
        .agg(orders=("Order_ID", "count"), revenue=("Amount", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    out["state"] = state.head(20).to_dict("records")

    city = (
        df.groupby("Ship_City")
        .agg(orders=("Order_ID", "count"), revenue=("Amount", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    out["city"] = city.head(15).to_dict("records")

    top_states_list = state.head(15)["Ship_State"].tolist()
    cancel_state = (
        df[df["Ship_State"].isin(top_states_list)]
        .groupby("Ship_State")
        .apply(lambda x: (x["Status_Group"] == "Cancelled").mean() * 100, include_groups=False)
        .reset_index(name="cancel_rate")
    )
    out["cancel_by_state"] = cancel_state.to_dict("records")

    b2b = df.groupby("B2B").size().reset_index(name="count")
    b2b["B2B"] = b2b["B2B"].astype(str)
    out["b2b"] = b2b.to_dict("records")

    amt = valid["Amount"]
    counts, edges = np.histogram(amt, bins=30)
    out["order_value_hist"] = [
        {"bin_start": float(edges[i]), "bin_end": float(edges[i + 1]), "count": int(counts[i])}
        for i in range(len(counts))
    ]

    seg = df.groupby("Order_Value_Segment").size().reset_index(name="count")
    out["order_value_segment"] = seg.to_dict("records")

    avg_cat = (
        df.groupby("Category")["Amount"]
        .mean()
        .reset_index(name="avg_amount")
        .sort_values("avg_amount", ascending=False)
    )
    out["avg_order_val_category"] = avg_cat.to_dict("records")

    combo = (
        df.groupby(["Category", "Size"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(15)
    )
    combo["combo"] = combo["Category"] + " - " + combo["Size"]
    out["top_combos"] = combo[["combo", "count"]].to_dict("records")

    status_all = df.groupby("Status_Group").size().reset_index(name="count")
    out["status_all"] = status_all.to_dict("records")

    top12_states = state.head(12)["Ship_State"].tolist()
    b2b_state = (
        df[df["Ship_State"].isin(top12_states)]
        .groupby("Ship_State")
        .apply(lambda x: (x["B2B"] == True).mean() * 100, include_groups=False)
        .reset_index(name="b2b_pct")
    )
    b2b_state["_order"] = b2b_state["Ship_State"].apply(lambda s: top12_states.index(s))
    b2b_state = b2b_state.sort_values("_order").drop(columns="_order")
    out["b2b_by_state"] = b2b_state.to_dict("records")

    # Add dynamic filtering data structure: compressed column list
    cats = sorted(df["Category"].dropna().unique().tolist())
    states = sorted(df["Ship_State"].dropna().unique().tolist())
    cities = sorted(df["Ship_City"].dropna().unique().tolist())
    sizes = sorted(df["Size"].dropna().unique().tolist())
    fulfils = sorted(df["Fulfilment"].dropna().unique().tolist())
    statuses = sorted(df["Status_Group"].dropna().unique().tolist())
    couriers = sorted(df["Courier_Status"].dropna().unique().tolist())
    channels = sorted(df["Sales_Channel"].dropna().unique().tolist())
    
    # Dates: offset from minimum date in days
    min_date = df["Date"].min()
    df["date_offset"] = (df["Date"] - min_date).dt.days
    min_date_str = str(min_date.date())

    cat_map = {v: i for i, v in enumerate(cats)}
    state_map = {v: i for i, v in enumerate(states)}
    city_map = {v: i for i, v in enumerate(cities)}
    size_map = {v: i for i, v in enumerate(sizes)}
    fulfil_map = {v: i for i, v in enumerate(fulfils)}
    status_map = {v: i for i, v in enumerate(statuses)}
    courier_map = {v: i for i, v in enumerate(couriers)}
    channel_map = {v: i for i, v in enumerate(channels)}

    out["meta"] = {
        "min_date": min_date_str,
        "cats": cats,
        "states": states,
        "cities": cities,
        "sizes": sizes,
        "fulfils": fulfils,
        "statuses": statuses,
        "couriers": couriers,
        "channels": channels
    }

    # Compress the dataframe into a row-oriented flat array of lists
    out["transactions"] = {
        "date": df["date_offset"].tolist(),
        "cat": [cat_map[v] for v in df["Category"]],
        "state": [state_map.get(v, -1) for v in df["Ship_State"]],
        "city": [city_map.get(v, -1) for v in df["Ship_City"]],
        "fulfil": [fulfil_map[v] for v in df["Fulfilment"]],
        "status": [status_map[v] for v in df["Status_Group"]],
        "courier": [courier_map.get(v, -1) for v in df["Courier_Status"]],
        "channel": [channel_map.get(v, -1) for v in df["Sales_Channel"]],
        "b2b": [1 if v else 0 for v in df["B2B"]],
        "size": [size_map[v] for v in df["Size"]],
        "qty": df["Qty"].tolist(),
        "amount": df["Amount"].fillna(0).tolist(),
        "amount_zero": [1 if v else 0 for v in df["Amount_Zero_Flag"]]
    }

    return out


def main():
    df = pd.read_csv(CSV_PATH)
    aggregates = build_aggregates(df)
    JSON_PATH.write_text(json.dumps(aggregates, default=str), encoding="utf-8")
    print(f"Aggregated data written to {JSON_PATH} ({JSON_PATH.stat().st_size} bytes)")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = template.replace("__DATA_JSON__", json.dumps(aggregates, default=str))
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Dashboard rebuilt at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
