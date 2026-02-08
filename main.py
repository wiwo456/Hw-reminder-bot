import json
import detector
from datetime import datetime


def main():
    print("The program has started ")

    with open ("config.json", "r") as f:
        config = json.load(f)

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
            
            print(" New homework found ")
            print("Course:", hw['course'])
            print("Title:", hw["title"])
            print("Due:", hw["due"], hw["time"])
            print("========================")

            reminded_hw.append(hw_id)
    
    #this line dumps the already reminded hw to the storage
    with open ("storage.json", "w") as f:
        json.dump(storage, f, indent = 4) #indent is to add spacing. 

    print("delay_minutes:", delay_minutes)
    print("delay_seconds:", delay_seconds)

if __name__ == "__main__":
    main()
