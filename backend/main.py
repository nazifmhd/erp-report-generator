from fastapi import FastAPI, Query
from utils.analyzer import analyze_data
from utils.llm_reporter import generate_report
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional: Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate-report")
def generate_erp_report(region: str = Query(...), category: str = Query(...)):
    # Load the mock data
    df = pd.read_csv("data/mock_data.csv")

    # Filter data based on region and category
    filtered_data = df[(df['Region'] == region) & (df['Category'] == category)]

    # If no data after filtering, return a message
    if filtered_data.empty:
        return {
            "report": f"No data found for region '{region}' and category '{category}'.",
            "sales_data": {
                "labels": [],
                "data": []
            }
        }

    # Analyze the filtered data (assuming this function is working)
    insights = analyze_data(filtered_data)

    # Generate the report (assuming this function is working)
    report = generate_report(insights)

    # Prepare sales data for chart (group by Product Name and aggregate Units Sold and Revenue)
    sales_by_product = filtered_data.groupby("Product Name").agg(
        total_units_sold=("Units Sold", "sum"),
        total_revenue=("Revenue", "sum")
    ).sort_values(by="total_revenue", ascending=False)

    # Extract labels (product names) and data (revenue or units sold)
    labels = sales_by_product.index.tolist()
    data = sales_by_product["total_revenue"].tolist()  # You can change to "total_units_sold" if you want units instead of revenue

    return {
        "report": report,
        "sales_data": {
            "labels": labels,
            "data": data
        }
    }
