import requests
import tkinter as tk
from tkinter import simpledialog, scrolledtext

GITHUB_API = "https://api.github.com"

def get_user_profile(username):
    url = f"{GITHUB_API}/users/{username}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            user = res.json()
            text_output.insert(tk.END, "\nПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ\n")
            text_output.insert(tk.END, f"Имя: {user.get('name', 'N/A')}\n")
            text_output.insert(tk.END, f"Ссылка на профиль: {user.get('html_url')}\n")
            text_output.insert(tk.END, f"Количество репозиториев: {user.get('public_repos')}\n")
            text_output.insert(tk.END, f"Подписчики: {user.get('followers')}\n")
            text_output.insert(tk.END, f"Подписки: {user.get('following')}\n")
        elif res.status_code == 404:
            text_output.insert(tk.END, f"Пользователь '{username}' не найден\n")
        else:
            text_output.insert(tk.END, f"Ошибка: {res.status_code}\n")
    except requests.exceptions.ConnectionError:
        text_output.insert(tk.END, "Ошибка соединения с сервером\n")
    except Exception as e:
        text_output.insert(tk.END, f"Ошибка: {str(e)}\n")

def get_user_repos(username):
    url = f"{GITHUB_API}/users/{username}/repos"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            repositories = res.json()
            if not repositories:
                text_output.insert(tk.END, f"У пользователя '{username}' нет публичных репозиториев\n")
                return
            text_output.insert(tk.END, f"\nРЕПОЗИТОРИИ {username}\n")
            for repo in repositories:
                text_output.insert(tk.END, f"\n{repo['name']}\n")
                text_output.insert(tk.END, f"   Ссылка: {repo['html_url']}\n")
                text_output.insert(tk.END, f"   Язык: {repo.get('language', 'N/A')}\n")
                text_output.insert(tk.END, f"   Видимость: {'Public' if not repo['private'] else 'Private'}\n")
                text_output.insert(tk.END, f"   Ветка по умолчанию: {repo.get('default_branch')}\n")
        elif res.status_code == 404:
            text_output.insert(tk.END, f"Пользователь '{username}' не найден\n")
        else:
            text_output.insert(tk.END, f"Ошибка: {res.status_code}\n")
    except requests.exceptions.ConnectionError:
        text_output.insert(tk.END, "Ошибка соединения с сервером\n")
    except Exception as e:
        text_output.insert(tk.END, f"Ошибка: {str(e)}\n")

def search_repos(query):
    url = f"{GITHUB_API}/search/repositories"
    params = {"q": query}
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            items = data.get("items", [])
            if not items:
                text_output.insert(tk.END, f"Репозитории по запросу '{query}' не найдены\n")
                return
            text_output.insert(tk.END, f"\nРЕЗУЛЬТАТЫ ПОИСКА ДЛЯ '{query}'\n")
            for repo in items[:5]:
                text_output.insert(tk.END, f"\n{repo['name']}\n")
                text_output.insert(tk.END, f"   Владелец: {repo['owner']['login']}\n")
                text_output.insert(tk.END, f"   Ссылка: {repo['html_url']}\n")
                text_output.insert(tk.END, f"   Язык: {repo.get('language', 'N/A')}\n")
        else:
            text_output.insert(tk.END, f"Ошибка поиска: {res.status_code}\n")
    except requests.exceptions.ConnectionError:
        text_output.insert(tk.END, "Ошибка соединения с сервером\n")
    except Exception as e:
        text_output.insert(tk.END, f"Ошибка: {str(e)}\n")

def profile_dialog():
    username = simpledialog.askstring("Профиль", "Введите имя пользователя на GitHub:")
    if username:
        get_user_profile(username.strip())

def repos_dialog():
    username = simpledialog.askstring("Репозитории", "Введите имя пользователя на GitHub:")
    if username:
        get_user_repos(username.strip())

def search_dialog():
    query = simpledialog.askstring("Поиск", "Введите название репозитория для поиска:")
    if query:
        search_repos(query.strip())

def clear_output():
    text_output.delete(1.0, tk.END)

root = tk.Tk()
root.title("GitHub Explorer")
root.geometry("650x500")

text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10))
text_output.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=5, pady=5)

buttons = [
    ("1. Профиль пользователя", profile_dialog),
    ("2. Репозитории пользователя", repos_dialog),
    ("3. Поиск репозиториев", search_dialog),
    ("4. Очистить", clear_output),
    ("0. Выход", root.quit)
]

for text, command in buttons:
    btn = tk.Button(button_frame, text=text, command=command)
    btn.pack(side=tk.LEFT, padx=2)

root.mainloop()
