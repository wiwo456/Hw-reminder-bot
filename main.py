import json
import detector
import requests
import time 
import storage
from datetime import datetime




def main():
    print("The program has started ")

    with open ("config.json", "r") as f:
        config = json.load(f)
    
    webhook_url = config["discord_webhook"]
   


    delay_minutes = config["delay_minutes"]
    delay_seconds = delay_minutes * 60

    storage_data = storage.load_storage()
    reminded_hw = storage_data["reminded_hw"]
    
    homework = detector.detect_hw()

    if not homework:
        print ("You do not have any assignment due.......")
        return delay_seconds
    else:
        print("\nHomework exits will notify you....\n")
       
        for hw in homework:
            hw_id = hw["course"] + " | " + hw["title"] + " | " + hw["due"] + " | " + hw["time"]
            
            
            if hw_id in reminded_hw: #this line does the skip of old hw
                continue
            
            due_string = hw["due"] + " " + hw["time"]
            due_datetime = datetime.strptime(due_string, "%Y-%m-%d %I:%M %p")
            now = datetime.now()
            hours_left = (due_datetime - now).total_seconds()/3600
            days_left = round(hours_left / 24, 2)

            
            
            if (days_left > 5):
                continue
            if (days_left<0):
                time_status = "Overdue."
            elif (days_left<1):
                hours = int(hours_left)
                time_status = f"{hours} hours left."
            elif(days_left<2):
                time_status = "Due tomorrow."
            else:
                time_status = f"{days_left} days left."
            
            
            color = 65280

            if (days_left <=0):
                color = 16711680
            elif (days_left <=2):
                color = 16753920

            message = {
                "embeds": [
                    {
                        "title" : "📚 Homework alert 🔔",
                        "description": f"⤍{hw['title']}⤎",
                        "color": color,
                        "fields": [
                            {
                                "name": "Course",
                                "value": hw['course'],
                                "inline": True
                            },
                            {
                                "name": "Due Date",
                                "value": f"{hw['due']} {hw['time']}",
                                "inline": True
                            },
                            {
                                "name": "Time Remaining",
                                "value": time_status,
                                "inline": False
                            }
                        ],
                     
                            "footer":{
                                "text": "Sent by HW-Bot 🤖"
                            }

                        
                    }
                ]
            }

            requests.post(webhook_url, json=message)

            
            reminded_hw.append(hw_id)
    
    storage.save_storage(storage_data)

    print("delay_minutes:", delay_minutes)
    print("delay_seconds:", delay_seconds)
    return delay_seconds
if __name__ == "__main__":
    while True:
        try:
            delay = main()
        except Exception as e:
            print("There is some issue: ", e)
            delay = 60 # you can change this according what you prefer the program to start again, i added 1 minute. 
        time.sleep(delay)
