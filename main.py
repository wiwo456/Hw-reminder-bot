import json
import detector
import requests
import time
import storage
from reminder import process_reminders
from datetime import datetime


def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    webhook_url = config["discord_webhook"]
    blackboard_url = config["blackboard_url"]
    delay_minutes = config["delay_minutes"]
    delay_seconds = delay_minutes * 60

    storage_data = storage.load_storage()

    homework = detector.detect_hw()

    reminders = process_reminders(homework, storage_data)

    # 🔔 Only print if something is actually sent
    if reminders:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending {len(reminders)} reminder(s)")

    for hw in reminders:
        message = {
            "embeds": [
                {
                    "title": "📚 Homework Alert 🔔",
                    "description": f"**{hw['title']}**\n\n[Blackboard]({blackboard_url})",
                    "color": hw["color"],
                    "fields": [
                        {
                            "name": "Due Date",
                            "value": f"{hw['due']} {hw['time']}",
                            "inline": True
                        },
                        {
                            "name": "Time Remaining",
                            "value": hw["time_text"],
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": "Sent by HW-Bot 🤖"
                    }
                }
            ]
        }

        requests.post(webhook_url, json=message)

    storage.save_storage(storage_data)

    return delay_seconds


if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Bot is running... 🚀\n")

    while True:
        try:
            delay = main()
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
            delay = 60

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sleeping for {delay//60} minutes...\n")
        time.sleep(delay)