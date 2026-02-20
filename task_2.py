import psutil
import tkinter as tk
from tkinter import ttk
import threading
import time


def update_stats():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent

        text_widget.delete(1.0, tk.END)

        text_widget.insert(tk.END, f"Загрузка CPU: {cpu_percent}%\n")
        text_widget.insert(tk.END, f"Использование RAM: {memory_percent}%\n")

        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                text_widget.insert(tk.END, f"Диск {partition.mountpoint}: {partition_usage.percent}%\n")
            except PermissionError:
                pass

        text_widget.see(1.0)

        time.sleep(1)


def start_monitoring():
    thread = threading.Thread(target=update_stats, daemon=True)
    thread.start()


root = tk.Tk()
root.title("Мониторинг системы")
root.geometry("400x300")

text_widget = tk.Text(root, wrap=tk.WORD, font=("Courier", 10))
text_widget.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

scrollbar = ttk.Scrollbar(text_widget)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

start_monitoring()

root.mainloop()