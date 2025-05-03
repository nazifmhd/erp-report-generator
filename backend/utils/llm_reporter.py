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

Make the report professional and concise.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a business analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content
