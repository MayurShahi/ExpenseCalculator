import json
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

DEFAULT_CATEGORIES = [
    "FOOD",
    "TRANSPORT",
    "ENTERTAINMENT",
    "UTILITIES",
    "SHOPPING",
    # Custom categories will be added here
]
expense_data={
    "ID":[],
    "DATE":[],
    "AMOUNT":[],
    "CATEGORY":[],
    "DESCRIPTION":[]
}
budget=[]
current_budget_month=[]
category_wise_total=[]
df=pd.DataFrame(expense_data)


def add_expenses():
    global expense_data, df, DEFAULT_CATEGORIES
    while True:
        try:
            expense_id = len(expense_data["ID"]) + 1 
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            amount = int(input("Enter Amount: "))
            
            # Category selection with custom option
            print("\n📋 Select Category:")
            for i, cat in enumerate(DEFAULT_CATEGORIES, 1):
                print(f"{i}. {cat}")
            print(f"{len(DEFAULT_CATEGORIES) + 1}. ✏️ Add Custom Category")
            print(f"{len(DEFAULT_CATEGORIES) + 2}. 🔍 Other (Manual Entry)")
            print(f"{len(DEFAULT_CATEGORIES)+3}. ❌ CANCEL")
            
            try:
                choice = int(input("Choose category (1-7): "))
                
                if 1 <= choice <= len(DEFAULT_CATEGORIES):
                    category = DEFAULT_CATEGORIES[choice - 1]
                    print(f"✅ Selected: {category}")
                    
                elif choice == len(DEFAULT_CATEGORIES) + 1:
                    # Custom category
                    custom_cat = input("Enter custom category name: ").strip().capitalize()
                    if custom_cat:
                        category = custom_cat
                        print(f"✅ Custom category '{category}' created!")
                        DEFAULT_CATEGORIES.append(category)  # Add to default list for future use
                    else:
                        print("❌ Invalid category name! Using 'OTHER'")
                        category = "OTHER"
                        
                elif choice == len(DEFAULT_CATEGORIES) + 2:
                    # Manual entry
                    category = input("Enter Category: ").strip().upper()
                    DEFAULT_CATEGORIES.append(category)  # Add to default list for future use
                    if not category:
                        category = "OTHER"
                        print("Using default: OTHER")
                        DEFAULT_CATEGORIES.append(category)
                elif choice== len(DEFAULT_CATEGORIES)+3:
                     return
                      
                else:
                    print("❌ Invalid choice! Using 'OTHER'")
                    category = "OTHER"
                    
            except ValueError:
                # If user enters non-number, fall back to manual entry
                print("⚠️ Invalid input! Please enter category manually.")
                category = input("Enter Category: ").strip().capitalize()
                if not category:
                    category = "OTHER"
            
            description = input("Add Description: ")
            
            # Add data to dictionary
            expense_data["ID"].append(expense_id)
            expense_data["DATE"].append(date)
            expense_data["AMOUNT"].append(amount)
            expense_data["CATEGORY"].append(category)
            expense_data["DESCRIPTION"].append(description)

            # Update the DataFrame
            df = pd.DataFrame(expense_data)
            check_budget_alert(category)
            print(f"\n✅ Expense #{expense_id} added successfully!")
            print(f"   Category: {category}")
            print(f"   Amount: ${amount}")
            print(f"   Date: {date}")
            break
            
        except ValueError:
            print("❌ Please enter a valid number for Amount!")
            continue
        except KeyError:
            print("❌ Invalid key in dictionary!")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
    
 ###################################################################################

def view_expense():
    global df
    while True:
        try:
            print("\n" + "="*50)
            print("1. View All Expenses")
            print("2. Filter by Date")
            print("3. Filter by Category")
            print("4. Sort Expenses")
            print("5. Back to Main Menu")
            print("="*50)
            choice=int(input("Which option do you choose? "))
            print("="*50)
            if choice==1:
                if df.empty:
                    print("No expenses recorded yet.")
                else:
                    print("\n" + "="*50)
                    print("📊 EXPENSES")
                    print("="*50)
                    print(df.to_string(index=False))   
            elif choice == 2:
                filter_by_date()  # Call date filter function
                
            elif choice == 3:
                filter_by_category()  # You can add this later
                
            elif choice == 4:
                sort_expenses()  # You can add this later
                
            elif choice == 5:
                break  # Return to main menu
                
            else:
                print("❌ Invalid choice! Please enter 1-5")
                
        except ValueError:
            print("❌ Please enter a valid number!")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

def filter_by_date():
    #Filter expenses by date
    global df 
    
    if df.empty:
        print("No expenses recorded")
        return

    try:
        print("\n" + "-"*40)
        print("📅 FILTER BY DATE")
        print("-"*40)
        print("""
                Choose filter type:
               1.Specific Date
               2.Date range
               3.Month/Year""")
        filter_choice=int(input("Enter your Choice: "))
         

        if filter_choice==1:
            try:

                #fliter by specific date
                date_input=input("Enter the date(DD-MM-YYYY): ").strip()

                # Parse the input date
                filter_date = datetime.strptime(date_input, "%d-%m-%Y")

                filter_date_str = filter_date.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD

                # Filter DataFrame (partial match since we have time in our data)
                filtered_df = df[df['DATE'].str.startswith(filter_date_str)]
                    
                if filtered_df.empty:
                    print(f"No expenses found for date: {date_input}")
                else:
                    print("\n" + "="*50)
                    print(f"📊 Expenses for {date_input}")
                    print("="*50)
                    print(filtered_df.to_string(index=False))
        
            except ValueError:
                print("❌ Please enter the date in correct format (DD-MM-YYYY)")
                return

        elif filter_choice==2:
            try:
                #filter by date range
                start_date_input=input("Enter the start date(DD-MM-YYYY): ").strip()
                end_date_input=input("Enter the end date(DD-MM-YYYY): ").strip()

                # Parse the input dates
                start_date = datetime.strptime(start_date_input, "%d-%m-%Y")
                end_date = datetime.strptime(end_date_input, "%d-%m-%Y")

                # Filter DataFrame
                filtered_df = df[(df['DATE'] >= start_date.strftime("%Y-%m-%d")) & (df['DATE'] <= end_date.strftime("%Y-%m-%d"))]
                    
                if filtered_df.empty:
                    print(f"No expenses found between {start_date_input} and {end_date_input}")
                else:
                    print("\n" + "="*50)
                    print(f"📊 Expenses from {start_date_input} to {end_date_input}")
                    print("="*50)
                    print(filtered_df.to_string(index=False))
            except ValueError:
                print("❌ Please enter the dates in correct format (DD-MM-YYYY)")
                return

        elif filter_choice==3:
            try:
                #filter by month/year
                month_year_input=input("Enter month and year (MM-YYYY): ").strip()

                # Parse the input month and year
                filter_month_year = datetime.strptime(month_year_input, "%m-%Y")
                filter_month_year_str = filter_month_year.strftime("%Y-%m")  # Convert to YYYY-MM

                # Filter DataFrame (partial match since we have day in our data)
                filtered_df = df[df['DATE'].str.startswith(filter_month_year_str)]
                    
                if filtered_df.empty:
                    print(f"No expenses found for month/year: {month_year_input}")
                else:
                    print("\n" + "="*50)
                    print(f"📊 Expenses for {month_year_input}")
                    print("="*50)
                    print(filtered_df.to_string(index=False))
            except ValueError:
                print("❌ Please enter the month and year in correct format (MM-YYYY)")
                return
        
    except ValueError:
        print("❌ Please enter correct option number (1-3) and date formats!")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

def filter_by_category():
    #Filter expenses by date
    global df,DEFAULT_CATEGORIES
    
    if df.empty:
        print("No expenses recorded")

    try:
        print("n"+"="*50)
        print(" Which category do you want to filter?")
        for i, cat in enumerate(DEFAULT_CATEGORIES,1):
            print(f"{i}. {cat}")
        print("="*50)
        category_choice=input("Enter your choice (IN WORDS): ").strip().upper()
        filtered_df = df[df['CATEGORY'].str.startswith(category_choice)]

        if filtered_df.empty:
            print(f"NO Expenses found for the category {category_choice}")
        else:
            print("\n"+"="*50)
            print(f"📊 Expenses for {category_choice}")
            print("="*50)
            print(filtered_df.to_string(index=False))
    except KeyError:
        print("The 'CATEGORY' column doesn't exist in the dataframe")


def sort_expenses():
    global df
    if df.empty:
        ("There are no datasets to sort. ")
    try:
        print("\n"+"="*50)
        print("""SORT OUT by according to following options:
              1.DATE
              2.Amount""")
        print("="*50)
        sort_option=int(input("Enter your option: "))

        if sort_option==1:
            sorted_df=df.sort_values(by="DATE")
            print("\n"+"="*50)
            print("📊 Expenses sorted by DATE")
            print("="*50)
            print(sorted_df.to_string(index=False))

        elif sort_option==2:
            sorted_df=df.sort_values(by="AMOUNT")
            print("\n"+"="*50)
            print("📊 Expenses sorted by AMOUNT")
            print("="*50)
            print(sorted_df.to_string(index=False))
    except ValueError:
        print("❌ Please enter a valid number (1 or 2)!")



#########################################################################################
        
def delete_expense():
    global df,expense_data
    if df.empty:
        print("No expenses recorded yet.")
        return
    try:
        print("\n"+"="*50)
        print("DELETE EXPENSE")
        print("="*50)
        expense_id=int(input("Enter the ID of the expense you want to delete: "))
        
        if expense_id in expense_data["ID"]:
            index_to_delete=expense_data["ID"].index(expense_id)#Finds out index of the expense to be deleted  
            final_decision=input("Do you really want to delete the dataset (y/n)? ").capitalize
            if final_decision=="Y" or final_decision=="Yes":
                for key in expense_data.keys():#iterates through each key in the dictionary and deletes the value at the index of the expense to be deleted
                    del expense_data[key][index_to_delete]
                df=pd.DataFrame(expense_data)#updates the dataframe after deleting the expense
                print(f"Expense with ID {expense_id} deleted successfully!")
            else:
                return
        else:
            print(f"No expense found with ID {expense_id}")
    except ValueError:
        print("❌ Please enter a valid number for ID!")
    except Exception as e:
        print(f"An error occurred: {e}")

#######################################################################################

def set_budget():
    global budget, current_budget_month
    # STEP 1: Initialize tracker if needed
    if 'current_budget_month' not in globals():
        current_budget_month = datetime.today().strftime("%Y-%m")
    
    # STEP 2: Check for month change
    this_month = datetime.today().strftime("%Y-%m")
    if this_month != current_budget_month:
        # STEP 3: Auto-reset!
        print("\n" + "="*50)
        print(f"📅 NEW MONTH: {this_month}")
        print("Previous budgets have been cleared for new month!")
        print("="*50)
        budget = []  # The actual reset
        current_budget_month = this_month  # Update tracker
    while True:
        try:
            print("\n"+"="*50)
            print("SET BUDGET")
            print("="*50)
            print("""For which category do you want to set budget
                1.FOOD
                2.TRANSPORT
                3.ENTERTAINMENT
                4.UTILITIES
                5.SHOPPING
                6.ADD CATEGORY
                7.DISPLAY BUDGET
                8.BACK TO MAIN MENU""")
            budget_category=int(input("Enter the category: "))
            if budget_category==1:
                bud=float(input("Enter your budget for Food: "))
                budget_entry={
                    "category":"Food",
                    "Budget":bud
                }
                print(f"Budget of {bud} for food this month successfulyy added")
                

            elif budget_category==2:
                bud=float(input("Enter your budget for Transport: "))
                budget_entry={
                    "category":"Transport",
                    "Budget":bud
                }
                print(f"Budget of {bud} for Transport this month added successfully")

            elif budget_category==3:
                bud=float(input("Enter your budget for Entertainment: "))
                budget_entry={
                    "category":"Entertainment",
                    "Budget":bud
                }
                print(f"BUdget of {bud} for Entertainment for this month added successfully ")

            elif budget_category==4:
                bud=float(input("Enter your budget for Utilities: "))
                budget_entry={
                    "category":"Utilities",
                    "Budget":bud
                }
                print(f"Budget of {bud} for Utilities for this month added successfully")
                

            elif budget_category==5:
                bud=float(input("Enter your budget for Shopping: "))
                budget_entry={
                    "category":"Shopping",
                    "Budget":bud
                }
                print(f"Budget of {bud} for shopping for this month added successfully")
                

            elif budget_category==6:
                cat=input("Enter the category you want to add: ")
                bud=float(input(f"Enter your budget for {cat}: "))
                budget_entry={
                    "category":f"{cat}",
                    "Budget":bud
                }
                print(f"Budget of {bud} for {cat} this month added successfully")
                

            elif budget_category==7:
                print("\n" + "="*50)
                print("📋 BUDGET")
                print("="*50)
                
                if not budget:
                     print("There is no calculation history yet")
                     return
                for i, entry in enumerate(budget, 1):
                    print(f"\n{i}. {entry['category']}: {entry['Budget']}")
                    

            elif budget_category==8:
                break

            budget.append(budget_entry)
            
        except ValueError:
            print("❌ Please enter a valid number for category and budget!")
        except IndexError:
            print("❌ Invalid category choice! Please choose a number between 1 and 7.")
        except Exception as e:
            print(f"An error occurred: {e}")

def check_budget_alert(category):
    global budget,df
    # 🔴 BUDGET CHECK 
    if 'budget' in globals() and budget:
        for b in budget:
            if b["category"].upper() == category.upper():
                cat_budget = b["Budget"]
                
                # Calculate total spent
                cat_expenses = df[df['CATEGORY'].str.upper() == category.upper()]
                total_spent = cat_expenses['AMOUNT'].sum()
                
                # Check if exceeded
                if total_spent > cat_budget:
                    print("\n" + "⚠️"*15)
                    print(f"⚠️ BUDGET EXCEEDED for {category}!")
                    print(f"Budget: ${cat_budget} | Spent: ${total_spent}")
                    print("⚠️"*15)
                
                # Check if approaching
                elif total_spent >= (cat_budget * 0.8):
                    remaining = cat_budget - total_spent
                    print(f"\n⚠️ {category} is at 80% of budget!")
                    print(f"Only ${remaining:.2f} left for this month")
                break 


            
#############################################################################################################



def show_statistics():
     global df, current_budget_month
     while True:
        try:
            print("\n"+"="*50)
            print("📊 STATISTICS")
            print("="*50)
            print("""Which insight do you want to analyze?
                1.Category-wise summary
                2.Total spent this month
                3.Daily Average spending
                4.Comparison with previous month
                5.Top 5 most expensive expenses
                6.Back to main menu""")
            stat_choice=int(input("Enter the option number of your choice:  "))

            if stat_choice==1:
                cat_summary()
            elif stat_choice==2:
                total_monthly()
            elif stat_choice==3:
                daily_avg()
            elif stat_choice==4:
                compare_monthly_chart()
            elif stat_choice==5:
                top_expense()
            elif stat_choice==6:
                return
            break
        except ValueError:
            print("Enter the current type of Input")
            continue
        except KeyError:
            print("Enter the correct option (1-6)")
            continue

def cat_summary():
    global df
    
    print("\n" + "="*50)
    print("📊 CATEGORY-WISE SUMMARY")
    print("="*50)
    
    if df.empty:
        print("No expenses recorded yet.")
        return
    
    # Group by category and sum amounts
    category_totals = df.groupby('CATEGORY')['AMOUNT'].sum().reset_index()
    category_totals.columns = ['CATEGORY', 'TOTAL']
    
    # Display results
    for i, row in category_totals.iterrows():
        print(f"{i+1}. {row['CATEGORY']}: ${row['TOTAL']:.2f}")
    
    # Show grand total
    grand_total = category_totals['TOTAL'].sum()
    print("-" * 40)
    print(f"GRAND TOTAL: ${grand_total:.2f}")
    print("="*50)
    show_category_pie_chart()  # Call the pie chart function after displaying summary

def show_category_pie_chart():
    global df
    
    if df.empty:
        print("No expenses to display in chart.")
        return
    
    # Group by category and sum amounts
    category_totals = df.groupby('CATEGORY')['AMOUNT'].sum()
    
    # Filter out categories with zero amount (optional)
    category_totals = category_totals[category_totals > 0]
    
    if category_totals.empty:
        print("No positive expenses to display.")
        return
    
    # Create the pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(category_totals.values, 
            labels=category_totals.index, 
            autopct='%1.1f%%',
            startangle=90,
            shadow=True)
    plt.title('Expenses by Category', fontsize=16)
    plt.axis('equal')  # Equal aspect ratio ensures pie is circular
    plt.show()

def total_monthly():
    global df, current_budget_month
    
    print("\n" + "="*50)
    print(f"📊 TOTAL SPENT IN {current_budget_month}")
    print("="*50)
    
    if df.empty:
        print("No expenses recorded yet.")
        return
    
    # Make a copy to avoid modifying original
    df_temp = df.copy()
    
    # Convert DATE column to datetime
    df_temp['DATE'] = pd.to_datetime(df_temp['DATE'])
    
    # Extract year-month from date
    df_temp['YEAR_MONTH'] = df_temp['DATE'].dt.strftime('%Y-%m')
    
    # Filter for current month
    current_month_expenses = df_temp[df_temp['YEAR_MONTH'] == current_budget_month]
    
    # Calculate total
    if current_month_expenses.empty:
        total_expense = 0
        print("No expenses found for this month.")
    else:
        total_expense = current_month_expenses['AMOUNT'].sum()
        print(f"💰 Total: ${total_expense:.2f}")
    
    print("="*50)
    """ 
    ALternative code where interation over row concept is used
        global df, current_budget_month
        
        print("\n" + "="*50)
        print(f"📊 TOTAL SPENT IN {current_budget_month}")
        print("="*50)
        
        if df.empty:
            print("No expenses recorded yet.")
            return
        
        # Initialize total
        total_expense = 0
        
        # Correct way to iterate through rows
        for index, row in df.iterrows():
            # Extract year-month from the date string (first 7 characters: YYYY-MM)
            expense_month = row['DATE'][:7]  # Gets first 7 chars: "2024-02" from "2024-02-17 14:30:25"
            
            if expense_month == current_budget_month:
                total_expense += row['AMOUNT']
        
        if total_expense == 0:
            print("No expenses found for this month.")
        else:
            print(f"💰 Total: ${total_expense:.2f}")
        
        print("="*50)
        """
        
def daily_avg():
    global df
    today= datetime.now()
    if df.empty:
        print("No expenses recorded yet.")
        return
    filtered_df = df[df['DATE'].str.startswith(today.strftime("%Y-%m-%d"))]
    if filtered_df.empty:
        print("No expenses recorded for today.")
        return  
    daily_average = filtered_df['AMOUNT'].mean()
    print("\n" + "="*50)    
    print(f"📊 DAILY AVERAGE SPENDING FOR {today.strftime('%Y-%m-%d')}: ${daily_average:.2f}")
    print("="*50)
    


    
def compare_monthly_chart():
    global df
    
    if df.empty:
        print("No expenses recorded yet.")
        return
    
    # Prepare data
    df_temp = df.copy()
    df_temp['DATE'] = pd.to_datetime(df_temp['DATE'])
    df_temp['YEAR_MONTH'] = df_temp['DATE'].dt.strftime('%Y-%m')
    
    # Get last 3 months for better trend
    months_with_data = sorted(df_temp['YEAR_MONTH'].unique(), reverse=True)[:3]
    
    if len(months_with_data) < 2:
        print("Need at least 2 months of data for comparison.")
        return
    
    # Calculate monthly totals
    monthly_totals = []
    for month in months_with_data:
        total = df_temp[df_temp['YEAR_MONTH'] == month]['AMOUNT'].sum()
        monthly_totals.append(total)
    
    # Create bar chart
    plt.figure(figsize=(12, 6))
    
    # Plot bars
    bars = plt.bar(range(len(months_with_data)), monthly_totals, 
                   color=['#ff6b6b', '#4ecdc4', '#45b7d1'],
                   edgecolor='black', linewidth=1.5)
    
    # Customize chart
    plt.title('Monthly Expense Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Expenses ($)', fontsize=12)
    plt.xticks(range(len(months_with_data)), months_with_data, rotation=45)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3)
    
    # Add trend line
    if len(months_with_data) > 1:
        plt.plot(range(len(months_with_data)), monthly_totals, 
                'ro-', linewidth=2, markersize=8, label='Trend')
        plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Show percentage changes
    print("\n📈 MONTHLY TREND")
    print("-" * 40)
    for i in range(len(months_with_data)-1):
        current = monthly_totals[i]
        previous = monthly_totals[i+1]
        change = ((current - previous) / previous) * 100
        arrow = "↑" if change > 0 else "↓"
        emoji = "🔴" if change > 0 else "🟢"
        print(f"{months_with_data[i]} vs {months_with_data[i+1]}: {arrow} {abs(change):.1f}% {emoji}")    
     
def top_expense():
    global df
    print("\n" + "="*50)
    print("📊 TOP 5 MOST EXPENSIVE EXPENSES")
    print("="*50)
    if df.empty:
        print("No expenses recorded yet.")
        return  
    top_expenses = df.sort_values(by='AMOUNT', ascending=False).head(5)
    print(top_expenses.to_string(index=False))








#############################################################################################
def save_data():
    """Save all expense data and budgets to JSON file"""
    global expense_data, budget, current_budget_month, DEFAULT_CATEGORIES
    
    try:
        # Create a dictionary with all data to save
        data_to_save = {
            "expense_data": expense_data,
            "budget": budget,
            "current_budget_month": current_budget_month,
            "DEFAULT_CATEGORIES": DEFAULT_CATEGORIES
        }
        
        # Save to JSON file
        with open('expense_tracker_data.json', 'w') as f:
            json.dump(data_to_save, f, indent=4)
        
        print(f"\n✅ Data saved successfully to 'expense_tracker_data.json'")
        print(f"   Total expenses: {len(expense_data['ID'])}")
        print(f"   Total budgets: {len(budget)}")
        
    except Exception as e:
        print(f"❌ Error saving data: {e}")

def load_data():
    """Load all expense data and budgets from JSON file"""
    global expense_data, budget, current_budget_month, DEFAULT_CATEGORIES, df
    
    filename = 'expense_tracker_data.json'
    
    # Check if file exists
    if not os.path.exists(filename):
        print("No existing data file found. Starting fresh.")
        return False
    
    try:
        # Load from JSON file
        with open(filename, 'r') as f:
            loaded_data = json.load(f)
        
        # Restore data
        expense_data = loaded_data.get("expense_data", expense_data)
        budget = loaded_data.get("budget", budget)
        current_budget_month = loaded_data.get("current_budget_month", 
                                               datetime.now().strftime("%Y-%m"))
        DEFAULT_CATEGORIES = loaded_data.get("DEFAULT_CATEGORIES", DEFAULT_CATEGORIES)
        
        # Recreate DataFrame from loaded data
        df = pd.DataFrame(expense_data)
        
        print(f"\n✅ Data loaded successfully from '{filename}'")
        print(f"   Total expenses: {len(expense_data['ID'])}")
        print(f"   Total budgets: {len(budget)}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False
    

##########################################################################################    

def main():
    while True:
        print("\n" + "="*50)
        print("EXPENSE TRACKER MAIN MENU")
        print("="*50)
        print("""
                1.Add Expense
                2.View Expense
                3.Delete Expense
                4.Set Budget
                5.Show Stastistics
                6.Save Data 
                7.Load Data
                8. Exit
                 """)
        try:
            opt=int(input("Which operation do you want to perform?"))
            if opt== 1 :
                add_expenses()
            if opt== 2 :
                view_expense()
            if opt== 3 :
                delete_expense()
            if opt== 4 :
                set_budget()
            if opt== 5 :
                show_statistics()
            if opt== 6 :
                save_data()
            
            if opt== 7:
                load_data()
            if opt== 8:
                print("Exiting the program. Goodbye!")
                break
        except ValueError:
            print("enter correct type of input")
            continue
        except KeyError:
            print("Error: Please enter a number between 1 and 9!")
            continue
if __name__=="__main__":
    main()
            
                
