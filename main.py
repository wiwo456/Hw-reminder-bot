#this is the code where main part of the code is going on 
import json
import detector
import requests
import time
import storage
from reminder import process_reminders


def main():
    print("The program has started")

    with open("config.json", "r") as f:
        config = json.load(f)

    webhook_url = config["discord_webhook"]
    delay_minutes = config["delay_minutes"]
    delay_seconds = delay_minutes * 60

    storage_data = storage.load_storage()

    homework = detector.detect_hw()

    reminders = process_reminders(homework, storage_data)

    
    for hw in reminders:
        message = {
            "embeds": [
                {
                    "title": "📚 Homework Alert 🔔",
                    "description": f"**{hw['title']}**",
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

    print("Sleeping for", delay_minutes, "minutes\n")
    return delay_seconds


if __name__ == "__main__":
    while True:
        try:
            delay = main()
        except Exception as e:
            print("There is some issue:", e)
            delay = 60
        time.sleep(delay)
