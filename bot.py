import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from agent import AssetRequestAgent
from database import (
    init_db,
    save_request,
    get_all_requests,
)

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# Store one agent per user
user_sessions = {}


# -----------------------------
# Gemini Function
# -----------------------------
def extract_details(user_message):

    prompt = f"""
You are an Asset Request Assistant.

Extract the following fields from the user's message.

Return ONLY JSON in this format:

{{
"employee_id":"",
"asset_type":"",
"asset_name":"",
"justification":""
}}

If any value is missing, keep it empty.

User Message:
{user_message}
"""

    response = model.generate_content(prompt)

    try:
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)

    except Exception:
        return None


# -----------------------------
# /start
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    agent = AssetRequestAgent()

    user_sessions[user_id] = agent

    await update.message.reply_text(
        "🤖 Welcome to Asset Request Bot.\n\n"
        "Please type your request naturally.\n\n"
        "Example:\n"
        "'My Employee ID is EMP1001. "
        "I need a Dell Latitude Laptop for AI Development.'"
    )


# -----------------------------
# Handle Messages
# -----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    message = update.message.text

    if user_id not in user_sessions:
        user_sessions[user_id] = AssetRequestAgent()

    agent = user_sessions[user_id]

    extracted = extract_details(message)

    if extracted is None:
        await update.message.reply_text(
            "❌ Unable to understand your request."
        )
        return

    # Fill Slots Automatically

    for slot, value in extracted.items():

        if value:
            agent.slot_manager.update_slot(slot, value)

    result = agent.generate_request()

    if isinstance(result, dict):

        save_request(result)

        await update.message.reply_text(
            f"""
✅ Asset Request Submitted

Request ID : {result['request_id']}

Employee ID : {result['employee_id']}

Asset Type : {result['asset_type']}

Asset Name : {result['asset_name']}

Justification : {result['justification']}

Status : {result['status']}
"""
        )

        del user_sessions[user_id]

    else:

        await update.message.reply_text(result)


# -----------------------------
# /requests
# -----------------------------
async def requests_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    rows = get_all_requests()

    if not rows:
        await update.message.reply_text("No requests found.")
        return

    message = "📋 Asset Requests\n\n"

    for row in rows:

        message += (
            f"Request ID : {row['request_id']}\n"
            f"Employee ID : {row['employee_id']}\n"
            f"Asset Name : {row['asset_name']}\n"
            f"Status : {row['status']}\n\n"
        )

    await update.message.reply_text(message)


# -----------------------------
# Main Function
# -----------------------------
def main():

    if not TOKEN:
        print("Telegram Token Missing")
        return

    if not GEMINI_API_KEY:
        print("Gemini API Key Missing")
        return

    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("requests", requests_cmd))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🚀 Asset Request Bot Started with Gemini AI...")

    app.run_polling()


if __name__ == "__main__":
    main()