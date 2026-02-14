from datetime import datetime, timedelta


def process_reminders(hw_list, storage):
    mem = storage["reminded_hw"]
    new_mem = {}

    now = datetime.now()

    if now.hour < 8:
        storage["reminded_hw"] = mem
        return []

    valid = []

    for hw in hw_list:
        hw_id = hw["title"] + " | " + hw["due"] + " | " + hw["time"]

        due = datetime.strptime(
            hw["due"] + " " + hw["time"],
            "%Y-%m-%d %I:%M %p"
        )

        hours_left = (due - now).total_seconds() / 3600
        days_left = hours_left / 24

        if due.date() < now.date():
            continue

        if days_left <= 5:
            hw["hours_left"] = hours_left
            hw["days_left"] = days_left
            valid.append(hw)

    valid.sort(key=lambda x: datetime.strptime(
        x["due"] + " " + x["time"],
        "%Y-%m-%d %I:%M %p"
    ))

    send = []
    limit = 2

    for hw in valid:
        if len(send) >= limit:
            break

        hw_id = hw["title"] + " | " + hw["due"] + " | " + hw["time"]

        hours_left = hw["hours_left"]
        days_left = hw["days_left"]

        if days_left < 1:
            hw["time_text"] = f"{round(hours_left,1)} hours left."
        elif days_left < 2:
            hw["time_text"] = "Due tomorrow."
        else:
            hw["time_text"] = f"{round(days_left,1)} days left."

        color = 65280

        if days_left <= 1:
            color = 16711680
        elif days_left <= 2:
            color = 16753920

        hw["color"] = color

        if hw_id not in mem:
            send.append(hw)
            new_mem[hw_id] = now.strftime("%Y-%m-%d %H:%M:%S")
        else:
            last = datetime.strptime(mem[hw_id], "%Y-%m-%d %H:%M:%S")
            if now - last >= timedelta(hours=24):
                send.append(hw)
                new_mem[hw_id] = now.strftime("%Y-%m-%d %H:%M:%S")
            else:
                new_mem[hw_id] = mem[hw_id]

    storage["reminded_hw"] = new_mem

    return send
