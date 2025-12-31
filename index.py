"""
Decision System v1.1 - Aid in task prioritization and scheduling
"""
import csv
import json
import os
from datetime import datetime, timedelta
from my_python_package_custom_package import my_module

LOG_FILE = "logs.csv"
USER_FILE = "user_info.json"

# ---------- Initialization ----------
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "sr_no", "date", "time", "task", "duration",
            "urgent", "important", "decision", "timestamp",
            "completion", "remarks"
        ])

if not os.path.exists(USER_FILE):
    sleep_time = my_module.gettime("What time do you go to bed?")
    wake_time = my_module.gettime("What time do you wake up?")
    school_start = my_module.gettime("What time do you leave for school?")
    school_end = my_module.gettime("What time do you come home?")
    with open(USER_FILE, "w") as f:
        json.dump({
            "sleep_time": sleep_time,
            "wake_time": wake_time,
            "school_start": school_start,
            "school_end": school_end
        }, f)

# ---------- Logging ----------
def log(task, duration=None, urgent="", important="", decision="", completion="pending", remarks=""):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    timestamp = now.isoformat()

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", newline="") as f:
            sr_no = sum(1 for _ in f)  # includes header
            if sr_no > 0:
                sr_no -= 1
            sr_no += 1
    else:
        sr_no = 1

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            sr_no, date_str, time_str, task, duration,
            urgent, important, decision, timestamp,
            completion, remarks
        ])

# ---------- Scheduling ----------
def when(duration):
    with open(USER_FILE, "r") as f:
        user_info = json.load(f)
    wake_time = datetime.strptime(user_info["wake_time"], "%H:%M")
    sleep_time = datetime.strptime(user_info["sleep_time"], "%H:%M")
    school_start = datetime.strptime(user_info["school_start"], "%H:%M")
    school_end = datetime.strptime(user_info["school_end"], "%H:%M")

    slots = [
        (wake_time, school_start),
        (school_end, sleep_time)
    ]

    busy_slots = []
    try:
        with open(LOG_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["date"] == datetime.now().strftime("%Y-%m-%d"):
                    start = datetime.strptime(row["time"], "%H:%M")
                    end = start + timedelta(minutes=int(row["duration"]))
                    busy_slots.append((start, end))
    except FileNotFoundError:
        pass

    for slot_start, slot_end in slots:
        candidate_start = slot_start
        while candidate_start + timedelta(minutes=duration) <= slot_end:
            overlap = False
            for busy_start, busy_end in busy_slots:
                if candidate_start < busy_end and candidate_start + timedelta(minutes=duration) > busy_start:
                    overlap = True
                    candidate_start = busy_end
                    break
            if not overlap:
                suggested_time = candidate_start.strftime("%H:%M")
                print(f"Suggested time for this task: {suggested_time}")
                return suggested_time
            candidate_start += timedelta(minutes=1)

    print("No available slot today. Consider another day.")
    return None

# ---------- Eisenhower Matrix ----------
def eisenhower_matrix(task, duration):
    urgent = my_module.yn("Is this task urgent?")
    important = my_module.yn("Is this task important?")

    if urgent and important:
        decision = "Do it now."
        suggested_time = ""
    elif not urgent and important:
        decision = "Schedule a time to do it."
        call_when = my_module.yn("Would you like me to help you schedule a time?")
        if call_when:
            suggested_time = when(duration)
        else:
            suggested_time = ""
    elif urgent and not important:
        decision = "Delegate it if possible."
        suggested_time = ""
    else:
        decision = "Eliminate it."
        suggested_time = ""

    log(
        task=task,
        duration=duration,
        urgent=urgent,
        important=important,
        decision=decision,
        remarks=suggested_time
    )

    print(f"Decision: {decision}")
    if suggested_time:
        print(f"Suggested time: {suggested_time}")

# ---------- Read Logs ----------
def read_logs(date=None):
    results = []
    with open(LOG_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if date is None or row["date"] == date:
                results.append(row)
    return results

# ---------- Pending Tasks with Mark Completed ----------
def pending_tasks():
    logs = read_logs()
    pending = [row for row in logs if row["completion"].lower() != "done"]
    if not pending:
        print("No pending tasks.")
        return
    print("Pending tasks:")
    for row in pending:
        print(f"{row['sr_no']}. {row['task']} ({row['decision']}) - Duration: {row['duration']} mins")
    
    mark_done = my_module.yn("Do you want to mark any task as completed?")
    if mark_done:
        sr_input = input("Enter the sr_no of the task you completed: ").strip()
        if not sr_input.isdigit():
            print("Invalid input. Must be a number.")
            return
        sr_no_to_mark = int(sr_input)

        updated_rows = []
        with open(LOG_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["sr_no"]) == sr_no_to_mark:
                    row["completion"] = "done"
                    print(f"Task '{row['task']}' marked as completed.")
                updated_rows.append(row)
        
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

# ---------- Change Settings ----------
def change_settings():
    with open(USER_FILE, "r") as f:
        user_info = json.load(f)
    print("Current settings:")
    print(user_info)
    wake_time = my_module.gettime("New wake-up time? (HH:MM)")
    sleep_time = my_module.gettime("New sleep time? (HH:MM)")
    school_start = my_module.gettime("New school start time? (HH:MM)")
    school_end = my_module.gettime("New school end time? (HH:MM)")
    user_info.update({
        "wake_time": wake_time,
        "sleep_time": sleep_time,
        "school_start": school_start,
        "school_end": school_end
    })
    with open(USER_FILE, "w") as f:
        json.dump(user_info, f)
    print("Settings updated.")

# ---------- Main Menu ----------
def main_menu():
    while True:
        print("\nHow may I help you?")
        print("""1 - New task
2 - Pending tasks
3 - Show logs
4 - Change settings
5 - Quit""")
        command = input("Enter corresponding number: ").strip()
        if not command.isdigit():
            print("Invalid input, please enter a number")
            continue
        if command == "1":
            task = input("What is the task? ")
            duration = int(input("How long will it take? (mins) "))
            if duration <= 15:
                decision = "Do it now."
                print(decision)
                log(task=task, duration=duration, urgent=True, important=True, decision=decision)
            else:
                eisenhower_matrix(task, duration)
        elif command == "2":
            pending_tasks()
        elif command == "3":
            date_filter = input("Enter date to filter logs (YYYY-MM-DD) or leave blank for all: ").strip()
            logs = read_logs(date_filter if date_filter else None)
            if not logs:
                print("No logs found.")
            else:
                for row in logs:
                    print(f"{row['sr_no']}. {row['task']} | Duration: {row['duration']} | Decision: {row['decision']} | Completion: {row['completion']} | Remarks: {row['remarks']}")
        elif command == "4":
            change_settings()
        elif command == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid command.")

# Run
if __name__ == "__main__":
    main_menu()
