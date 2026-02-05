import json
import detector

def main():
    print("The program has started ")

    with open ("config.json", "r") as f:
        config = json.load(f)

    delay_minutes = config["delay_minutes"]
    delay_seconds = delay_minutes * 60

    with open ("storage.json", "r") as f:
        storage = json.load(f)

    homework = detector.detect_hw()
    
    if not homework:
        print ("You do not have any assignment due.......")
        return
    else:
        print("\nHomework exits will notify you....\n")
        print("\nHomework Found:\n")

        for hw in homework:
            print("Course:", hw['course'])
            print("Title:", hw["title"])
            print("Due:", hw["due"])
            print("========================")

    print("delay_minutes:", delay_minutes)
    print("delay_seconds:", delay_seconds)

if __name__ == "__main__":
    main()
