def latest_financial_index(data: dict) -> int:
    """
    Determine the index of the latest standalone financial entry in the data.
    """
    if data is None or not isinstance(data, dict):
        raise ValueError("Invalid data: expected a dictionary.")

    financials = data.get("financials")
    if financials is None:
        raise ValueError("Invalid data: 'financials' key is missing or None.")
    
    for index, financial in enumerate(financials):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


def profit_margin(data: dict, financial_index: int) -> float:
    """
    Calculate the profit margin for the financial data at the given index.
    
    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The profit margin value from the financial data.
    """
    financial_entry = data.get("financials")[financial_index]
    pnl = financial_entry.get("pnl", {})
    
    net_income = pnl.get("netIncome", 0.0)
    total_revenue = pnl.get("lineItems", {}).get("netRevenue", 0.0)
    
    if total_revenue == 0:
        return 0.0  # Avoid division by zero
    
    return net_income / total_revenue


def total_revenue(data: dict, financial_index: int) -> float:
    """
    Calculate the total revenue from the financial data at the given index.

    This function accesses the "financials" list in the data dictionary at the specified index.
    It then retrieves the net revenue from the "pnl" (Profit and Loss) section under "lineItems".

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data.
    """
    financial_entry = data.get("financials")[financial_index]
    pnl = financial_entry.get("pnl", {})
    revenue = pnl.get("lineItems", {}).get("netRevenue", 0.0)
    return revenue


def total_borrowing(data: dict, financial_index: int) -> float:
    """
    Calculate the ratio of total borrowings to total revenue for the financial data at the given index.

    This function sums the long-term and short-term borrowings from the balance sheet ("bs")
    section of the financial data. It then divides this sum by the total revenue, calculated
    by calling the `total_revenue` function.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The ratio of total borrowings to total revenue.
    """
    financial_entry = data.get("financials")[financial_index]
    balance_sheet = financial_entry.get("bs", {})
    
    long_term_borrowing = balance_sheet.get("longTermBorrowings", 0.0)
    short_term_borrowing = balance_sheet.get("shortTermBorrowings", 0.0)
    
    total_borrowings = long_term_borrowing + short_term_borrowing
    revenue = total_revenue(data, financial_index)
    
    # Avoid division by zero
    if revenue == 0:
        return 0.0
    
    return total_borrowings / revenue


def iscr(data: dict, financial_index: int) -> float:
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.

    ISCR is a ratio that measures how well a company can cover its interest payments on outstanding debt.
    It is calculated as the sum of profit before interest and tax, and depreciation, increased by 1,
    divided by the sum of interest expenses increased by 1. The addition of 1 is to avoid division by zero.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value.
    """
    financial_entry = data.get("financials")[financial_index]
    pnl = financial_entry.get("pnl", {})
    
    profit_before_interest_and_tax = pnl.get("profitBeforeInterestAndTax", 0.0)
    depreciation = pnl.get("depreciation", 0.0)
    interest_expenses = pnl.get("interestExpenses", 0.0)

    numerator = profit_before_interest_and_tax + depreciation + 1
    denominator = interest_expenses + 1
    
    return numerator / denominator


def iscr_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    This function calculates the ISCR value by calling the `iscr` function and then assigns a flag color
    based on the ISCR value. If the ISCR value is greater than or equal to 2, it assigns a GREEN flag,
    otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the ISCR value.
    """
    is_ratio = iscr(data, financial_index)
    return FLAGS.GREEN if is_ratio >= 2 else FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.

    This function calculates the total revenue by calling the `total_revenue` function and then assigns
    a flag color based on the revenue amount. If the total revenue is greater than or equal to 50 million,
    it assigns a GREEN flag, otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the revenue calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the total revenue.
    """
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED


def borrowing_to_revenue_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    This function calculates the ratio of total borrowings to total revenue by calling the `total_borrowing`
    function and then assigns a flag color based on the calculated ratio. If the ratio is less than or equal
    to 0.25, it assigns a GREEN flag, otherwise, it assigns an AMBER flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
    ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER
