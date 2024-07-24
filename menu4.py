from module4 import Bank

bank = Bank()
    
    
while True:
        print("Service Provided:")
        print("1. Acc Creation")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Fixed Deposit")
        print("5. Transaction Details")
        print("6. Check Credit Card Eligibility")
        print("7. Exit")
        
        choice = int(input())
        if choice == 1:
            name = input("Enter Name: ")
            depamt = int(input("Enter Deposit Amt: "))
            fdamt = int(input("Enter FD Amt: "))
            bank.create(name, depamt, fdamt)
        elif choice == 2:
            accno = int(input("Enter Accno: "))
            depamt = int(input("Enter Deposit amt: "))
            bank.deposit(accno, depamt)
        elif choice == 3:
            accno = int(input("Enter Accno: "))
            witamt = int(input("Enter Withdraw amt: "))
            bank.withdraw(accno, witamt)
        elif choice == 4:
            accno = int(input("Enter Accno: "))
            fdamt = int(input("Enter FD amt: "))
            yrs = int(input("Enter years: "))
            bank.fd(accno, fdamt, yrs)
        elif choice == 5:
            accno = int(input("Enter Accno: "))
            bank.transaction(accno)
        elif choice == 6:
            accno = int(input("Enter Accno: "))
            bank.credit_card(accno)
        elif choice == 7:
            break
        else:
            print("Invalid choice") 