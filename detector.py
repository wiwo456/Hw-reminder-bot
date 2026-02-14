import requests
from ics import Calendar
from datetime import datetime
import json


def detect_hw():
    with open("config.json", "r") as f:
        config = json.load(f)

    ical_url = config["ical_url"]

    response = requests.get(ical_url)
    calendar = Calendar(response.text)

    homework_list = []

    now = datetime.now()

    for event in calendar.events:
        event_time = event.begin.to("local").naive

        if event_time < now:
            continue

        title = event.name.strip()

        due_date = event_time.strftime("%Y-%m-%d")
        due_time = event_time.strftime("%I:%M %p")

        homework_list.append({
            "title": title,
            "due": due_date,
            "time": due_time
        })

    return homework_list
