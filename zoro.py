import json
import os
import datetime
import random
import matplotlib.pyplot as plt
import requests

# 🗡️ Zoro - Daily Goal Tracker with Quotes & Graphs

# 📁 File to store goal data
data_file = "goals.json"

# 💬 Offline quotes as fallback
offline_quotes = [
    "Believe in yourself and all that you are.",
    "Discipline is the bridge between goals and accomplishment.",
    "Push yourself, because no one else is going to do it for you.",
    "Wake up with determination. Go to bed with satisfaction.",
    "You don’t have to be extreme, just consistent."
]

def get_daily_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            quote = data[0]["q"]
            author = data[0]["a"]
            return f"💬 Quote of the Day: \"{quote}\" — {author}"
        else:
            return random.choice(offline_quotes)
    except:
        return random.choice(offline_quotes)

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

def log_goals():
    date_str = str(datetime.date.today())
    data = load_data()

    print("\n📅 Today is:", date_str)
    print(get_daily_quote())

    tasks = []
    print("\n📝 Enter your goals for today:")
    while True:
        task = input("👉 Task (press Enter to stop): ").strip()
        if not task:
            break
        if ("python.exe" in task.lower() or task.endswith(".py") or task.startswith("&")):
            print("⚠️ Ignored suspicious input. Please enter an actual goal.")
            continue
        tasks.append({"task": task, "done": False})

    if tasks:
        data[date_str] = tasks
        save_data(data)
        print("\n✅ Your goals have been saved successfully!")
    else:
        print("⚠️ No tasks entered.")

def complete_goals():
    date_str = str(datetime.date.today())
    data = load_data()
    if date_str not in data:
        print("\n📭 No goals found for today. Try logging them first!")
        return

    print("\n📋 Your goals for today:")
    for i, task in enumerate(data[date_str]):
        status = "✅" if task["done"] else "❌"
        print(f"[{i+1}] {status} {task['task']}")

    choices = input("\n✔️ Enter the numbers of the goals you completed (comma-separated): ").strip()
    try:
        indexes = []
        for c in choices.split(","):
            c = c.strip()
            if c.isdigit():
                indexes.append(int(c) - 1)
        updated = False
        for idx in indexes:
            if 0 <= idx < len(data[date_str]):
                data[date_str][idx]["done"] = True
                updated = True
        if updated:
            save_data(data)
            print("🎉 Great job! Selected goals marked as completed!")
        else:
            print("⚠️ No valid selections made.")
    except:
        print("⚠️ Please enter valid numbers.")

def view_progress():
    data = load_data()
    dates = []
    completion = []

    for date, tasks in sorted(data.items()):
        if tasks:
            total = len(tasks)
            done = sum(1 for t in tasks if t["done"])
            percent = (done / total) * 100
            dates.append(date)
            completion.append(percent)

    if dates:
        plt.figure(figsize=(10, 5))
        plt.plot(dates, completion, marker='o', color='gold')
        plt.title("📈 Zoro - Goal Completion Trend")
        plt.xlabel("📅 Date")
        plt.ylabel("✅ % Completed")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()
    else:
        print("📭 No data available to display.")

def main():
    while True:
        print("\n🗡️ Welcome to Zoro - Track Goals Like a Warrior 🗡️")
        print("1️⃣ Log Today’s Goals")
        print("2️⃣ Mark a Goal as Completed")
        print("3️⃣ View Progress Graph")
        print("4️⃣ Exit 🚪")

        choice = input("\n📌 Choose an option (1-4): ").strip()
        if choice == '1':
            log_goals()
        elif choice == '2':
            complete_goals()
        elif choice == '3':
            view_progress()
        elif choice == '4':
            print("\n👋 Goodbye and keep slicing through those goals! ⚔️")
            break
        else:
            print("⚠️ Invalid option. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
