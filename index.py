"""
a program to aid in decision-making
"""
import csv
import json
import time
import os 
from my_python_package_custom_package import my_module

if not os.path.exists("logs.csv"):
    with open("logs.csv","w") as file :
        writer = csv.writer(file)
        writer.writerow(["sr_no","date","time","task","duration","decision","timestamp","completion","remarks"])

if not os.path.exists("user_info.json"):
    sleep_time = my_module.gettime("what time do you go to bed?")
    wake_time = my_module.gettime("what time do you wake up?")
    school_start = my_module.gettime("what time do you leave for school?")
    school_end = my_module.gettime("what time do you come home?")    
    with open("user_info.json","w") as file:
        json.dump({"sleep_time":sleep_time,"wake_time":wake_time,"school_start":school_start,"school_end":school_end},file)


def eisenhower_matrix(): 
    urgent = my_module.yn("is this task urgent?")
    important = my_module.yn("is this task important?")

    if urgent and important:
        decision = "Do it now."
    elif not urgent and important:
        decision = "Schedule a time to do it."
        call_when = my_module.yn("would you like me to help you schedule a time?")
        if call_when:
            when()
    elif urgent and not important:
        decision = "Delegate it if possible."
    else:
        decision = "Eliminate it."
    print(decision)
    log()


def when():
    duration = int(input("how long will it take to complete this task? (mins) "))
    

def read_logs(date):
    results=[]
    with open("logs.csv","r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"] == date:
                results.append(row)
    return results

def log():
    pass

  
print("how may i help you? ")
print("""1 - new task
          2 - pending tasks
          3 - show logs
          4 - change settings
          5 - quit""")
while True:
    command = input("enter corresponding number: ").strip()
    if not command.isdigit():
        print("invalid input, please enter a number")
        continue
    if command =="1":
        task = input("what is the task? ")
        duration = int(input("how long will it take?(mins)"))
        if duration <= 15:
            decision="Do it now."
            print(decision)
            log()
        else:
            eisenhower_matrix()
    if command =="2":
        pass
    if command =="3":
        pass
    if command =="4":
        pass
    if command =="5":
        print("goodbye!")
        break

