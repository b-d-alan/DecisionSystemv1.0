"""
a program to aid in decision-making
"""
import csv
import time
import os 
from my_python_package_custom_package import my_module


def eisenhower_matrix(): 
    urgent = my_module.yn("is this task urgent?")
    important = my_module.yn("is this task important?")

    if urgent and important:
        decision = "Do it now."
    elif not urgent and important:
        decision = "Schedule a time to do it."
        call_when = yn("would you like me to helo you schedule a time?")
        if call_when:
            when()
    elif urgent and not important:
        decision = "Delegate it if possible."
    else:
        decision = "Eliminate it."
    print(decision)
    with


def when():
    duration = int(input("how long will it take to complete this task? (mins) "))
    

def read_logs():
    
print("how may i help you? ")
print("""1 - new task
          2 - pending tasks
          3 - read logs""")
while True:
    command = input("enter corresponding number: ").strip()
    if not command.isdigit():
        print("invalid input, please enter a number")
        continue
    if command =="1":