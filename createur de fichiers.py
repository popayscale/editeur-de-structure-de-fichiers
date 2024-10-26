import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

class FileEntry(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=2)
        self.extension_entry = tk.Entry(self, width=10)
        self.extension_entry.pack(side=tk.LEFT, padx=2)

    def get(self):
        return self.name_entry.get(), self.extension_entry.get()

def create_files_direct():
    target_dir = filedialog.askdirectory(title="Choisissez le dossier cible")
    if not target_dir:
        return
    
    base_name = name_entry.get().strip()
    extension = extension_entry.get().strip()
    quantity_str = single_quantity_entry.get().strip()
    
    if not base_name:
        messagebox.showerror("Erreur", "Veuillez entrer un nom de base.")
        return
    if not extension:
        messagebox.showerror("Erreur", "Veuillez entrer une extension.")
        return
    if not quantity_str:
        messagebox.showerror("Erreur", "Veuillez entrer une quantité.")
        return
    
    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            raise ValueError("La quantité doit être supérieure à zéro.")
    except ValueError as e:
        messagebox.showerror("Erreur", f"Quantité invalide : {str(e)}")
        return
    
    if not extension.startswith('.'):
        extension = '.' + extension

    created_files = []
    for i in range(1, quantity + 1):
        file_name = f"{base_name}{i}{extension}"
        file_path = os.path.join(target_dir, file_name)
        
        counter = 1
        while os.path.exists(file_path):
            file_name = f"{base_name}{i}({counter}){extension}"
            file_path = os.path.join(target_dir, file_name)
            counter += 1
        
        with open(file_path, 'w') as f:
            f.write(f"Contenu du fichier {file_name}")
        created_files.append(file_name)
    
    messagebox.showinfo("Succès", f"{quantity} fichier(s) ont été créés dans {target_dir}\n\nFichiers créés:\n" + "\n".join(created_files))

def create_multiple_files():
    target_dir = filedialog.askdirectory(title="Choisissez le dossier cible")
    if not target_dir:
        return
    
    created_files = []
    for file_entry in file_entries:
        name, extension = file_entry.get()
        name = name.strip()
        extension = extension.strip()
        
        if not name or not extension:
            continue
        
        if not extension.startswith('.'):
            extension = '.' + extension
        
        file_name = f"{name}{extension}"
        file_path = os.path.join(target_dir, file_name)
        
        counter = 1
        while os.path.exists(file_path):
            file_name = f"{name}({counter}){extension}"
            file_path = os.path.join(target_dir, file_name)
            counter += 1
        
        with open(file_path, 'w') as f:
            f.write(f"Contenu du fichier {file_name}")
        created_files.append(file_name)
    
    if created_files:
        messagebox.showinfo("Succès", f"{len(created_files)} fichier(s) ont été créés dans {target_dir}\n\nFichiers créés:\n" + "\n".join(created_files))
    else:
        messagebox.showwarning("Attention", "Aucun fichier n'a été créé. Vérifiez les noms et extensions saisis.")

def copy_files():
    source_dir = filedialog.askdirectory(title="Choisissez le dossier source")
    if not source_dir:
        return
    
    target_dir = filedialog.askdirectory(title="Choisissez le dossier cible")
    if not target_dir:
        return
    
    copied_files = []
    for file_name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, file_name)
        if os.path.isfile(source_path):
            target_path = os.path.join(target_dir, file_name)
            
            counter = 1
            while os.path.exists(target_path):
                name, ext = os.path.splitext(file_name)
                new_name = f"{name}({counter}){ext}"
                target_path = os.path.join(target_dir, new_name)
                counter += 1
            
            shutil.copy2(source_path, target_path)
            copied_files.append(os.path.basename(target_path))
    
    if copied_files:
        messagebox.showinfo("Succès", f"{len(copied_files)} fichier(s) ont été copiés de {source_dir} vers {target_dir}\n\nFichiers copiés:\n" + "\n".join(copied_files))
    else:
        messagebox.showwarning("Attention", "Aucun fichier n'a été copié. Vérifiez le contenu du dossier source.")

def toggle_multiple_files():
    if multiple_files_var.get():
        single_file_frame.pack_forget()
        multiple_files_frame.pack()
        quantity_label.pack()
        multiple_quantity_entry.pack()
        generate_entries_button.pack()
        back_button.pack(pady=5)
    else:
        reset_to_single_file_mode()

def reset_to_single_file_mode():
    multiple_files_frame.pack_forget()
    quantity_label.pack_forget()
    multiple_quantity_entry.pack_forget()
    generate_entries_button.pack_forget()
    back_button.pack_forget()
    single_file_frame.pack()
    multiple_files_var.set(False)
    
    for widget in file_entries_frame.winfo_children():
        widget.destroy()
    file_entries.clear()

def generate_file_entries():
    for widget in file_entries_frame.winfo_children():
        widget.destroy()
    file_entries.clear()

    try:
        num_entries = int(multiple_quantity_entry.get())
        if num_entries <= 0:
            raise ValueError("Le nombre doit être positif")
        for _ in range(num_entries):
            file_entry = FileEntry(file_entries_frame)
            file_entry.pack()
            file_entries.append(file_entry)
        create_multiple_button.pack()
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif pour la quantité.")

def parse_structure(text):
    lines = text.split('\n')
    structure = {}
    current_path = []
    
    for line in lines:
        stripped_line = line.lstrip('|   ')
        depth = (len(line) - len(stripped_line)) // 4  # Chaque niveau est représenté par 4 espaces
        name = stripped_line.strip()
        
        if name:
            # Ajuster current_path en fonction de la profondeur
            current_path = current_path[:depth]
            current_path.append(name)
            
            # Naviguer dans la structure et créer les niveaux nécessaires
            current_dict = structure
            for path_part in current_path[:-1]:
                if path_part not in current_dict:
                    current_dict[path_part] = {}
                current_dict = current_dict[path_part]
            
            # Ajouter le dernier élément
            if current_path[-1] not in current_dict:
                current_dict[current_path[-1]] = {}
    
    return structure

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if content:  # C'est un dossier
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:  # C'est un fichier
            open(path, 'a').close()

def choose_directory_for_structure():
    folder_selected = filedialog.askdirectory()
    structure_directory_entry.delete(0, tk.END)
    structure_directory_entry.insert(0, folder_selected)

def generate_structure():
    text = structure_input_text.get("1.0", tk.END)
    base_path = structure_directory_entry.get()
    
    if not base_path:
        messagebox.showerror("Erreur", "Veuillez choisir un dossier de destination.")
        return
    
    try:
        structure = parse_structure(text)
        create_structure(base_path, structure)
        messagebox.showinfo("Succès", "Structure créée avec succès!")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la création de la structure : {str(e)}")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Gestionnaire de fichiers")

# Créer un notebook (onglets)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Onglet 1 : Création de fichiers
file_creation_frame = ttk.Frame(notebook)
notebook.add(file_creation_frame, text="Création de fichiers")

# Widgets pour la création de fichiers uniques
single_file_frame = tk.Frame(file_creation_frame)
single_file_frame.pack(pady=10)

tk.Label(single_file_frame, text="Nom de base:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(single_file_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(single_file_frame, text="Extension:").grid(row=1, column=0, padx=5, pady=5)
extension_entry = tk.Entry(single_file_frame)
extension_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(single_file_frame, text="Quantité:").grid(row=2, column=0, padx=5, pady=5)
single_quantity_entry = tk.Entry(single_file_frame)
single_quantity_entry.grid(row=2, column=1, padx=5, pady=5)

start_button = ttk.Button(single_file_frame, text="Start", command=create_files_direct)
start_button.grid(row=3, column=0, columnspan=2, pady=10)

# Widgets pour la création de plusieurs fichiers
multiple_files_frame = tk.Frame(file_creation_frame)
file_entries = []

multiple_files_var = tk.BooleanVar()
multiple_files_check = ttk.Checkbutton(file_creation_frame, text="Créer plusieurs fichiers avec des noms différents", 
                                       variable=multiple_files_var, command=toggle_multiple_files)
multiple_files_check.pack(pady=5)

quantity_label = tk.Label(multiple_files_frame, text="Nombre de fichiers:")
multiple_quantity_entry = tk.Entry(multiple_files_frame, width=5)
generate_entries_button = ttk.Button(multiple_files_frame, text="Générer les champs", command=generate_file_entries)

file_entries_frame = tk.Frame(multiple_files_frame)
file_entries_frame.pack()

create_multiple_button = ttk.Button(multiple_files_frame, text="Créer des fichiers", command=create_multiple_files)

back_button = ttk.Button(multiple_files_frame, text="Retour au menu précédent", command=reset_to_single_file_mode)

copy_button = ttk.Button(file_creation_frame, text="Copier des fichiers", command=copy_files)
copy_button.pack(pady=5)

# Onglet 2 : Générateur de structure
structure_frame = ttk.Frame(notebook)
notebook.add(structure_frame, text="Générateur de structure")

# Zone de texte pour la saisie de la structure
structure_input_text = tk.Text(structure_frame, height=20, width=50)
structure_input_text.pack(pady=10)

# Champ et bouton pour choisir le dossier de destination
structure_directory_frame = tk.Frame(structure_frame)
structure_directory_frame.pack(pady=5)

structure_directory_entry = tk.Entry(structure_directory_frame, width=40)
structure_directory_entry.pack(side=tk.LEFT)

structure_choose_button = tk.Button(structure_directory_frame, text="Choisir dossier", command=choose_directory_for_structure)
structure_choose_button.pack(side=tk.LEFT)

# Bouton pour générer la structure
generate_structure_button = tk.Button(structure_frame, text="Générer structure", command=generate_structure)
generate_structure_button.pack(pady=10)

# Lancer la boucle principale de l'interface graphique
root.mainloop()
