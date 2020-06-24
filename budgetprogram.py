"""
Develop a Budget Program
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from os import system, name

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet1 = client.open("lukebudget").sheet1
data = sheet1.get_all_records()
"""
Examples:
#pprint(data)
#row = sheet1.row_values(3)
#col = sheet1.col_values(3)
#sheet1.update_cell(1, 1, 'Expense')
#sheet1.cell(1, 1).value
#sheet1.insert_row(row, index)
#sheet1.delete_row(row)
pprint(sheet1.row_count)
#cell_list = worksheet.findall('Expense')
#pprint(sheet1.row_values(1)[1])
"""

#sheet1.insert_row(1, 14)




def clear():

    if name == 'nt':
        _ = system('cls')

### create dictionary of expenses
expenses = sheet1.col_values(1)[1:]
exp_d = {}
for i, v in enumerate(expenses):
    exp_d[i+1] = v

def get_expense_value(expense, month=False):    
    for k, v in exp_d.items():
        if k == expense:
            if month == True:
                return sheet1.cell(k+1, 1).value, float(sheet1.row_values(k+1)[month])
            elif month == False:
                return sheet1.cell(k+1, 1).value

def view_expenses():
    print('Here are your expenses:')
    for k, v in exp_d.items():
        if k > 0:
            print(k, v)
    
    user_input = int(input('Please choose an expense to view (1-12): '))
    user_month = int(input('Please choose a month (1-12): '))

    return user_input, user_month

def add_new_expense():
    new_expense = str(input('Please describe your new expense? '))
    values = [new_expense, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    x = sheet1.insert_row(values, index = len(exp_d)+2, value_input_option='Raw')
    return x, len(exp_d)+1
    
    

def update_value(expense, month, payment):
    update = float(sheet1.row_values(expense+1)[month]) - payment
    sheet1.update_cell(expense+1, month+1, update)
    return sheet1.cell(expense+1, 1).value, float(sheet1.row_values(expense+1)[month])


program_on = True
while program_on:
    clear()
    print('Welcome back, Luke!')
    print('')
    print('1. View Expense \n2. Update Expenses \n3. Add New Expense') #\n4. Budget for Future Expense')
    task = int(input('What task would you like to perform? '))
    if task == 1:
        expense, month = view_expenses()
        x = get_expense_value(expense, month=True)
        pprint(x)
    
    elif task == 2:
        u_expense, u_month = view_expenses()
        payment_input = float(input('How much did you pay off? '))
        update = update_value(u_expense, u_month, payment_input)
        pprint(update)
    
    elif task == 3:
        _, new_expense = add_new_expense()
        #print(new_expense, values[0])
        x = get_expense_value(new_expense, month=False)
        print(f'{x} has been added to your expenses.')

    elif task == 4:
        pass
        
        

    
    choose_another = input('Would you like to choose another (y/n): ')
    if choose_another.lower() == 'y':
        continue
    else:
        break

