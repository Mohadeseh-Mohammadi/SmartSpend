from storage import save_expense
import analyzer



def main():
    while True:
        # main menu
        headline =  "SmartSpend"
        print("\n\n"+headline.center(75))        
        print("\n\n\t1. Add new expense")
        print("\t2. Show today's expenses")
        print("\t3. Monthly report")     
        print("\t4. Statistics & Averages ")
        print("\t5. Monthly prediction")
        print("\t6. Unusual spending alert")
        print("\t7. Exit")
        print("\u2550"*75)
        
        choice = input("\tYour choice (1-7): ")
        
        if choice == "1":

            # Add new expense
            print("\nAdd new expense:")
            try:
                amount = int(input("Amount (Toman): "))
                description = input("description: ")
                
                if not description.strip():
                    description = "No description"
                
                # auto category description
                detected = analyzer.detect_category(description)
                if detected:
                    print(f"Auto-detected category: {detected}")
                    category = detected
                else:
                    category = input("Category (e.g. Food, Transport, ...): ")
                    
                    analyzer.learn_new_category(description, category)
                
                save_expense(amount, category, description)
                print("✅ Expense added successfully!")
            except ValueError:
                print("❌ Error: Amount must be a number!")
        
        
        elif choice == "2":
            # show today's expenses
            today_list = analyzer.get_today_expenses()
            if not today_list:
                print("\nYou have no expenses today!")
            else:
                total = sum(item["amount"] for item in today_list)
                print(f"\nToday's expenses ({len(today_list)} items):")
                print("\u2500"*50)
                for item in today_list:
                    print(f"{item['category']}: {item['amount']:,} Toman - {item.get('description')}")
                print("\u2500"*50)
                print(f"Total: {total:,} Toman")
        
        elif choice == "3":
            # monthly report 
            categories,total= analyzer.get_monthly_report()
            if not categories:
                print("NO expense this month!")
            else:
                print("\n Monthly Report:")
                print("\u2500"*50)
                for category ,amount in categories.items():
                    print(f"{category} : {amount : ,} Toman")
                print("\u2500"*50)
                print(f"total : {total:,}")


        elif choice == "4":
            # statistics & analytics
            stats = analyzer.get_statistics()
            if stats is None:
                print("\nNo expenses this month!")
            else:
                print("\nStatistics & Averages")
                print("\u2500"*75)
                print(f"Total expenses: {stats['total']:,} Toman")
                print(f"Daily average: {stats['daily_avg']:,.0f} Toman")
                print(f"Days with expense: {stats['days_with_expense']}")
                print(f"Top category: {stats['top_category']} ({stats['top_amount']:,} Toman)")
                print(f"Most expensive day: {stats['max_day']} ({stats['max_amount']:,} Toman)")
                print(f"Cheapest day: {stats['min_day']} ({stats['min_amount']:,} Toman)")
        

        elif choice == "5":
            # monthly prediction
            budget = input("Enter your monthly budget (optional, press Enter to skip): ")
            if budget.strip():
                try:
                    budget = int(budget)
                except ValueError:
                    print("❌ Invalid budget! Skipping...")
                    budget = None
            else:
                budget = None
            
            prediction = analyzer.predict_monthly(budget)
            
            if prediction is None:
                print("\nNo data for prediction!")
            else:
                print("\nMonthly Prediction")
                print("\u2500"*75)
                print(f" Daily average: {prediction['daily_avg']:,.0f} Toman")
                print(f" Days remaining: {prediction['days_left']}")
                print(f" Projected total: {prediction['predicted']:,.0f} Toman")
                
                if budget is not None:
                    print(f"\n{prediction['message']}")

        elif choice == "6":
            # unusual spending alert
            result = analyzer.check_unusual_spending()
            print("\n" + result['message'])
            

        elif choice == "7":
            # Exit
            print("\n Goodbye! Good luck!")
            break
        
        else:
            print("\n❌ Invalid option! Please choose a number from 1 to 7.")

if __name__ == "__main__":
    main()