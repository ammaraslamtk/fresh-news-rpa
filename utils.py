import re
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


def get_date_range(months: int) -> tuple:
    """
    Get date range between the last day of current month
    and the first day of X months ago

    Args:
        months: The number of months to look back

    Raises:
        Exception: Invalid month in case of a negative value

    Returns:
        Date range tuple in a string DD/MM/YYYY format
    """
    if months == 0:
        months = 1
    if months < 0:
        raise Exception("Invalid month requested")
    today = date.today()
    start_date = (today - relativedelta(months=months - 1)).replace(day=1)
    end_date = date.today().replace(day=1, month=today.month + 1) - timedelta(days=1)
    start_date = date.strftime(start_date, "%m/%d/%Y")
    end_date = date.strftime(end_date, "%m/%d/%Y")
    return start_date, end_date


def search_currency(string: str) -> bool:
    """
    Search for any currency occurance in string
    using regex

    Args:
        string: String to search

    Returns:
        Matches or None
    """
    exp = r"(\$[0-9][0-9,]*(.[0-9]+)?)|([0-9][0-9,]*(.[0-9]+)?( dollars| USD))"
    return re.search(exp, string)
