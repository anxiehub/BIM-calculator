import customtkinter as ctk
import os
import json
import webbrowser

# Настройка темы и стиля
ctk.set_appearance_mode("System")  # "Light" или "Dark"
ctk.set_default_color_theme("blue")

# Путь для сохранения данных веса
WEIGHT_FILE = "weight_data.json"

def load_weight_data():
    if os.path.exists(WEIGHT_FILE):
        with open(WEIGHT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"dates": [], "weights": [], "fat_percentages": []}

def save_weight_data(data):
    with open(WEIGHT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # Convert height to meters
        bmi = weight / (height ** 2)
        result = ""
        if bmi < 18.5:
            result = "Недостаточный вес"
        elif 18.5 <= bmi < 24.9:
            result = "Норма"
        elif 25 <= bmi < 29.9:
            result = "Избыточный вес"
        else:
            result = "Ожирение"
        bmi_result_label.configure(text=f"Ваш ИМТ: {bmi:.2f} ({result})")
    except ValueError:
        ctk.messagebox.show_error("Ошибка", "Введите корректные данные для веса и роста.")

def calculate_kbju():
    try:
        weight = float(weight_entry_kbju.get())
        age = int(age_entry.get())
        activity = activity_var.get()
        sex = sex_var.get()

        if sex == "Мужчина":
            bmr = 10 * weight + 6.25 * float(height_entry_kbju.get()) - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * float(height_entry_kbju.get()) - 5 * age - 161

        if activity == "Минимальная":
            bmr *= 1.2
        elif activity == "Низкая":
            bmr *= 1.375
        elif activity == "Средняя":
            bmr *= 1.55
        elif activity == "Высокая":
            bmr *= 1.725
        else:
            bmr *= 1.9

        proteins = bmr * 0.3 / 4
        fats = bmr * 0.25 / 9
        carbs = bmr * 0.45 / 4

        kbju_result_label.configure(
            text=f"Калории: {bmr:.0f}\nБелки: {proteins:.0f} г\nЖиры: {fats:.0f} г\nУглеводы: {carbs:.0f} г"
        )
    except ValueError:
        ctk.messagebox.show_error("Ошибка", "Введите корректные данные.")

def open_github(event):
    webbrowser.open_new("https://github.com/anxiehub")

# Создание основного окна
root = ctk.CTk()
root.title("Калькулятор ИМТ и КБЖУ")
root.geometry("360x640")
root.resizable(False, False)

# Создание вкладок
tab_view = ctk.CTkTabview(root)
tab_view.pack(expand=True, fill="both")

# Вкладка для ИМТ
bmi_tab = tab_view.add("Калькулятор ИМТ")
ctk.CTkLabel(bmi_tab, text="Калькулятор ИМТ", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

bmi_result_label = ctk.CTkLabel(bmi_tab, text="", font=ctk.CTkFont(size=14))
bmi_result_label.pack(pady=5)

frame_bmi = ctk.CTkFrame(bmi_tab)
frame_bmi.pack(pady=10, padx=10, fill="both", expand=True)

weight_label = ctk.CTkLabel(frame_bmi, text="Вес (кг):")
weight_label.pack(pady=5)
weight_entry = ctk.CTkEntry(frame_bmi, width=200, height=40, font=ctk.CTkFont(size=14))
weight_entry.pack(pady=5)

height_label = ctk.CTkLabel(frame_bmi, text="Рост (см):")
height_label.pack(pady=5)
height_entry = ctk.CTkEntry(frame_bmi, width=200, height=40, font=ctk.CTkFont(size=14))
height_entry.pack(pady=5)

bmi_button = ctk.CTkButton(frame_bmi, text="Рассчитать ИМТ", command=calculate_bmi, width=200, height=40, font=ctk.CTkFont(size=14))
bmi_button.pack(pady=10)

# Вкладка для КБЖУ
kbju_tab = tab_view.add("Калькулятор КБЖУ")
ctk.CTkLabel(kbju_tab, text="Калькулятор КБЖУ", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

kbju_result_label = ctk.CTkLabel(kbju_tab, text="", font=ctk.CTkFont(size=14))
kbju_result_label.pack(pady=5)

frame_kbju = ctk.CTkFrame(kbju_tab)
frame_kbju.pack(pady=10, padx=10, fill="both", expand=True)

weight_label_kbju = ctk.CTkLabel(frame_kbju, text="Вес (кг):")
weight_label_kbju.pack(pady=5)
weight_entry_kbju = ctk.CTkEntry(frame_kbju, width=200, height=40, font=ctk.CTkFont(size=14))
weight_entry_kbju.pack(pady=5)

height_label_kbju = ctk.CTkLabel(frame_kbju, text="Рост (см):")
height_label_kbju.pack(pady=5)
height_entry_kbju = ctk.CTkEntry(frame_kbju, width=200, height=40, font=ctk.CTkFont(size=14))
height_entry_kbju.pack(pady=5)

age_label = ctk.CTkLabel(frame_kbju, text="Возраст:")
age_label.pack(pady=5)
age_entry = ctk.CTkEntry(frame_kbju, width=200, height=40, font=ctk.CTkFont(size=14))
age_entry.pack(pady=5)

sex_label = ctk.CTkLabel(frame_kbju, text="Пол:")
sex_label.pack(pady=5)
sex_var = ctk.StringVar(value="Мужчина")
sex_menu = ctk.CTkOptionMenu(frame_kbju, variable=sex_var, values=["Мужчина", "Женщина"], width=200, height=40, font=ctk.CTkFont(size=14))
sex_menu.pack(pady=5)

activity_label = ctk.CTkLabel(frame_kbju, text="Активность:")
activity_label.pack(pady=5)
activity_var = ctk.StringVar(value="Средняя")
activity_menu = ctk.CTkOptionMenu(frame_kbju, variable=activity_var, values=["Минимальная", "Низкая", "Средняя", "Высокая", "Очень высокая"], width=200, height=40, font=ctk.CTkFont(size=14))
activity_menu.pack(pady=5)

kbju_button = ctk.CTkButton(frame_kbju, text="Рассчитать КБЖУ", command=calculate_kbju, width=200, height=40, font=ctk.CTkFont(size=14))
kbju_button.pack(pady=10)

# Подпись внизу окна
footer_label = ctk.CTkLabel(root, text="open code on github", font=ctk.CTkFont(size=10), fg_color="gray")
footer_label.pack(side="bottom", pady=10)
footer_label.bind("<Button-1>", open_github)

# Запуск приложения
root.mainloop()