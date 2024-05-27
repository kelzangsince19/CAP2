import random
import string

class BankAccount:
    def __init__(self, account_type, initial_balance=0.0):
        # Initialize account with type and initial balance
        self.account_number = self._generate_account_number()
        self.password = self._generate_password()
        self.account_type = account_type
        self.balance = initial_balance

    def _generate_account_number(self):
        # Generate a random 10-digit account number
        return ''.join(random.choices(string.digits, k=10))

    def _generate_password(self):
        # Generate a random 8-character password
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def deposit(self, amount):
        # Deposit a positive amount to the account
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount:.2f} Ngultrum. New balance: {self.balance:.2f} Ngultrum")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        # Withdraw money from the account if funds are sufficient
        if amount > self.balance:
            print("Insufficient funds.")
        elif amount <= 0:
            print("Withdrawal amount must be positive.")
        else:
            self.balance -= amount
            print(f"Withdrew {amount:.2f} Ngultrum. New balance: {self.balance:.2f} Ngultrum")

    def display_balance(self):
        # Display the current account balance
        print(f"Account balance: {self.balance:.2f} Ngultrum")

class SavingsAccount(BankAccount):
    def __init__(self, initial_balance=0.0):
        # Init a savings account with the given balance
        super().__init__('Savings', initial_balance)

class CurrentAccount(BankAccount):
    def __init__(self, initial_balance=0.0):
        # init a current account with the given balance
        super().__init__('Current', initial_balance)

class BankSystem:
    def __init__(self, filename='accounts.txt'):
        # Init the bank system with a filename for account storage
        self.filename = filename
        self.accounts = self._load_accounts()

    def _load_accounts(self):
        # put accounts from a file into a dictionary
        accounts = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, account_number, account_type, balance = line.strip().split(',')
                    if account_type == 'Savings':
                        account = SavingsAccount(float(balance))
                    else:
                        account = CurrentAccount(float(balance))
                    account.account_number = account_number
                    account.password = password
                    accounts[username] = account
        except FileNotFoundError:
            pass
        return accounts

    def _save_accounts(self):
        # Save all accounts to the file
        with open(self.filename, 'w') as file:
            for username, account in self.accounts.items():
                file.write(f"{username},{account.password},{account.account_number},{account.account_type},{account.balance}\n")

    def create_account(self):
        # Create a new account with user input
        username = input("Enter NEW Username: ")
        if username in self.accounts:
            print("Username already exists. Try a different username.")
            return

        password = input("Enter NEW Password: ")
        initial_deposit = float(input("Enter your Deposit Amount in Ngultrum: "))
        account_type = input("Enter the type of bank account (Savings/Current): ").capitalize()

        if account_type == 'Savings':
            account = SavingsAccount(initial_deposit)
        elif account_type == 'Current':
            account = CurrentAccount(initial_deposit)
        else:
            print("Invalid account type. Account not created.")
            return

        account.password = password
        self.accounts[username] = account
        self._save_accounts()
        print(f"Account created successfully. Account Number: {account.account_number}")

    def login(self):
        # Log in to an existing account
        username = input("Enter Username: ")
        password = input("Enter PASSWORD: ")

        account = self.accounts.get(username)
        if account and account.password == password:
            print("LOGGED IN")
            return username
        else:
            print("Login FAILED")
            return None

    def delete_account(self, username):
        # Delete an account
        if username in self.accounts:
            del self.accounts[username]
            self._save_accounts()
            print("Account deleted successfully.")
        else:
            print("Account not found.")

    def send_money(self, from_username):
        # fund Transfer from one account to another
        to_account_number = input("Enter the recipient's account number: ")
        amount = float(input("Enter the amount to send in Ngultrum: "))

        sender_account = self.accounts[from_username]
        recipient_account = None

        for account in self.accounts.values():
            if account.account_number == to_account_number:
                recipient_account = account
                break

        if recipient_account:
            if sender_account.balance >= amount:
                sender_account.withdraw(amount)
                recipient_account.deposit(amount)
                self._save_accounts()
                print("Money sent successfully.")
            else:
                print("Insufficient funds.")
        else:
            print("Recipient account not found.")

    def main_menu(self):
        # show the main menu
        while True:
            print("\n1. Create a new account")
            print("2. Login to an existing account")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_account()
            elif choice == '2':
                username = self.login()
                if username:
                    self.account_menu(username)
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def account_menu(self, username):
        # show the account menu
        while True:
            print("\n1. Deposit")
            print("2. Withdraw")
            print("3. Send Money")
            print("4. Check Balance")
            print("5. Delete Account")
            print("6. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                amount = float(input("Enter amount to deposit in Ngultrum: "))
                self.accounts[username].deposit(amount)
                self._save_accounts()
            elif choice == '2':
                amount = float(input("Enter amount to withdraw in Ngultrum: "))
                self.accounts[username].withdraw(amount)
                self._save_accounts()
            elif choice == '3':
                self.send_money(username)
            elif choice == '4':
                self.accounts[username].display_balance()
            elif choice == '5':
                self.delete_account(username)
                break
            elif choice == '6':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.main_menu()

