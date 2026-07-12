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
        "UPDATE users SET balance = balance + 0.001 WHERE telegram_id=?",
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
        "UPDATE users SET balance = balance + 0.01 WHERE telegram_id=?",
        (telegram_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "bonus": 0.01
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )