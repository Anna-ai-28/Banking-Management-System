import json
import random
import string
from pathlib import Path

class Bank:
    database = str(Path(__file__).parent / 'data.json')
    data = []

    def __init__(self):
        # Load data safely
        if Path(self.database).exists():
            try:
                with open(self.database, 'r') as file:
                    self.__class__.data = json.load(file)
            except:
                self.__class__.data = []
        else:
            with open(self.database, 'w') as file:
                json.dump([], file)
            self.__class__.data = []

    @staticmethod
    def __update():
        with open(Bank.database, 'w') as file:
            json.dump(Bank.data, file, indent=4)
            file.flush()

    @classmethod
    def __accountNoGenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        nums = random.choices(string.digits, k=3)
        spChar = random.choices('!@#$%^&*', k=1)
        acc_id = alpha + nums + spChar
        random.shuffle(acc_id)
        return "".join(acc_id)

    def createAccount(self):
        try:
            info = {
                'name': input('Your name: '),
                'age': int(input('Your age: ')),
                'email': input('Your email: '),
                'pin': int(input('Your pin (4 digit): ')),
                'accountNo.': Bank.__accountNoGenerate(),
                'balance': 0
            }

            if info['age'] < 18 or len(str(info['pin'])) != 4:
                print("❌ Invalid age or PIN")
                return

            Bank.data.append(info)
            Bank.__update()

            print("\n✅ Account created successfully!")
            print("👉 Your Account Number:", info['accountNo.'])

        except Exception as e:
            print("Error:", e)

    def depositMoney(self):
        accNumber = input('Enter account number: ')
        pin = int(input('Enter pin: '))

        userData = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]

        if not userData:
            print('❌ No user found')
            return

        amount = int(input("Enter amount to deposit: "))

        if amount <= 0 or amount > 10000:
            print('❌ Deposit must be between 1 and 10000')
            return

        userData[0]['balance'] += amount
        Bank.__update()

        print('✅ Amount deposited successfully!')

    def withdrawMoney(self):
        accNumber = input('Enter account number: ')
        pin = int(input('Enter pin: '))

        userData = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]

        if not userData:
            print('❌ No user found')
            return

        amount = int(input("Enter amount to withdraw: "))

        if amount > userData[0]['balance']:
            print('❌ Insufficient balance')
            return

        userData[0]['balance'] -= amount
        Bank.__update()

        print('✅ Amount withdrawn successfully!')

    def showDetails(self):
        accNumber = input('Enter account number: ')
        pin = int(input('Enter pin: '))

        userData = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]

        if not userData:
            print("❌ No user found")
            return

        print('\n📄 Your Details:')
        for key, value in userData[0].items():
            print(f'{key} : {value}')

    def updateDetails(self):
        accNumber = input('Enter account number: ')
        pin = int(input('Enter pin: '))

        userData = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]

        if not userData:
            print('❌ No user found')
            return

        print('Leave blank to keep old values')

        new_name = input('New name: ')
        new_email = input('New email: ')
        new_pin = input('New pin: ')

        if new_name:
            userData[0]['name'] = new_name

        if new_email:
            userData[0]['email'] = new_email

        if new_pin:
            if len(new_pin) == 4 and new_pin.isdigit():
                userData[0]['pin'] = int(new_pin)
            else:
                print("❌ Invalid PIN format")

        Bank.__update()
        print('✅ Details updated successfully!')

    def deleteAccount(self):
        accNumber = input('Enter account number: ')
        pin = int(input('Enter pin: '))

        userData = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]

        if not userData:
            print('❌ No user found')
            return

        confirm = input('Are you sure? (y/n): ')

        if confirm.lower() != 'y':
            print('Cancelled')
            return

        Bank.data.remove(userData[0])
        Bank.__update()

        print('✅ Account deleted successfully!')


# -------- MAIN PROGRAM --------

user = Bank()

while True:
    print("\n--- BANK MENU ---")
    print('1. Create Account')
    print('2. Deposit Money')
    print('3. Withdraw Money')
    print('4. Show Details')
    print('5. Update Details')
    print('6. Delete Account')
    print('7. Exit')

    try:
        choice = int(input('Enter your choice: '))

        if choice == 1:
            user.createAccount()
        elif choice == 2:
            user.depositMoney()
        elif choice == 3:
            user.withdrawMoney()
        elif choice == 4:
            user.showDetails()
        elif choice == 5:
            user.updateDetails()
        elif choice == 6:
            user.deleteAccount()
        elif choice == 7:
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

    except ValueError:
        print("❌ Enter a valid number")