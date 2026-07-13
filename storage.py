import json
import os
from datetime import datetime

# file path for storing expenses
DATA_FILE = "expenses.json"

# load all expenses from JSON file
def load_expenses():
    # if file does not exist, return empty list
    if not os.path.exists(DATA_FILE):
       return []
    # read & parse JSON data
    with open( DATA_FILE , "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# save a new expense to file
def save_expense(amount,category,description):
    expenses = load_expenses()
    # creat a new expense record
    new_expense = {
        "id":len(expenses)+1,
        "amount" : amount,
        "category":category,
        "description":description,
        "date":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    # append & save back to JSON file
    expenses.append(new_expense)

    with open(DATA_FILE , "w" ,encoding="utf-8") as f:
        json.dump(expenses,f,ensure_ascii=False,indent=2)
    return new_expense