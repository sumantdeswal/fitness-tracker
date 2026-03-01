import json
import datetime
from enum import Enum
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import matplotlib.pyplot as plt


# ---------------- ENUM ----------------
class FitnessStatus(Enum):
    UNDERWEIGHT = "Underweight"
    NORMAL = "Normal"
    OVERWEIGHT = "Overweight"
    OBESE = "Obese"


# ---------------- USER CLASS ----------------
class User:
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height
        self.bmi = self.calculate_bmi()
        self.fitness_status = self.determine_fitness_status()

    def calculate_bmi(self):
        return round(self.weight / (self.height ** 2), 2)

    def determine_fitness_status(self):
        if self.bmi < 18.5:
            return FitnessStatus.UNDERWEIGHT
        elif 18.5 <= self.bmi < 25:
            return FitnessStatus.NORMAL
        elif 25 <= self.bmi < 30:
            return FitnessStatus.OVERWEIGHT
        else:
            return FitnessStatus.OBESE


# ---------------- DIET PLAN ----------------
class DietPlan:
    def __init__(self, filename):
        with open(filename) as f:
            self.plans = json.load(f)

    def get_plan(self, user, plan_type):
        plan_types = {
            "1": "weight_loss",
            "2": "weight_gain",
            "3": "healthy"
        }
        return self.plans[user.fitness_status.value][plan_types[plan_type]]


# ---------------- UTILITY FUNCTIONS ----------------
def log_data(file, data):
    with open(file, "a") as f:
        f.write(data + "\n")


def display_message(title, message):
    messagebox.showinfo(title, message)


def record_weight(user):
    weight = simpledialog.askfloat("Record Weight", "Enter your weight (kg):")
    if weight:
        user.weight = weight
        user.bmi = user.calculate_bmi()
        today = datetime.date.today()
        log_data("bmi_log.txt", f"{today},{user.bmi}")
        display_message("Success", f"Updated BMI: {user.bmi}")


def record_calories():
    calories = simpledialog.askinteger("Calories Intake", "Enter calories consumed:")
    if calories:
        today = datetime.date.today()
        log_data("calorie_log.txt", f"{today},{calories}")
        display_message("Success", "Calories recorded!")


def record_exercise():
    exercise = simpledialog.askstring("Exercise", "Enter exercise details:")
    if exercise:
        today = datetime.date.today()
        log_data("exercise_log.txt", f"{today},{exercise}")
        display_message("Success", "Exercise recorded!")


def view_data(file):
    try:
        with open(file, "r") as f:
            content = f.read()
        window = tk.Toplevel()
        window.title("Log Viewer")
        text_area = scrolledtext.ScrolledText(window, width=50, height=20)
        text_area.pack()
        text_area.insert(tk.END, content)
        text_area.config(state="disabled")
    except FileNotFoundError:
        display_message("Error", "No log found.")


def plot_data(file, y_label, title):
    try:
        dates = []
        values = []

        with open(file, "r") as f:
            for line in f:
                date, value = line.strip().split(",")
                dates.append(date)
                values.append(float(value))

        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, marker="o")
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel(y_label)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        display_message("Error", "No log found.")


# ---------------- MAIN GUI ----------------
def main_gui():
    root = tk.Tk()
    root.title("Health and Fitness Guide")

    weight = simpledialog.askfloat("User Weight", "Enter your weight (kg):")
    height = simpledialog.askfloat("User Height", "Enter your height (m):")

    if weight and height:
        user = User(weight, height)
        diet_plan = DietPlan("diet_plans.json")

        display_message(
            "User Info",
            f"Your BMI: {user.bmi}\nStatus: {user.fitness_status.value}"
        )

        def get_diet_plan():
            plan_choice = simpledialog.askstring(
                "Diet Plan",
                "Choose:\n1. Weight Loss\n2. Weight Gain\n3. Healthy"
            )
            if plan_choice in ["1", "2", "3"]:
                plan = diet_plan.get_plan(user, plan_choice)
                display_message("Diet Plan", plan)
            else:
                display_message("Error", "Invalid choice")

        tk.Button(root, text="Get Diet Plan", command=get_diet_plan).pack(pady=5)
        tk.Button(root, text="Record Weight & BMI",
                  command=lambda: record_weight(user)).pack(pady=5)
        tk.Button(root, text="Record Calories",
                  command=record_calories).pack(pady=5)
        tk.Button(root, text="Record Exercise",
                  command=record_exercise).pack(pady=5)
        tk.Button(root, text="View BMI Log",
                  command=lambda: view_data("bmi_log.txt")).pack(pady=5)
        tk.Button(root, text="View Calorie Log",
                  command=lambda: view_data("calorie_log.txt")).pack(pady=5)
        tk.Button(root, text="Plot BMI",
                  command=lambda: plot_data("bmi_log.txt", "BMI", "BMI Over Time")).pack(pady=5)
        tk.Button(root, text="Plot Calories",
                  command=lambda: plot_data("calorie_log.txt", "Calories", "Calories Over Time")).pack(pady=5)
        tk.Button(root, text="Exit", command=root.destroy).pack(pady=5)

        root.mainloop()

    else:
        display_message("Error", "Invalid input.")


if __name__ == "__main__":
    main_gui()