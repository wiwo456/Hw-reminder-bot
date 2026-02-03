import json
import detector

def main():
    print("The program has started ")

    with open ("config.json", "r") as f:
        config = json.load(f)

    delay_minutes = config["delay_minutes"]
    delay_seconds = delay_minutes * 60

    found = detector.detect_hw()
    print("Homework found? ", found)
    
    print("delay_minutes:", delay_minutes)
    print("delay_seconds:", delay_seconds)

if __name__ == "__main__":
    main()
