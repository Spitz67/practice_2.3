from tkinter import *
from tkinter import ttk
import requests



root = Tk()
root.title('Проверка соединения')
root.geometry('800x150')

tree = ttk.Treeview(root, columns=("url", "status", "code"), show="headings")
tree.heading('url', text='URL')
tree.heading('status', text='Статус')
tree.heading('code', text='Код')
tree.pack(fill='both', expand=True)


urls = [
    'https://github.com/',
    'https://www.binance.com/en',
    'https://tomtit.tomsk.ru/',
    'https://jsonplaceholder.typicode.com/',
    'https://moodle.tomtit-tomsk.ru/'
]
for i in urls:
    response = requests.get(i)
    code = response.status_code

    status = {
        200: "доступен",
        202: "доступен, но обработка ещё не завершена"
    }.get(code, "не доступен")
    if 400 <= code < 600:
        status = "ошибка сервера"

    tree.insert("", "end", values=(i, status, code))


root.mainloop()