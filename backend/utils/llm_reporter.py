import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)

def generate_report(insights):
    prompt = f"""
Generate a short business report using the following data:
- Total revenue in {insights['latest_month']}: ${insights['total_current']}
- Revenue in {insights['previous_month']}: ${insights['total_previous']}
- Month-over-month change: {insights['change_percent']}%
- Top-selling product: {insights['top_product']}
- Low inventory products: {', '.join(insights['low_inventory']) or 'None'}

Make the report professional and concise. Include the following sections:
1. Summary of key findings
2. Revenue analysis
3. Product performance
4. Inventory status
5. Conclusion with actionable recommendations

The conclusion should summarize the overall business performance and provide 2-3 specific recommendations.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a business analyst who creates comprehensive reports with clear conclusions and actionable recommendations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=350  # Increased from 200 to ensure conclusion fits
    )

    return response.choices[0].message.content