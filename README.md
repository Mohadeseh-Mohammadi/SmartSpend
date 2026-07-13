# 🧠 SmartSpend

A smart command-line tool for managing and analyzing daily expenses.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=for-the-badge)

## Features

- Add expenses with auto-category detection
- View today's expenses
- Monthly expense report by category
- Statistics and averages (total, daily average, top category)
- Predict monthly spending
- Unusual spending alerts
- JSON storage (no database needed)

## Technologies

- Python 3.8+
- JSON
- Datetime
- Regular Expressions

## Installation

bash
git clone https://github.com/Mohadeseh-Mohammadi/SmartSpend.git
cd SmartSpend
python main.py

Screenshots

[Main Menu](screenshots/menu.png)
[Add Expense](screenshots/add_expense.png)
[Today's Expenses](screenshots/today.png)
[Monthly Report](screenshots/monthly_report.png)
[Statistics](screenshots/statistics.png)
[Monthly Prediction](screenshots/prediction.png)
[Unusual Spending Alert](screenshots/alert.png)

Project Structure

SmartSpend/
├── main.py
├── analyzer.py
├── storage.py
├── README.md
└── screenshots/
├── menu.png
├── add_expense.png
├── today.png
├── monthly_report.png
├── statistics.png
├── prediction.png
└── alert.png

Roadmap

· CLI version ✅
· GUI version with PyQt5
· ML-based category detection

License

This project is licensed under the MIT License.

Contact

GitHub: github.com/Mohadeseh-Mohammadi
