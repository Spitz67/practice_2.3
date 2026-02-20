import requests
import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

SAVE_FILE = "save.json"
CURRENCY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

currency_data = {}
user_groups = {}

def fetch_currency_data():
    global currency_data
    try:
        response = requests.get(CURRENCY_URL)
        response.raise_for_status()
        data = response.json()
        currency_data = data.get('Valute', {})
        text_output.insert(tk.END, "Курсы обновлены\n")
    except:
        currency_data = {}
        text_output.insert(tk.END, "Ошибка загрузки\n")

def print_all_currencies():
    if not currency_data:
        text_output.insert(tk.END, "Нет данных\n")
        return
    for code, info in sorted(currency_data.items()):
        name = info.get('Name', '')
        nominal = info.get('Nominal', 1)
        value = info.get('Value', 0)
        text_output.insert(tk.END, f"{code} {nominal} {name} {value}\n")

def print_currency_by_code():
    if not currency_data:
        text_output.insert(tk.END, "Нет данных\n")
        return
    code = simpledialog.askstring("Поиск", "Введите код валюты:").upper().strip()
    if code in currency_data:
        info = currency_data[code]
        text_output.insert(tk.END, f"{code}\n")
        text_output.insert(tk.END, f"{info.get('Name', '')}\n")
        text_output.insert(tk.END, f"{info.get('Nominal', 1)}\n")
        text_output.insert(tk.END, f"{info.get('Value', 0)}\n")
    else:
        text_output.insert(tk.END, "Не найдено\n")

def load_groups():
    global user_groups
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                user_groups = json.load(f)
        except:
            user_groups = {}
    else:
        user_groups = {}
    text_output.insert(tk.END, "Группы загружены\n")

def save_groups():
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_groups, f, ensure_ascii=False, indent=4)
        text_output.insert(tk.END, "Сохранено\n")
    except:
        text_output.insert(tk.END, "Ошибка сохранения\n")

def create_group():
    group_name = simpledialog.askstring("Создать группу", "Введите название группы:").strip()
    if not group_name:
        return
    if group_name in user_groups:
        text_output.insert(tk.END, "Группа уже существует\n")
        return
    user_groups[group_name] = []
    text_output.insert(tk.END, f"Группа {group_name} создана\n")

def add_currency_to_group():
    if not user_groups:
        text_output.insert(tk.END, "Нет групп\n")
        return
    if not currency_data:
        text_output.insert(tk.END, "Нет данных о валютах\n")
        return
    for group in user_groups.keys():
        text_output.insert(tk.END, group + "\n")
    group_name = simpledialog.askstring("Добавить", "Введите название группы:").strip()
    if group_name not in user_groups:
        text_output.insert(tk.END, "Группа не найдена\n")
        return
    code = simpledialog.askstring("Добавить", "Введите код валюты:").upper().strip()
    if code not in currency_data:
        text_output.insert(tk.END, "Валюта не найдена\n")
        return
    if code not in user_groups[group_name]:
        user_groups[group_name].append(code)
        text_output.insert(tk.END, f"{code} добавлен в {group_name}\n")

def remove_currency_from_group():
    if not user_groups:
        text_output.insert(tk.END, "Нет групп\n")
        return
    group_name = simpledialog.askstring("Удалить", "Введите название группы:").strip()
    if group_name not in user_groups:
        text_output.insert(tk.END, "Группа не найдена\n")
        return
    if not user_groups[group_name]:
        text_output.insert(tk.END, "Группа пуста\n")
        return
    for code in user_groups[group_name]:
        text_output.insert(tk.END, code + "\n")
    code_to_remove = simpledialog.askstring("Удалить", "Введите код валюты для удаления:").upper().strip()
    if code_to_remove in user_groups[group_name]:
        user_groups[group_name].remove(code_to_remove)
        text_output.insert(tk.END, f"{code_to_remove} удален\n")

def list_groups():
    if not user_groups:
        text_output.insert(tk.END, "Нет групп\n")
        return
    for group_name, currencies in user_groups.items():
        text_output.insert(tk.END, f"{group_name}\n")
        if currencies:
            for code in currencies:
                if code in currency_data:
                    info = currency_data[code]
                    text_output.insert(tk.END, f"  {code} {info.get('Name', '')} {info.get('Value', 0)}\n")
                else:
                    text_output.insert(tk.END, f"  {code}\n")
        else:
            text_output.insert(tk.END, "  пусто\n")

def edit_group_menu():
    choice = simpledialog.askstring("Редактирование", "1. Добавить валюту\n2. Удалить валюту\n0. Назад\nВыберите действие:")
    if choice == '1':
        add_currency_to_group()
    elif choice == '2':
        remove_currency_from_group()

def clear_output():
    text_output.delete(1.0, tk.END)

root = tk.Tk()
root.title("Курсы валют")
root.geometry("600x400")

text_output = tk.Text(root, wrap=tk.WORD, font=("Courier", 10))
text_output.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

scrollbar = tk.Scrollbar(text_output)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_output.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_output.yview)

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=5, pady=5)

buttons = [
    ("1. Все валюты", print_all_currencies),
    ("2. Поиск по коду", print_currency_by_code),
    ("3. Создать группу", create_group),
    ("4. Все группы", list_groups),
    ("5. Редактировать группы", edit_group_menu),
    ("6. Обновить курсы", fetch_currency_data),
    ("7. Сохранить", save_groups),
    ("8. Очистить", clear_output),
    ("0. Выход", root.quit)
]

for i, (text, command) in enumerate(buttons):
    btn = tk.Button(button_frame, text=text, command=command)
    btn.pack(side=tk.LEFT, padx=2)

load_groups()
fetch_currency_data()

root.mainloop()

if user_groups:
    if messagebox.askyesno("Сохранение", "Сохранить перед выходом?"):
        save_groups()