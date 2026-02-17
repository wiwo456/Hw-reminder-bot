Hw-Remainder-Bot 🤖

This is a python based hw remainder bot that reads your homework from blackboard and sends it to discord as remainders to do the homework.

Features:
1. Detects upcoming assignments by blackboard calendar.
2. Sends assignments remainders to discord.
3. Shows you the due date and time.
4. Clickable link that directly takes you to blackboard.

Setup:
Installation required:
1. pip install requests
2. pip install ics

Config:

Create a file: config.json
```json 
{
  "discord_webhook": "your discord webhook link",
  "delay_minutes": 10, #For this you can choose your own time in order to create the notification gap between two assignments.
  "ical_url": "your calendar(ICAL) url ",
  "blackboard_url": "https://your-school-blackboard.edu"
}
```
Create a file: storage.json (this one is for storage of assignments)
```json
{
  "reminded_hw":{
   }
}
```
To run:

```
python main.py
```
