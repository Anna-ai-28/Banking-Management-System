Bank Management System

A simple bank management web app built with Python, Streamlit, and JSON for data storage. It allows users to create accounts, deposit, withdraw, check details, update, and delete accounts.

Features
Create a new bank account with a unique account number.
Deposit and withdraw money (with limits).
View account details in a structured format.
Update personal details (name, email, PIN).
Delete an account permanently.
How to Run
Make sure you have Python (3.x) installed.

Install dependencies:

pip install streamlit

Run the app:

python -m streamlit run app.py
Data Storage

This app uses a data.json file for storing user data locally. All accounts and balances are saved in this file. Make sure the file stays in the same directory as the app.

Future Improvements
Add user authentication (secure login system).
Deploy on a cloud platform (e.g., Streamlit Cloud or Heroku).
Add transaction history tracking.
