import mysql.connector
from login.user_auth_sql import authentication
from login.user_auth_sql import connect_db

auth = authentication()
username = auth

db = connect_db()
cursor = db.cursor()


def view_all_users():
    select_users_query = """
    SELECT id, name, email FROM users;
    """

    cursor.execute(select_users_query)
    users = cursor.fetchall()

    if users:
        print("Users in the database:")
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    else:
        print("No users found in the database.")

# Function to add a new user
def add_new_user(name, email, password):
    insert_user_query = """
    INSERT INTO users (name, email, password)
    VALUES (%s, %s, %s);
    """
    user_data = (name, email, password)
    try:
        cursor.execute(insert_user_query, user_data)
        db.commit()
        print(f"New user '{name}' added successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()


def add_expense(user_id, amount, expense_type, expense_date):
    insert_expense_query = """
    INSERT INTO expenses (user_id, amount, expense_type, expense_date)
    VALUES (%s, %s, %s, %s);
    """
    expense_data = (user_id, amount, expense_type, expense_date)
    try:
        cursor.execute(insert_expense_query, expense_data)
        db.commit()
        print(f"Expense of {amount} for '{expense_type}' added successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()


def get_user_expenses(user_id):
    select_expenses_query = """
    SELECT amount, expense_type, expense_date 
    FROM expenses
    WHERE user_id = %s;
    """
    cursor.execute(select_expenses_query, (user_id,))
    expenses = cursor.fetchall()

    if expenses:
        print(f"Expenses for User ID {user_id}:")
        for expense in expenses:
            print(f"Amount: {expense[0]}, Type: {expense[1]}, Date: {expense[2]}")
    else:
        print("No expenses found for this user.")


def admin_database():
    while True:
        print("WELCOME TO EXPENSE MANAGEMENT APPLICATION")
        print("1. Add new user\n2. Add new expense\n3. View expenses\n4. View all users\n5. Exit")
        user_input = input("Enter your choice: ")
        if user_input == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            add_new_user(name, email, password)

        elif user_input == "2":
            user_id = input("Enter your user id: ")
            amount = input("Enter amount of expense: ")
            expense_type = input("Enter expense type: ")
            expense_date = input("Enter expense date: ")
            add_expense(user_id, amount, expense_type, expense_date)

        elif user_input == "3":
            user_id = input("Enter user id: ")
            get_user_expenses(user_id)

        elif user_input == "4":
            view_all_users()

        elif user_input == "5":
            break


def manage_expenses():
    while True:
        print("WELCOME TO EXPENSE MANAGEMENT APPLICATION")
        print("1. Add new expense\n2. View expenses\n3. Exit")
        user_input = input("Enter your choice: ")

        if user_input == "1":
            user_id = input("Enter your user id: ")
            amount = input("Enter amount of expense: ")
            expense_type = input("Enter expense type: ")
            expense_date = input("Enter expense date: ")
            add_expense(user_id, amount, expense_type, expense_date)

        elif user_input == "2":
            user_id = input("Enter user id: ")
            get_user_expenses(username)


        elif user_input == "3":
            break

# manage_expenses()
admin_database()
