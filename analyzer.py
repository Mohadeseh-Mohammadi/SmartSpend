from datetime import datetime
from storage import load_expenses
import re

# category kyewords for auto-detection
CATEGORY_KEYWORDS = {
    "Food": ["lunch", "dinner", "pizza", "restaurant", "coffee", "food", "meal", "breakfast", "snack", "cake"],
    "Transport": ["taxi", "bus", "metro", "fuel", "gas", "parking", "train", "subway", "car"],
    "Shopping": ["shirt", "shoes", "clothes", "phone", "gift", "bag", "watch", "store", "shop"],
    "Entertainment": ["cinema", "movie", "game", "concert", "party", "music", "film"],
    "Bills": ["electricity", "water", "gas bill", "internet", "phone bill", "rent"]
}

# group expenses by category 
def group_by_category(expenses):
    data = expenses
    categories= {}
    for item in data:
        category = item["category"].strip()
        if category not in categories:
            categories[category]= 0
        else:
            pass
        
        categories[category] += item["amount"]

    total = sum(categories.values())
    return categories , total

# get today's expevses
def get_today_expenses():
    expenses=load_expenses()
    today_expenses= []
    today = datetime.now().date()

    for item in expenses:
        date_str = item["date"].strip()
        expense_date = datetime.strptime(date_str.strip(),"%Y-%m-%d %H:%M:%S").date()
        if (expense_date == today):
            today_expenses.append(item)
    return today_expenses

# monthly report grouped by category
def get_monthly_report():
    expenses=load_expenses()
    monthly_expenses = []
    month = datetime.now().month
    year = datetime.now().year

    for item in expenses:
        date_str = item["date"].strip()
        expense_date = datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S").date()
        if (expense_date.year == year and expense_date.month == month):
            monthly_expenses.append(item)
    return group_by_category(monthly_expenses)
    
# calculate monthly statistics
def get_statistics():
    expenses=load_expenses()
    monthly_expenses = []
    now = datetime.now()

    #filter current month date
    for item in expenses:
        date_str = item["date"].strip()
        expense_date = datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S").date()
        if (expense_date.year == now.year and expense_date.month == now.month):
            monthly_expenses.append(item)
   
    if not monthly_expenses:
        return None
    # total spending
    total = sum(item["amount"] for item in monthly_expenses)
    # daily average based on current day of month
    days_passed = now.day
    daily_avg = total/ days_passed

    # count days with at least on expense
    unique_day =set()
    for item in monthly_expenses:
        date_str = item["date"].strip()
        expense_date = datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S").date()
        unique_day.add(expense_date)
    days_with_expense = len(unique_day)

    # find top category
    categories , _ =group_by_category(monthly_expenses)
    top_category = max(categories , key=categories.get)
    top_amount= categories[top_category]


    # calculate daily totals for min/max  day detection
    daily_totals ={}
    for item in monthly_expenses:
        date_str = item["date"].strip()
        expense_date = datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S").date()
        date_only =expense_date

        if date_only not in daily_totals:
            daily_totals[date_only] = 0
        
        daily_totals[date_only] += item["amount"]

    # find most & least expensive day
    max_day = max(daily_totals , key=daily_totals.get)
    max_amount = daily_totals[max_day]
    min_day = min(daily_totals , key=daily_totals.get)
    min_amount =daily_totals[min_day]

    return{
        "total" : total,
        "daily_avg": daily_avg,
        "days_with_expense" : days_with_expense,
        "top_category" : top_category,
        "top_amount" : top_amount,
        "max_day":max_day,
        "max_amount":max_amount,
        "min_day": min_day,
        "min_amount":min_amount,
    }

# predict monthly spending
def predict_monthly(budget=None):
    stats = get_statistics()
    if not stats:
        return None
    now = datetime.now()
    daily_avg = stats["daily_avg"]

     # calculate remaining days in month
    if now.month ==12 :
        next_month = datetime(now.year+1,1,1)
    else:
        next_month = datetime(now.year,now.month+1,1)
    days_left = (next_month - datetime(now.year,now.month,now.day)).days
    total_days = days_left + now.day

    # predict total spending
    predicted = daily_avg * total_days

    result = {
        "predicted":predicted,
        "days_left":days_left,
        "daily_avg":daily_avg,
        "total_days":total_days,
    }

    # budget comparison 
    if budget is not None:
        diff = predicted - budget
        result["diff"] = diff
        if diff > 0:
            result["status"] = "over"
            result["message"] = f"⚠️ You will be over budget by {diff:,.0f} Toman!"
        else:
            result["status"] = "under"
            result["message"] = f"✅ You will be under budget by {abs(diff):,.0f} Toman!"
    
    return result

# detect category from description
def detect_category(description):
    if not description:
        return None
    description = description.lower()
    words = re.findall(r"\b\w+\b" , description)
    for category,keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:

            if keyword in words:
                return category
            
    return None

# learn new words for category improvement
def learn_new_category(description, category):
    if not description or not category:
        return
    
    description = description.lower()
    words = description.split()
    
    for word in words:
        if len(word) > 3 and word not in CATEGORY_KEYWORDS.get(category, []):
            if category not in CATEGORY_KEYWORDS:
                CATEGORY_KEYWORDS[category] = []
            CATEGORY_KEYWORDS[category].append(word)

# detect unusual spending behavior
def check_unusual_spending():
    total_list = get_today_expenses()
    if not total_list:
        return{"status" : "no_data",
               "message" : "You have no expenses today!"}
    today_total = sum(item["amount"] for item in total_list)
    stats = get_statistics()
    if stats is None:
        return{"status" : "no_data",
               "message" : "Not enough data for comparison!"}
    avg = stats["daily_avg"]
    # detect anomal
    if today_total > avg*2 :
        percent = (today_total / avg)*100
        excess = today_total - avg
        return{"status":"alert",
                "message":  "UNUSUAL SPENDING ALERT\n"
                            f"Today : {today_total:,} Toman\n"
                            f"Daily average : {avg:,.0f} toman\n"
                            f"This is {percent:,.0f}% above average!\n"
                            f"You spend { excess:,.0f} Toman more than usual."}
    else:
        return{"status":"normal",
               "message":   f"Everything is normal!\n"
                            f"Today : {today_total:,} Toman\n"
                            f"Daily average : {avg:,.0f} Toman"}