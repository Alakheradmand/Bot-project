Telegram receipt-check bot with Join Button (python-telegram-bot v20+)

This bot:

1. Receives payment screenshot from user

2. Forwards it to admin

3. Admin approves or rejects

4. On approve: bot sends the user's invite link

import logging from telegram import Update from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

=== CONFIG ===

BOT_TOKEN = "YOUR_BOT_TOKEN" ADMIN_ID = 123456789  # replace with your Telegram user ID CHANNEL_ID = -1001234567890  # your private channel ID JOIN_BUTTON_TEXT = "ورود به کانال ویژه ❤️"  # unique invite per user

logging.basicConfig(level=logging.INFO)

Temporary memory for pending approvals

pending = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "سلام ❤️\nاسکرین‌شات پرداخت رو اینجا ارسال کن تا بررسی بشه." )

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.message.from_user file_id = update.message.photo[-1].file_id

# Save pending with user id
pending[user.id] = file_id

# Forward to admin
await context.bot.send_message(ADMIN_ID, f"درخواست جدید از: {user.full_name} (ID: {user.id})")
await context.bot.send_photo(ADMIN_ID, file_id)
await context.bot.send_message(ADMIN_ID, f"برای تایید: /approve_{user.id}\nبرای رد: /reject_{user.id}")

await update.message.reply_text("رسید دریافت شد 🌿 در حال بررسی هستیم…")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE): cmd = update.message.text user_id = int(cmd.split("_", 1)[1])

if user_id in pending:
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(JOIN_BUTTON_TEXT, url=f"https://t.me/c/{str(CHANNEL_ID)[4:]}")]])
await context.bot.send_message(user_id, "پرداخت تایید شد ❤️", reply_markup=keyboard ❤️\nاین هم لینک ورود شما:\n{INVITE_LINK}")
    del pending[user_id]
    await update.message.reply_text("تایید شد ✨")
else:
    await update.message.reply_text("درخواستی یافت نشد.")

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE): cmd = update.message.text user_id = int(cmd.split("_", 1)[1])

if user_id in pending:
    await context.bot.send_message(user_id, "پرداخت تایید نشد ❌ لطفاً دوباره بررسی کن.")
    del pending[user_id]
    await update.message.reply_text("رد شد ❌")
else:
    await update.message.reply_text("درخواستی نبود.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.PHOTO, receive_photo)) app.add_handler(CommandHandler("approve", approve)) app.add_handler(CommandHandler("reject", reject))

if name == "main": app.run_polling()
