from flask import Flask, request, jsonify, render_template
import threading
import time
from services.login_service import LoginService
from services.line_bot_handler import LineBotHandler
from services.repair_service import RepairService
from services.flex_builder import FlexBuilder
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load config
LOGIN_URL = os.getenv("LOGIN_URL")
USERNAME = os.getenv("LOGIN_USERNAME")
PASSWORD = os.getenv("LOGIN_PASSWORD")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
COMPANY_ID = 355

# Initialize services
login_service = LoginService(LOGIN_URL, USERNAME, PASSWORD)
login_service.authenticate()

line_bot = LineBotHandler(CHANNEL_ACCESS_TOKEN)
repair_service = RepairService(COMPANY_ID, login_service=login_service)

LINE_UID = None


def auto_send_message():
    global LINE_UID
    while True:
        if LINE_UID:
            line_bot.push_message(LINE_UID, "📢 แจ้งเตือนอัตโนมัติทุก 5 นาที")
        time.sleep(300)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook():
    global LINE_UID
    body = request.json
    events = body.get("events", [])

    for event in events:
        if "source" in event:
            LINE_UID = event["source"]["userId"]
            line_bot.get_profile(LINE_UID)

        if event.get("type") == "message":
            msg_type = event["message"]["type"]
            if msg_type == "text":
                user_text = event["message"]["text"]
                reply_token = event["replyToken"]

                if "ติดตามงานที่กำลังทำ" in user_text:
                    data = repair_service.get_in_progress(LINE_UID)
                    bubbles = FlexBuilder.build_report_card(data)
                    line_bot.send_flex_message(reply_token, bubbles, "ติดตามงานที่กำลังทำ")
                elif "ติดตามงานที่ปิดแล้ว" in user_text:
                    data = repair_service.get_completed(LINE_UID)
                    bubbles = FlexBuilder.build_report_card(data)
                    line_bot.send_flex_message(reply_token, bubbles, "ติดตามงานที่ปิดแล้ว")
                else:
                    line_bot.reply_message(reply_token, LINE_UID)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # threading.Thread(target=auto_send_message, daemon=True).start()
    app.run(port=5000, debug=True)
