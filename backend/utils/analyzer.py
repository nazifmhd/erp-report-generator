import pandas as pd

def analyze_data(df: pd.DataFrame):
    if df.empty:
        return {
            "latest_month": None,
            "previous_month": None,
            "total_current": 0,
            "total_previous": 0,
            "change_percent": 0,
            "top_product": None,
            "low_inventory": []
        }

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Drop rows with invalid dates
    df['Month'] = df['Date'].dt.to_period('M')

    latest_month = df['Month'].max()
    previous_month = latest_month - 1

    current_data = df[df['Month'] == latest_month]
    previous_data = df[df['Month'] == previous_month]

    total_current = current_data['Revenue'].sum()
    total_previous = previous_data['Revenue'].sum()

    change_percent = ((total_current - total_previous) / total_previous * 100) if total_previous > 0 else 0

    top_product = (
        current_data.groupby("Product Name")["Revenue"].sum().idxmax()
        if not current_data.empty else None
    )

    low_inventory = df[df["Inventory Level"] < 10]["Product Name"].unique().tolist()

    return {
        "latest_month": str(latest_month),
        "previous_month": str(previous_month),
        "total_current": total_current,
        "total_previous": total_previous,
        "change_percent": round(change_percent, 2),
        "top_product": top_product,
        "low_inventory": low_inventory
    }
