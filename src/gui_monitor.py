#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import threading
import monitor  # Ton script de surveillance

def run_monitor():
    try:
        monitor.main(pause_interval=60)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def start_monitoring():
    btn_start.config(state=tk.DISABLED)
    threading.Thread(target=run_monitor, daemon=True).start()
    messagebox.showinfo("Surveillance activée", "Le monitoring des news a démarré !")

# Interface graphique
root = tk.Tk()
root.title("📈 Surveillance de News Financières")

root.geometry("400x200")
root.configure(bg="#f5f5f5")

label = tk.Label(root, text="Surveiller les dernières news économiques", font=("Arial", 14), bg="#f5f5f5")
label.pack(pady=20)

btn_start = tk.Button(root, text="▶️ Lancer la surveillance", font=("Arial", 12), command=start_monitoring, bg="#4CAF50", fg="white")
btn_start.pack(pady=10)

root.mainloop()
