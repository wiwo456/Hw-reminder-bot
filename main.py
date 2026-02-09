import json
import detector
import requests
from datetime import datetime



def main():
    print("The program has started ")

    with open ("config.json", "r") as f:
        config = json.load(f)
    
    webhook_url = config["discord_webhook"]
   


    delay_minutes = config["delay_minutes"]
    delay_seconds = delay_minutes * 60

    #this line will read the storage to see if there are any hw and it will send a message if found 
    with open ("storage.json", "r") as f:
        storage = json.load(f)

    reminded_hw = storage["reminded_hw"]
    
    homework = detector.detect_hw()

    if not homework:
        print ("You do not have any assignment due.......")
        return
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
            elif(days_left <=0):
                print("You missed the hw (Overdue). Write a mail.....")
            elif(days_left <=2):
                print("Do your homework.....")
            else:
                print("Your homework is due soon")
            print(" ")
            print ("=====================") 
            print(" New homework found ")
            print("Course:", hw['course'])
            print("Title:", hw["title"])
            print("Due:", hw["due"], hw["time"])
            print ( f"You have {days_left} days left")
            print("========================")

            
            reminded_hw.append(hw_id)
    
    #this line dumps the already reminded hw to the storage
    with open ("storage.json", "w") as f:
        json.dump(storage, f, indent = 4) #indent is to add spacing. 

    print("delay_minutes:", delay_minutes)
    print("delay_seconds:", delay_seconds)

if __name__ == "__main__":
    main()
