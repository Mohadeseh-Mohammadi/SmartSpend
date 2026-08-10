# SmartSpend

A smart expense management tool with both CLI and GUI interfaces.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0-orange?style=for-the-badge)
![GUI](https://img.shields.io/badge/GUI-PyQt5-brightgreen?style=for-the-badge)

## Features

- Add expenses with auto-category detection
- View today's expenses
- Monthly expense report by category
- Statistics and averages (total, daily average, top category)
- Predict monthly spending
- Unusual spending alerts
- JSON storage (no database needed)
- GUI version with PyQt5 (v2.0)

## Technologies

- Python 3.8+
- PyQt5 (GUI)
- JSON
- Datetime
- Regular Expressions

## Installation

```bash
git clone https://github.com/Mohadeseh-Mohammadi/SmartSpend.git
cd SmartSpend
python main.py
```

Screenshots

[Main Menu](screenshots/menu.png)
[Add Expense](screenshots/add_expense.png)
[Today's Expenses](screenshots/today.png)
[Monthly Report](screenshots/monthly_report.png)
[Statistics](screenshots/statistics.png)
[Monthly Prediction](screenshots/prediction.png)
[Unusual Spending Alert](screenshots/alert.png)
[GUI Showcase](screenshots/gui.gif)

Project Structure

```
SmartSpend/
├── main.py
├── gui.py
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
    ├── alert.png
    └── gui.gif
```

Roadmap

- [x] CLI version
- [x] GUI version with PyQt5
- [ ] ML-based category detection

License

This project is licensed under the MIT License.

Contact

GitHub:[Mohadeseh Mohammadi](https://github.com/Mohadeseh-Mohammadi)
