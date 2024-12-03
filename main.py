import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Initialiser la base de données SQLite
def init_db():
    conn = sqlite3.connect("sante_fitness.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            activite TEXT,
            duree INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            aliment TEXT,
            calories INTEGER
        )
    """)
    conn.commit()
    return conn

# Ajouter une activité
def ajouter_activite():
    date = date_entry.get()
    activite = activite_entry.get()
    duree = duree_entry.get()

    if not date or not activite or not duree:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return

    try:
        conn.execute("INSERT INTO activites (date, activite, duree) VALUES (?, ?, ?)", (date, activite, duree))
        conn.commit()
        messagebox.showinfo("Succès", "Activité ajoutée avec succès.")
        clear_entries()
        afficher_historique()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Ajouter un repas
def ajouter_repas():
    date = date_entry.get()
    aliment = aliment_entry.get()
    calories = calories_entry.get()

    if not date or not aliment or not calories:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return

    try:
        conn.execute("INSERT INTO repas (date, aliment, calories) VALUES (?, ?, ?)", (date, aliment, calories))
        conn.commit()
        messagebox.showinfo("Succès", "Repas ajouté avec succès.")
        clear_entries()
        afficher_historique()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Afficher l'historique
def afficher_historique():
    for item in tree.get_children():
        tree.delete(item)

    # Récupérer les activités
    cursor = conn.execute("SELECT date, activite, duree FROM activites")
    for row in cursor.fetchall():
        tree.insert("", "end", values=(row[0], row[1], f"{row[2]} min"))

    # Récupérer les repas
    cursor = conn.execute("SELECT date, aliment, calories FROM repas")
    for row in cursor.fetchall():
        tree.insert("", "end", values=(row[0], row[1], f"{row[2]} cal"))

# Effacer les champs d'entrée
def clear_entries():
    date_entry.delete(0, tk.END)
    activite_entry.delete(0, tk.END)
    duree_entry.delete(0, tk.END)
    aliment_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)

# Fenêtre principale
conn = init_db()
root = tk.Tk()
root.title("Santé et Fitness")

# Cadre pour les entrées
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Activité:").grid(row=1, column=0, padx=5, pady=5)
activite_entry = tk.Entry(frame)
activite_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Durée (min):").grid(row=2, column=0, padx=5, pady=5)
duree_entry = tk.Entry(frame)
duree_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Aliment:").grid(row=3, column=0, padx=5, pady=5)
aliment_entry = tk.Entry(frame)
aliment_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame, text="Calories:").grid(row=4, column=0, padx=5, pady=5)
calories_entry = tk.Entry(frame)
calories_entry.grid(row=4, column=1, padx=5, pady=5)

# Boutons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Ajouter Activité", command=ajouter_activite).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Ajouter Repas", command=ajouter_repas).grid(row=0, column=1, padx=5, pady=5)

# Historique
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

tree = ttk.Treeview(tree_frame, columns=("Date", "Description", "Détails"), show="headings", height=10)
tree.heading("Date", text="Date")
tree.heading("Description", text="Description")
tree.heading("Détails", text="Détails")
tree.pack()

afficher_historique()

# Lancer l'application
root.mainloop()
