from module4 import Bank

bank = Bank()

while True:
    print("!!! *** WELCOME TO THE BANK *** !!!")
    print("1. Existing User")
    print("2. New User")
    user_choice = int(input())

    if user_choice == 1:
        print("Service Provided:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Fixed Deposit")
        print("4. Transaction Details")
        print("5. Check Credit Card Eligibility")
        print("6. Loan Availability")
        print("7. Exit")

        service_choice = int(input())

        if service_choice == 1:
            accno = int(input("Enter Accno: "))
            isacc = False
            for i in bank.data:
                if i[1] == accno:
                    depamt = int(input("Enter Deposit amt: "))
                    if depamt > 50000:
                        pan = input("Enter Pan No.: ")
                        if len(pan) != 5:
                            print("Invalid PAN")
                    bank.deposit(accno, depamt)
                    isacc = True
                    break
            if not isacc:
                print("Invalid Account No.")
                print("Click NEW USER and create a new account.")

        elif service_choice == 2:
            accno = int(input("Enter Accno: "))
            isacc = False
            for i in bank.data:
                if i[1] == accno:
                    witamt = int(input("Enter Withdraw amt: "))
                    if witamt > 50000:
                        pan = input("Enter Pan No.: ")
                        if len(pan) != 5:
                            print("Invalid PAN")
                    bank.withdraw(accno, witamt)
                    isacc = True
                    break
            if not isacc:
                print("Invalid Account No.")
                print("Click NEW USER and create a new account.")


        elif service_choice == 3:
            accno = int(input("Enter Accno: "))
            isacc = False
            for i in bank.data:
                if i[1] == accno:
                    fdamt = int(input("Enter FD amt: "))
                    yrs = int(input("Enter years: "))
                    bank.fd(accno, fdamt, yrs)
                    isacc = True
                    break
            if not isacc:
                print("Invalid Account No.")
                print("Click NEW USER and create a new account.")


        
        elif service_choice == 4:
            accno = int(input("Enter Accno: "))
            isacc = False
            for i in bank.data:
                if i[1] == accno:
                    bank.transaction(accno)
                    isacc = True
                    break
            if not isacc:
                print("Invalid Account No.")
                print("Click NEW USER and create a new account.")

        elif service_choice == 5:
            accno = int(input("Enter Accno: "))
            isacc = False
            for i in bank.data:
                if i[1] == accno:
                    bank.credit_card(accno)
                    isacc = True
                    break
            if not isacc:
                print("Invalid Account No.")
                print("Click NEW USER and create a new account.")

        elif service_choice == 6:
            print("*** LOAN TYPE ***")
            print("1.Vehicle Loan")
            print("2.Home Loan")
            print("3.Personal Loan")
            print("4.Education Loan")
            loan_choice = int(input())

            if loan_choice == 1:
                print("Select Vehicle Type")
                print("1.Bike")
                print("2.Car")
                vehicle_choice = int(input())

                if vehicle_choice == 1:
                    accno = int(input("Enter Your AccNo: "))
                    bike_value = int(input("Enter Bike Value: "))
                    model_year = int(input("Enter Model Year: "))
                    bank.bike(accno,bike_value,model_year )

                elif vehicle_choice == 2:
                    accno = int(input("Enter Your AccNo: "))
                    car_value = int(input("Enter car Value: "))
                    model_year = int(input("Enter Model Year: "))
                    bank.car(accno,car_value,model_year)
                else:
                    print("Invalid Option")

            elif loan_choice == 2:
                print(" Select Loan Type")
                print("1.Home Loan For Purchase of Land")
                print("2.Home Purchase Loan")
                print("3.Home Construction Loan")
                print("4.Home Extension Loan")
                print("5.Home Improvement Loan (Renovation)")
                homeloan_type = int(input())

                if homeloan_type == 1:
                    print("Fixed interest for your loan is 0.75% p.m. which is 9% p.a")
                    accno = int(input("Enter Your AccNo: "))
                    loan_amt = int(input("Enter Loan Amount: "))
                    loan_term = int(input("Enter Loan Tenure in Months"))
                    bank.loan_purchase_of_land(accno,loan_amt,loan_term)

                elif homeloan_type == 2:
                    print("Fixed interest for your loan is 0.83% p.m. which is 10% p.a")
                    accno = int(input("Enter Your AccNo: "))
                    loan_amt = int(input("Enter Loan Amount: "))
                    loan_term = int(input("Enter Loan Tenure in Months"))
                    bank.loan_home_purchase(accno,loan_amt,loan_term)

                elif homeloan_type == 3:
                    print("Fixed interest for your loan is 0.91% p.m. which is 11% p.a")
                    accno = int(input("Enter Your AccNo: "))
                    loan_amt = int(input("Enter Loan Amount: "))
                    loan_term = int(input("Enter Loan Tenure in Months"))
                    bank.loan_home_construction(accno,loan_amt,loan_term)

                elif homeloan_type == 4:
                    print("Fixed interest for your loan is 1% p.m. which is 12% p.a")
                    accno = int(input("Enter Your AccNo: "))
                    loan_amt = int(input("Enter Loan Amount: "))
                    loan_term = int(input("Enter Loan Tenure in Months"))
                    bank.loan_home_extension(accno,loan_amt,loan_term)

                elif homeloan_type == 5:
                    print("Fixed interest for your loan is 0.6 p.m. which is 8% p.a")
                    accno = int(input("Enter Your AccNo: "))
                    loan_amt = int(input("Enter Loan Amount: "))
                    loan_term = int(input("Enter Loan Tenure in Months"))
                    bank.loan_home_improvement(accno,loan_amt,loan_term)

                else:
                    print("Invalid Option")
            

            elif loan_choice == 3:
                print("Fixed interest for your loan is 1.08% p.m. which is 13% p.a")
                accno = int(input("Enter Your AccNo: "))
                loan_amt = int(input("Enter Loan Amount: "))
                loan_term = int(input("Enter Loan Tenure in Months"))
                bank.loan_personal(accno,loan_amt,loan_term)

            elif loan_choice == 4:
                print("Fixed interest for your loan is 1% p.m. which is 12% p.a")
                accno = int(input("Enter Your AccNo: "))
                loan_amt = int(input("Enter Loan Amount: "))
                loan_term = int(input("Enter Loan Tenure in Months"))
                bank.loan_education(accno,loan_amt,loan_term)

            else:
                print("Invalid Option")


        elif service_choice == 7:
            break

        else:
            print("Invalid choice")

    elif user_choice == 2:
        print("New ACCOUNT CREATION")
        name = input("Enter Name: ")
        depamt = int(input("Enter Deposit Amt: "))
        fdamt = int(input("Enter FD Amt: "))
        bank.create(name, depamt, fdamt)
    else:
        print("Invalid choice")
