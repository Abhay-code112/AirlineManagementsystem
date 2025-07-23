import re
from datetime import datetime
from tabulate import tabulate
import pandas as pd

def validate_date(date_str):
    """Validates a date string in DD/MM/YYYY format."""
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    """Validates a time string in HH:MM format."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def validate_phone(phone):
    """Validates a 10-digit phone number."""
    return re.fullmatch(r"\d{10}", phone) is not None

def display_table(data):
    """Displays a pandas DataFrame in a grid format."""
    if isinstance(data, pd.DataFrame) and not data.empty:
        print(tabulate(data, headers='keys', tablefmt='grid'))
    else:
        print("No records found.")