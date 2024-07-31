import os
import math
from mysql import connector
from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()



create_table_queries = [
    """CREATE TABLE IF NOT EXISTS bankdata (
        name VARCHAR(30),
        accNo INT PRIMARY KEY,
        balance INT,
        fdamt INT
    )""",
    """CREATE TABLE IF NOT EXISTS banktrans (
        transId INT PRIMARY KEY AUTO_INCREMENT,
        accNo INT,
        transtype VARCHAR(20),
        amount INT,
        balance INT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (accNo) REFERENCES bankdata(accNo)
    )""",
    """CREATE TABLE IF NOT EXISTS bankcreditscr (
        accNo INT PRIMARY KEY,
        credit INT,
        membership VARCHAR(25),
        FOREIGN KEY (accNo) REFERENCES bankdata(accNo)
    )"""
]

try:
    with connector.connect(
        host="localhost",
        user="root",
        password="123456",
    ) as database:
        
        create_db = "CREATE DATABASE IF NOT EXISTS bankdatabase"
        with database.cursor() as cursor:
            cursor.execute(create_db)
        
        with connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="bankdatabase"
        ) as database:
            
            with database.cursor() as cursor:
                
                for query in create_table_queries:
                    cursor.execute(query)
                    
                database.commit()

except connector.Error as e:
    print(e)


class Bank:
    def __init__(self):
        self.db = connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="bankdatabase"
        )
        self.initialize_data()

    def initialize_data(self):
        query = "SELECT name, accNo, balance, fdamt FROM bankdata"
        
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query)
                self.data = cursor.fetchall()
        except connector.Error as e:
            print(e)

    def create(self, name, bal, fd):
        query = "INSERT INTO bankdata (name, accNo, balance, fdamt) VALUES (%s, %s, %s, %s)"
        last_accno = "SELECT MAX(accNo) FROM bankdata"

        try:
            with self.db.cursor() as cursor:
                cursor.execute(last_accno)
                result = cursor.fetchone()[0]
                accno = result + 1 if result else 1
                cursor.execute(query, (name, accno, bal, fd))
                self.db.commit()
                self.data.append((name, accno, bal, fd))
                print("Name: ", name)
                print("AccNo.: ", accno)
                print("Balance: ", bal)
                print("Fixed Deposit: ", fd)
                print("Your Account Created. Thank You !!!!")
        except connector.Error as e:
            print(e)

    def deposit(self, accno, depamt):
        bal_query = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_query = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        trans_query = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"

        try:
            with self.db.cursor() as cursor:
                cursor.execute(update_query, (depamt, accno))
                self.db.commit()
                cursor.execute(bal_query, (accno,))
                balance = cursor.fetchone()[0]
                cursor.execute(trans_query, (accno, 'deposit', depamt, balance))
                self.db.commit()
                print("Deposited Rs.", depamt)
                print("Balance Rs.", balance)
                self.update_creditscore(accno)
        except connector.Error as e:
            print(e)

    def withdraw(self, accno, witamt):
        bal_query = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_query = "UPDATE bankdata SET balance = balance - %s WHERE accNo = %s"
        trans_query = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"

        try:
            with self.db.cursor() as cursor:
                cursor.execute(bal_query, (accno,))
                crnt_bal = cursor.fetchone()[0]

                if witamt > crnt_bal:
                    print("Insufficient Funds.")
                    return

                cursor.execute(update_query, (witamt, accno))
                self.db.commit()
                cursor.execute(bal_query, (accno,))
                new_bal = cursor.fetchone()[0]
                cursor.execute(trans_query, (accno, 'withdraw', witamt, new_bal))
                self.db.commit()
                print("Withdrawn Rs.", witamt)
                print("Balance Rs.", new_bal)
                self.update_creditscore(accno)

        except connector.Error as e:
            print(e)

    def fd(self, accno, fdamt, yrs):
        idx = None
        for i in self.data:
            if i[1] == accno:
                idx = self.data.index(i)
                break

        if idx is None:
            print("Invalid Accno.")
            return

        if fdamt < 50000:
            rtn = (10000 * yrs) + self.data[idx][3]
            print("Your Return will be Rs.", rtn)
        elif fdamt < 100000:
            rtn = (20000 * yrs) + self.data[idx][3]
            print("Your Return will be Rs.", rtn)
        else:
            print("FD should be above 50000")

    def transaction(self, accno):
        query = "SELECT * FROM banktrans WHERE accNo = %s ORDER BY transId DESC LIMIT 5"

        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchall()

                if not result:
                    print("No Transaction Found.")
                else:
                    table = PrettyTable()
                    table.field_names = ["Transaction ID", "Account No", "Transaction Type", "Amount", "Balance", "Timestamp"]
                    for row in result:
                        table.add_row(row)
                    print(table)

        except connector.Error as e:
            print(e)

    def update_creditscore(self, accno):
        query = "SELECT COUNT(*) FROM banktrans WHERE accNo = %s"

        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                nooftrans = cursor.fetchone()[0]
                crdscr = nooftrans * 10
                if crdscr < 50:
                    memship = "None"
                elif crdscr >= 50 and crdscr < 100:
                    memship = "Silver"
                elif crdscr >= 100 and crdscr < 150:
                    memship = "Gold"
                elif crdscr >= 150:
                    memship = "Diamond"

                cursor.execute("REPLACE INTO bankcreditscr (accNo, credit, membership) VALUES (%s, %s, %s)", (accno, crdscr, memship))
                self.db.commit()

        except connector.Error as e:
            print(e)

    def credit_card(self, accno):
        query = "SELECT credit FROM bankcreditscr WHERE accNo = %s"

        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                if not result:
                    print("No Credit Card Info.")
                    return
                
                credit_pnts = result[0]
                if credit_pnts >= 150:
                    card_type = "Diamond"
                    limit = 100000
                elif credit_pnts >= 100:
                    card_type = "Gold"
                    limit = 50000
                elif credit_pnts >= 50:
                    card_type = "Silver"
                    limit = 25000
                else:
                    card_type = "None"
                if card_type == "None":
                    print("You are not eligible for credit card yet.")
                else:
                    print("You are eligible for credit card - ", card_type)
                    print("Limit is Rs.", limit)
        except connector.Error as e:

            print(e)



    def bike(self,accno,bike_value,model_year):
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 25000:
                    if bike_value <= 90000 or model_year <= 2020:
                        loan_amt = bike_value - 30000
                        cursor.execute(update_balance, (loan_amt,accno))
                        self.db.commit()
                        cursor.execute(new_balance, (accno,))
                        balance = cursor.fetchone()[0]
                        cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                        self.db.commit()
                        print("Your loan is approved. The loan amount is credited to your account.")
                        print("Your balance Rs.",balance)
                    elif bike_value <= 150000 or model_year <= 2024:
                        loan_amt = bike_value - 20000
                        cursor.execute(update_balance, (loan_amt,accno))
                        self.db.commit()
                        cursor.execute(new_balance, (accno,))
                        balance = cursor.fetchone()[0]
                        print("Your loan is approved. The loan amount is credited to your account.")
                        print("Your balance Rs.",balance)
                else:
                    print("You are not eligible for bike loan yet.")

        except connector.Error as e:
            print(e)




    def car(self,accno,car_value,model_year):   #changethecode
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 100000:
                    if car_value <= 500000 and model_year <= 2020:
                        loan_amt = car_value - 30000
                        cursor.execute(update_balance, (loan_amt,accno))
                        self.db.commit()
                        cursor.execute(new_balance, (accno,))
                        balance = cursor.fetchone()[0]
                        cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                        self.db.commit()
                        print("Your loan is approved. The loan amount is credited to your account.")
                        print("Your balance Rs.",balance)
                    elif car_value <= 150000 and model_year <= 2024:
                        loan_amt = car_value - 20000
                        cursor.execute(update_balance, (loan_amt,accno))
                        self.db.commit()
                        cursor.execute(new_balance, (accno,))
                        balance = cursor.fetchone()[0]
                        print("Your loan is approved.The loan amount is credited to your account.")
                        print("Your balance Rs.",balance)
                else:
                    print("You are not eligible for car loan yet.")

        except connector.Error as e:
            print(e)



    def loan_purchase_of_land(self,accno,loan_amt,loan_term):
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 1000000:
                    emi = ( loan_amt * 0.75 * math.pow(1 + 0.75, loan_term)) / (math.pow(1 + 0.75, loan_term) - 1)
                    cursor.execute(update_balance, (loan_amt,accno))
                    self.db.commit()
                    cursor.execute(new_balance, (accno,))
                    balance = cursor.fetchone()[0]
                    cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                    self.db.commit()
                    print("Your loan is approved. The loan amount is credited to your account.")
                    print("Your balance Rs.",balance)
                    print("Your EMI is Rs.",emi)
                 
                else:
                    print("You are not eligible for car loan yet.")

        except connector.Error as e:
            print(e)




    def loan_home_purchase(self,accno,loan_amt,loan_term):
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 1000000:
                    emi = ( loan_amt * 0.75 * math.pow(1 + 0.83, loan_term)) / (math.pow(1 + 0.75, loan_term) - 1)
                    cursor.execute(update_balance, (loan_amt,accno))
                    self.db.commit()  #roundup
                    cursor.execute(new_balance, (accno,))
                    balance = cursor.fetchone()[0]
                    cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                    self.db.commit()
                    print("Your loan is approved. The loan amount is credited to your account.")
                    print("Your balance Rs.",balance)
                    print("Your EMI is Rs.",emi)
                 
                else:
                    print("You are not eligible for car loan yet.")

        except connector.Error as e:
            print(e)


    def loan_home_construction(self, accno, loan_amt, loan_term):
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
    
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 1000000:
                    monthly_interest_rate = 0.91 / 12  # Correct monthly interest rate calculation
                    num_payments = loan_term * 12  # Correct loan term in months
                    emi = (loan_amt * monthly_interest_rate * math.pow(1 + monthly_interest_rate, num_payments)) / \
                          (math.pow(1 + monthly_interest_rate, num_payments) - 1)
                    cursor.execute(update_balance, (loan_amt, accno))
                    self.db.commit()
                    cursor.execute(new_balance, (accno,))
                    balance = cursor.fetchone()[0]
                    cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                    self.db.commit()
                    print("Your loan is approved. The loan amount is credited to your account.")
                    print("Your balance Rs.", balance)
                    print("Your EMI is Rs.", emi)
             
                else:
                     print("You are not eligible for a home construction loan yet.")

        except connector.Error as e:
            print(e)



    def loan_home_extension(self,accno,loan_amt,loan_term):
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 1000000:
                    emi = ( loan_amt * 0.75 * math.pow(1 + 0.1, loan_term)) / (math.pow(1 + 0.75, loan_term) - 1)
                    cursor.execute(update_balance, (loan_amt,accno))
                    self.db.commit()
                    cursor.execute(new_balance, (accno,))
                    balance = cursor.fetchone()[0]
                    cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                    self.db.commit()
                    print("Your loan is approved. The loan amount is credited to your account.")
                    print("Your balance Rs.",balance)
                    print("Your EMI is Rs.",emi)
                 
                else:
                    print("You are not eligible for car loan yet.")

        except connector.Error as e:
            print(e)



    def loan_home_improvement(self,accno,loan_amt,loan_term):
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 1000000:
                    emi = ( loan_amt * 0.75 * math.pow(1 + 0.6, loan_term)) / (math.pow(1 + 0.75, loan_term) - 1)
                    cursor.execute(update_balance, (loan_amt,accno))
                    self.db.commit()
                    cursor.execute(new_balance, (accno,))
                    balance = cursor.fetchone()[0]
                    cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                    self.db.commit()
                    print("Your loan is approved. The loan amount is credited to your account.")
                    print("Your balance Rs.",balance)
                    print("Your EMI is Rs.",emi)
                 
                else:
                    print("You are not eligible for car loan yet.")

        except connector.Error as e:
            print(e)



    def loan_personal(self,accno,loan_amt,loan_term):
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 1000000:
                    emi = ( loan_amt * 0.75 * math.pow(1 + 0.6, loan_term)) / (math.pow(1 + 0.75, loan_term) - 1)
                    cursor.execute(update_balance, (loan_amt,accno))
                    self.db.commit()
                    cursor.execute(new_balance, (accno,))
                    balance = cursor.fetchone()[0]
                    cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                    self.db.commit()                                                                #not updating transaction table
                    print("Your loan is approved. The loan amount is credited to your account.")
                    print("Your balance Rs.",balance)
                    print("Your EMI is Rs.",emi)
                 
                else:
                    print("You are not eligible for car loan yet.")

        except connector.Error as e:
            print(e)



    def loan_education(self,accno,loan_amt,loan_term):
        query = "SELECT SUM(amount) AS trans_amt FROM banktrans WHERE accNo = %s"
        update_balance = "UPDATE bankdata SET balance = balance + %s WHERE accNo = %s"
        new_balance = "SELECT balance FROM bankdata WHERE accNo = %s"
        update_trans = "INSERT INTO banktrans (accNo, transtype, amount, balance, timestamp) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, (accno,))
                result = cursor.fetchone()
                trans_amt = result[0] if result[0] is not None else 0
                if trans_amt > 1000000:
                    emi = ( loan_amt * 0.75 * math.pow(1 + 0.6, loan_term)) / (math.pow(1 + 0.75, loan_term) - 1)
                    cursor.execute(update_balance, (loan_amt,accno))
                    self.db.commit()
                    cursor.execute(new_balance, (accno,))
                    balance = cursor.fetchone()[0]
                    cursor.execute(update_trans, (accno, 'Loan Credit', loan_amt, balance))
                    self.db.commit()
                    print("Your loan is approved. The loan amount is credited to your account.")
                    print("Your balance Rs.",balance)
                    print("Your EMI is Rs.",emi)
                 
                else:
                    print("You are not eligible for car loan yet.")

        except connector.Error as e:
            print(e)




#endd