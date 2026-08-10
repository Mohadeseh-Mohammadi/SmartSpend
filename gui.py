import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QMessageBox,
    QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt
from analyzer import (
    get_today_expenses, get_monthly_report, get_statistics,
    predict_monthly, check_unusual_spending, detect_category,
    learn_new_category)
from storage import save_expense


STYLE = """
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Tahoma', sans-serif;
}
QLabel#title {
    font-size: 32px;
    font-weight: bold;
    color: #89b4fa;
    padding: 10px;
}
QLabel#subtitle {
    font-size: 18px;
    color: #a6adc8;
}
QLabel#content {
    font-size: 17px;
    color: #cdd6f4;
    padding: 5px;
}
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 500;
    margin: 5px;
    outline: none;
    border: none;
}
QPushButton:hover {
    background-color: #45475a;
    border-color: #89b4fa;
}
QPushButton#primary {
    background-color: #89b4fa;
    color: #1e1e2e;
    border: none;
}
QPushButton#danger {
    background-color: #f38ba8;
    color: #1e1e2e;
    border: none;
}
QPushButton#success {
    background-color: #a6e3a1;
    color: #1e1e2e;
    border: none;
}
QPushButton#back {
    background-color: #45475a;
    color: #cdd6f4;
    border: 2px solid #89b4fa;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
}
QPushButton#back:hover {
    background-color: #89b4fa;
    color: #1e1e2e;
}
QLineEdit, QTextEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 15px;
    min-height: 30px;
}
QLineEdit:focus, QTextEdit:focus {
    border-color: #89b4fa;
}
QFrame#line {
    background-color: #45475a;
    min-height: 2px;
    max-height: 2px;
    border: none;
}
"""

#  Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartSpend - v2.0")
        self.setGeometry(100, 100, 700, 700)
        self.setMinimumSize(600, 600)
        self.setStyleSheet(STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        #  Stacked Widget 
        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)

        #  Menu page
        self.menu_page = self.create_menu_page()
        self.stacked.addWidget(self.menu_page)

        #  others page
        self.add_expense_page = self.create_add_expense_page()
        self.stacked.addWidget(self.add_expense_page)

        self.info_page = QWidget()
        self.info_layout = QVBoxLayout()
        self.info_page.setLayout(self.info_layout)
        self.stacked.addWidget(self.info_page)

        central.setLayout(main_layout)

        self.current_page = "menu"

    #  Main Menu page
    def create_menu_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # titel
        title = QLabel(" SmartSpend")
        title.setObjectName("title")
        layout.addWidget(title, alignment=Qt.AlignCenter)
        # subtitle
        subtitle = QLabel("Smart Daily Expense Manager")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        line = QFrame()
        line.setObjectName("line")
        layout.addWidget(line)

        buttons = [
            (" Add New Expense", self.show_add_expense, None, "#89b4fa"),
            (" Today's Expenses", self.show_info, "Today's Expenses", "#74c7ec"),
            (" Monthly Report", self.show_info, "Monthly Report", "#a6e3a1"),
            (" Statistics & Averages", self.show_info, "Statistics & Averages", "#f9e2af"),
            (" Monthly Prediction", self.show_info, "Monthly Prediction", "#cba6f7"),
            (" Unusual Spending Alert", self.show_info, "Spending Alert", "#ecc8d2"),
        ]
        for text, func, title, color in buttons:
            btn = QPushButton(text)
            if title is None:
                btn.clicked.connect(func)
            else:
                btn.clicked.connect(lambda checked, t=title, f=func: f(t))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: #1e1e2e;
                    border: none;
                    border-radius: 10px;
                    padding: 14px;
                    font-size: 15px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    opacity: 0.85;
                }}
            """)
            layout.addWidget(btn)
        # Exit button
        exit_btn = QPushButton(" Exit")
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: #1e1e2e;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
                margin-top: 10px;
            }
            QPushButton:hover {
                opacity: 0.85;
            }
        """)
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)

        page.setLayout(layout)
        return page

    #  Add new expense page
    def create_add_expense_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        # back button
        back_btn = QPushButton("← Back to Menu")
        back_btn.setObjectName("back")
        back_btn.clicked.connect(self.show_menu)
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        # line
        line = QFrame()
        line.setObjectName("line")
        layout.addWidget(line)
        # title
        title = QLabel(" Add New Expense")
        title.setObjectName("title")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        #  Amount input field
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount (Toman)...")
        self.amount_input.setMinimumWidth(400)
        layout.addWidget(self.amount_input)
        #  Description input field
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Description...")
        self.desc_input.setMinimumWidth(400)
        layout.addWidget(self.desc_input)
        #  Category input field
        self.cat_input = QLineEdit()
        self.cat_input.setPlaceholderText("Category (or auto-detect)...")
        self.cat_input.setMinimumWidth(400)
        layout.addWidget(self.cat_input)
        #  Auto-Detect button
        detect_btn = QPushButton(" Auto-Detect Category")
        detect_btn.setObjectName("primary")
        detect_btn.clicked.connect(self.auto_detect)
        layout.addWidget(detect_btn)
        #  Action buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton(" Save Expense")
        save_btn.setObjectName("success")
        save_btn.clicked.connect(self.save_expense)
        btn_layout.addWidget(save_btn)

        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setObjectName("danger")
        cancel_btn.clicked.connect(self.show_menu)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        page.setLayout(layout)
        return page

    
    def show_menu(self):
        self.stacked.setCurrentIndex(0)

    def show_add_expense(self):
        self.stacked.setCurrentIndex(1)
    # show Information page
    def show_info(self, title_text):
        self.stacked.setCurrentIndex(2)
        
        for i in reversed(range(self.info_layout.count())):
            self.info_layout.itemAt(i).widget().setParent(None)

        # Back button
        back_btn = QPushButton("← Back to Menu")
        back_btn.setObjectName("back")
        back_btn.clicked.connect(self.show_menu)
        self.info_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        line = QFrame()
        line.setObjectName("line")
        self.info_layout.addWidget(line)
        # title
        title = QLabel(title_text)
        title.setObjectName("title")
        self.info_layout.addWidget(title, alignment=Qt.AlignCenter)
        
        if "Today" in title_text:
            expenses = get_today_expenses()
            text = "No expenses recorded today." if not expenses else "\n".join(
                [f"• {e['category']}: {e['amount']:,} Toman - {e.get('description', '')}" for e in expenses]
            ) + f"\n\n Total: {sum(e['amount'] for e in expenses):,} Toman"
        elif "Monthly" in title_text:
            categories, total = get_monthly_report()
            text = "No expenses recorded this month." if not categories else "\n".join(
                [f"• {cat}: {amt:,} Toman" for cat, amt in categories.items()]
            ) + f"\n\n Monthly Total: {total:,} Toman"
        elif "Statistics" in title_text:
            stats = get_statistics()
            text = "No data available." if not stats else (
                f" Total: {stats['total']:,} Toman\n"
                f" Daily Average: {stats['daily_avg']:,.0f} Toman\n"
                f" Days with expenses: {stats['days_with_expense']}\n"
                f" Top Category: {stats['top_category']} ({stats['top_amount']:,} Toman)\n"
                f"⬆ Most Expensive Day: {stats['max_day']} ({stats['max_amount']:,} Toman)\n"
                f"⬇ Cheapest Day: {stats['min_day']} ({stats['min_amount']:,} Toman)"
            )
        elif "Prediction" in title_text:
            result = predict_monthly()
            text = "Not enough data." if not result else (
                f" Daily Average: {result['daily_avg']:,.0f} Toman\n"
                f" Days Remaining: {result['days_left']}\n"
                f" Projected Total: {result['predicted']:,.0f} Toman"
            )
            if result and "message" in result:
                text += f"\n\n{result['message']}"
        else:  # Alert
            result = check_unusual_spending()
            text = result["message"]

        info_label = QLabel(text)
        info_label.setObjectName("content")
        info_label.setWordWrap(True)
        self.info_layout.addWidget(info_label)

        ok_btn = QPushButton("✅ OK")
        ok_btn.setObjectName("success")
        ok_btn.clicked.connect(self.show_menu)
        self.info_layout.addWidget(ok_btn, alignment=Qt.AlignCenter)

    def auto_detect(self):
        desc = self.desc_input.text().strip()
        if not desc:
            QMessageBox.warning(self, "Error", "Please enter a description!")
            return
        category = detect_category(desc)
        if category:
            self.cat_input.setText(category)
            QMessageBox.information(self, "Category Detected", f"Detected: {category}")
        else:
            QMessageBox.information(self, "Category Detection", "Not detected. Please enter manually.")

    def save_expense(self):
        try:
            amount = int(self.amount_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Error", "Amount must be a number!")
            return
        desc = self.desc_input.text().strip() or "No description"
        category = self.cat_input.text().strip()
        if not category:
            detected = detect_category(desc)
            if detected:
                category = detected
            else:
                QMessageBox.warning(self, "Error", "Please enter a category!")
                return
        learn_new_category(desc, category)
        save_expense(amount, category, desc)
        QMessageBox.information(self, "Success", "✅ Expense added!")
        self.show_menu()


#  Run 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())