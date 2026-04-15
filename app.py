import json
import random
import string
from pathlib import Path
import streamlit as st

# -------- DATA PATH --------
DB_PATH = Path(__file__).parent / "data.json"

# -------- LOAD / SAVE --------
def load_data():
    if DB_PATH.exists():
        try:
            with open(DB_PATH, "r") as f:
                return json.load(f)
        except:
            return []
    else:
        with open(DB_PATH, "w") as f:
            json.dump([], f)
        return []

def save_data(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

# -------- SESSION STATE --------
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# -------- UTILS --------
def generate_account_no():
    alpha = random.choices(string.ascii_letters, k=3)
    nums = random.choices(string.digits, k=3)
    sp = random.choice("!@#$%^&*")
    acc = alpha + nums + [sp]
    random.shuffle(acc)
    return "".join(acc)

def find_user(acc, pin):
    for user in data:
        if user["accountNo"] == acc and user["pin"] == pin:
            return user
    return None

# -------- UI --------
st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox("Menu", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Check Details",
    "Update Details",
    "Delete Account"
])

# -------- CREATE ACCOUNT --------
if menu == "Create Account":
    st.header("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create Account"):
        if age < 18 or len(pin) != 4 or not pin.isdigit():
            st.error("❌ Invalid age or PIN")
        else:
            acc_no = generate_account_no()
            user = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "accountNo": acc_no,
                "balance": 0
            }
            data.append(user)
            save_data(data)
            st.success(f"✅ Account created! Account No: {acc_no}")

# -------- DEPOSIT --------
elif menu == "Deposit":
    st.header("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1, max_value=10000)

    if st.button("Deposit Money"):
        if not pin.isdigit():
            st.error("Enter valid PIN")
        else:
            user = find_user(acc, int(pin))

            if not user:
                st.error("❌ User not found")
            else:
                user["balance"] += amount
                save_data(data)
                st.success("✅ Amount deposited!")

# -------- WITHDRAW --------
elif menu == "Withdraw":
    st.header("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw Money"):
        if not pin.isdigit():
            st.error("Enter valid PIN")
        else:
            user = find_user(acc, int(pin))

            if not user:
                st.error("❌ User not found")
            elif amount > user["balance"]:
                st.error("❌ Insufficient balance")
            else:
                user["balance"] -= amount
                save_data(data)
                st.success("✅ Withdrawal successful!")

# -------- DETAILS --------
elif menu == "Check Details":
    st.header("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        if not pin.isdigit():
            st.error("Enter valid PIN")
        else:
            user = find_user(acc, int(pin))

            if not user:
                st.error("❌ User not found")
            else:
                st.json(user)

# -------- UPDATE --------
elif menu == "Update Details":
    st.header("Update Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Load User"):
        if not pin.isdigit():
            st.error("Enter valid PIN")
        else:
            user = find_user(acc, int(pin))

            if user:
                st.session_state.user = user
            else:
                st.error("❌ User not found")

    if "user" in st.session_state:
        user = st.session_state.user

        new_name = st.text_input("New Name", value=user["name"])
        new_email = st.text_input("New Email", value=user["email"])
        new_pin = st.text_input("New PIN", value=str(user["pin"]))

        if st.button("Update Details"):
            user["name"] = new_name
            user["email"] = new_email

            if new_pin.isdigit() and len(new_pin) == 4:
                user["pin"] = int(new_pin)

            save_data(data)
            st.success("✅ Updated successfully!")

# -------- DELETE --------
elif menu == "Delete Account":
    st.header("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete Account"):
        if not pin.isdigit():
            st.error("Enter valid PIN")
        else:
            user = find_user(acc, int(pin))

            if not user:
                st.error("❌ User not found")
            else:
                data.remove(user)
                save_data(data)
                st.success("✅ Account deleted!")