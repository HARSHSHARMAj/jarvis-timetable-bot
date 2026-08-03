import json, datetime, urllib.request, urllib.parse, os

def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=15)
        return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def main():
    with open("telegram_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    with open("timetable_config.json", "r", encoding="utf-8") as f:
        tasks = json.load(f)

    BOT_TOKEN = config.get("bot_token", "8936644850:AAEpq7L7CUMWfdUNbX_Om23Po5JwBj8fOLM")
    CHAT_ID = str(config.get("chat_id", "7974926299"))

    # IST = UTC + 5:30
    now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_time = now_ist.strftime("%H:%M")
    current_day  = now_ist.strftime("%A").lower()

    print(f"IST: {current_time} | Day: {current_day}")

    sent = 0
    for task in tasks:
        if not task.get("active", True):
            continue
        days = task.get("days", ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"])
        if current_day not in days:
            continue
        if task.get("time","") == current_time:
            name = task.get("name","Task")
            note = task.get("note","")
            msg = (
                f"\U0001F6A8 <b>JARVIS ALERT - BOSS!</b>\n\n"
                f"\u23F0 <b>Time:</b> {task['time']}\n"
                f"\U0001F4DA <b>Task:</b> {name}\n"
                f"\U0001F4DD <b>Note:</b> {note if note else 'Shuru karo Boss!'}\n\n"
                f"\U0001F525 <i>IBPS PO 2025 - Aaj ka target complete karo!</i>"
            )
            print(f"Sending: {name} @ {task['time']}")
            send_telegram(BOT_TOKEN, CHAT_ID, msg)
            sent += 1

    print(f"Done. Sent: {sent} alert(s).")

if __name__ == "__main__":
    main()
