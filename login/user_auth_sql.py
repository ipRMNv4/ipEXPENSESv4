import bcrypt
import mysql.connector

# from mail import send_login_notification

def connect_db():
    # root = input("MYSQL: enter your username: ")
    # root_pass = input("MYSQL: enter your password: ")

    return mysql.connector.connect(
        host = "localhost",
        user = "USERNAME",
        password = "PASSWORD",
        database = "expense_management"
    )


def register():
    db = connect_db()
    cursor = db.cursor()

    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    combo = (username+password).encode()
    hashed = bcrypt.hashpw(combo, bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed.decode()))

        db.commit()
        print("registration successful")

    except mysql.connector.IntegrityError:
        print("username or email already registered")

    finally:
        cursor.close()
        db.close()





def authentication():
    db = connect_db()
    cursor = db.cursor()

    username = input("Username: ")


    cursor.execute("SELECT password FROM users WHERE name = %s", (username,))
    result = cursor.fetchone()

    if result:
        password = input("Password: ")
        saved_hashed = result[0].encode()
        combo = (username+password).encode()

        if bcrypt.checkpw(combo,saved_hashed):
            print("Password matches!")
            # send_login_notification()
            return username
        else:
            print("Incorrect password!")
            # send_login_notification()
            return False

    else:
        print("You need to register first...")
        register()

    cursor.close()
    db.close()

authentication()


