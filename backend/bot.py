from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sqlite3

BOT_TOKEN = "8737030958:AAE65Z-NkXZiqfoBPvxBJeAuX1NHJhL8WnY"

DATABASE = "database/click2earn.db"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (telegram_id, username)
        VALUES (?, ?)
        """,
        (str(user.id), user.username)
    )

    connection.commit()
    connection.close()

    await update.message.reply_text(
        "🚀 Welcome to Click2Earn!\n\nYour account has been created."
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))


print("Click2Earn Bot Running...")

app.run_polling()