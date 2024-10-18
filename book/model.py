# model.py

import json
from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, iscr, borrowing_to_revenue_flag
from rules import latest_financial_index, total_revenue, profit_margin

def analyze_financial_data(data):
    """
    Analyzes the financial data and returns results in JSON format.
    :param data: A dictionary containing financial data
    :return: A JSON string with the analysis results
    """
    results = {
        "latest_financial_index": latest_financial_index(data),
        "total_revenue": total_revenue(data),
        "profit_margin": profit_margin(data),
    }
    return json.dumps(results)
