import time

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):
        return f"Thank you, {self.name.title()}, {self.age} years old"

class BankAccount(User):
    total_deposits = 0
    total_withdrawals = 0

    def __init__(self, name, age, balance, account_number, password, account_type):
        super().__init__(name, age)
        self.balance = balance
        self.account_number = account_number
        self.password = password
        self.account_type = account_type

    def show_details(self):
        return f"{self.name} remaining balance of: {round(self.balance, 2)}"

    def deposit(self, amount):
        self.balance += amount
        BankAccount.total_deposits += amount
        print("Thank you for depositing...")
        return f"Your balance is now: {round(self.balance, 2)}"

    def withdraw(self, amount):
        if self.balance < amount:
            return "Withdrawal failed, insufficient funds"
        else:
            self.balance -= amount
            BankAccount.total_withdrawals += amount
            print("Thank you for withdrawing...")
            return f"Your balance is now: {round(self.balance, 2)}"

    def save_to_file(self, filename='accounts.txt'):
        account_info = f"{self.name},{self.age},{self.account_number},{self.password},{self.account_type},{self.balance}\n"
        with open(filename, 'a') as file:
            file.write(account_info)

    @staticmethod
    def load_from_file(account_number, password, filename='accounts.txt'):
        with open(filename, 'r') as file:
            for line in file:
                name, age, acc_num, pwd, acc_type, balance = line.strip().split(',')
                if acc_num == account_number and pwd == password:
                    print("Login successful.")
                    return BankAccount(name, int(age), float(balance), acc_num, pwd, acc_type)
        print("Invalid account number or password.")
        return None

    @staticmethod
    def generate_account_number():
        current_time = str(int(time.time() * 1000))
        return current_time[-8:]

    def transfer_money(self, recipient_account, amount):
        if self.balance < amount:
            return "Transfer failed due to insufficient amount"
        else:
            self.balance -= amount
            recipient_account.balance += amount
            print(f"Successfully sent {amount} to {recipient_account.name}.")
            return f"Your new balance is: {round(self.balance, 2)}"

def user_options(bank_account, all_accounts):
    print('Account successfully created.')
    print("Here are a few options, choose the number you want:")
    while True:
        choice = int(input("1) balance\n2) Withdraw\n3) Deposit\n4) total deposits\n5) total withdrawals\n6) Send money\n7) Logout\nEnter choice: "))
        if choice == 1:
            print(bank_account.show_details())
        elif choice == 2:
            amount = float(input(f"{bank_account.name.title()}, enter how much you would like to withdraw: "))
            print(bank_account.withdraw(amount))
        elif choice == 3:
            amount = float(input(f"{bank_account.name.title()}, enter how much you would like to deposit: "))
            print(bank_account.deposit(amount))
        elif choice == 4:
            print(f"There have been {BankAccount.total_deposits} total deposits.")
        elif choice == 5:
            print(f"There have been {BankAccount.total_withdrawals} total withdrawals.")
        elif choice == 6:
            recipient_account_number = input("Enter the recipient's account number: ")
            recipient_account = next((acc for acc in all_accounts if acc.account_number == recipient_account_number), None)
            if recipient_account:
                amount = float(input(f"enter the amount you would like to send to {recipient_account.name}? "))
                print(bank_account.transfer_money(recipient_account, amount))
            else:
                print("Recipient account not found.")
        elif choice == 7:
            print("Thank you for using Rigsel Bank")
            return True
        else:
            print("Please choose a number from 1-7.")

def create_bank_account():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    account_number = BankAccount.generate_account_number()
    password = input("Create a password: ")
    account_type = input("Enter account type (Personal/commercial): ")
    balance = float(input("Enter your deposit amount: "))
    new_account = BankAccount(name, age, balance, account_number, password, account_type)
    new_account.save_to_file()
    return new_account

def main():
    all_accounts = []
    while True:
        print("Welcome to Rigsel Bank")
        choice = input("1) Create Account\n2) Login\n3) Exit\nEnter choice: ")

        if choice == '1':
            new_account = create_bank_account()
            all_accounts.append(new_account)
            print(f"Account created. Account Number: {new_account.account_number}, Password: {new_account.password}")
            user_options(new_account, all_accounts)
        elif choice == '2':
            account_number = input("Enter your account number: ")
            password = input("Enter your password: ")
            existing_account = BankAccount.load_from_file(account_number, password)
            if existing_account:
                user_options(existing_account, all_accounts)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
