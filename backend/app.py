from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

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

    else:
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

    connection.close()

    if user:
        return jsonify({
            "username": user[0],
            "balance": user[1],
            "currency": "USDT"
        })

    return jsonify({
        "message": "User not found"
    })
if __name__ == "__main__":
    app.run(debug=True)