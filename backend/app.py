from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = "database/click2earn.db"


@app.route("/")
def home():
    return "🚀 Click2Earn Backend Running!"


@app.route("/api/user")
def user():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT telegram_id, username, balance FROM users LIMIT 1"
    )

    data = cursor.fetchone()

    connection.close()

    if data:
        return jsonify({
            "telegram_id": data[0],
            "username": data[1],
            "balance": data[2],
            "currency": "USDT"
        })

    return jsonify({
        "message": "No user found",
        "balance": 0,
        "currency": "USDT"
    })


@app.route("/api/user/<telegram_id>")
def get_user(telegram_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username, balance FROM users WHERE telegram_id=?",
        (telegram_id,)
    )

    user = cursor.fetchone()

    if user:
        connection.close()
        return jsonify({
            "username": user[0],
            "balance": user[1],
            "currency": "USDT"
        })

    # Auto create new user
    cursor.execute(
        """
        INSERT INTO users (telegram_id, username, balance)
        VALUES (?, ?, ?)
        """,
        (telegram_id, "New User", 0)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "username": "New User",
        "balance": 0,
        "currency": "USDT"
    })
@app.route("/api/reward/<telegram_id>", methods=["POST"])
def reward(telegram_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE users SET balance = balance + 0.10 WHERE telegram_id=?",
        (telegram_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "reward": 0.001
    })

@app.route("/api/daily_bonus/<telegram_id>", methods=["POST"])
def daily_bonus(telegram_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE users SET balance = balance + 5 WHERE telegram_id=?",
        (telegram_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "bonus": 5.00
    })

@app.route("/api/withdraw", methods=["POST"])
def withdraw():

    from flask import request

    data = request.json

    telegram_id = data["telegram_id"]
    method = data["method"]
    address = data["address"]
    amount = float(data["amount"])

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Check balance
    cursor.execute(
        "SELECT balance FROM users WHERE telegram_id=?",
        (telegram_id,)
    )

    user = cursor.fetchone()

    if not user:
        connection.close()
        return jsonify({
            "success": False,
            "message": "User not found"
        })

    if user[0] < amount:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Insufficient balance"
        })


    # Deduct balance
    cursor.execute(
        "UPDATE users SET balance = balance - ? WHERE telegram_id=?",
        (amount, telegram_id)
    )


    # Save withdrawal request
    cursor.execute(
        """
        INSERT INTO withdrawals
        (telegram_id, method, address, amount)
        VALUES (?, ?, ?, ?)
        """,
        (telegram_id, method, address, amount)
    )


    connection.commit()
    connection.close()


    return jsonify({
        "success": True,
        "message": "Withdrawal request submitted"
    })

@app.route("/api/admin/withdrawals")
def admin_withdrawals():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, telegram_id, method, address, amount, status
        FROM withdrawals
        ORDER BY id DESC
        """
    )

    data = cursor.fetchall()

    connection.close()

    withdrawals = []

    for row in data:
        withdrawals.append({
            "id": row[0],
            "telegram_id": row[1],
            "method": row[2],
            "address": row[3],
            "amount": row[4],
            "status": row[5]
        })

    return jsonify(withdrawals)

@app.route("/api/admin/withdraw/<int:withdraw_id>/<action>", methods=["POST"])
def update_withdraw(withdraw_id, action):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if action == "approve":

        cursor.execute(
            "UPDATE withdrawals SET status='Approved' WHERE id=?",
            (withdraw_id,)
        )

    elif action == "reject":

        cursor.execute(
            "UPDATE withdrawals SET status='Rejected' WHERE id=?",
            (withdraw_id,)
        )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "status": action
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )