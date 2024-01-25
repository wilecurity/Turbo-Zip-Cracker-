print("""
##   ##   ####    ##                #####    ######   ####    
 ##   ##    ##     ##                ##  ##   ##       ## ##   
 ##   ##    ##     ##                ##  ##   ##       ##  ##  
 ## # ##    ##     ##       ######   #####    ####     ##  ##  
 #######    ##     ##                ####     ##       ##  ##  
 ### ###    ##     ##                ## ##    ##       ## ##   
 ##   ##   ####    ######            ##  ##   ######   #### 
""")

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from optparse import OptionParser
import pyzipper
from progress.bar import Bar

def get_wordlist(wordlist_file):
    try:
        with open(wordlist_file, 'r', errors='replace') as f:
            return f.read().split('\n')
    except UnicodeDecodeError as e:
        print(f"Error decoding file: {e}")
        return []


def extract(file_name, password):
    try:
        with pyzipper.AESZipFile(file_name, 'r') as f:
            f.extractall(pwd=bytes(password, 'utf-8'))
        return True
    except RuntimeError:
        return False

def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def browse_wordlist():
    wordlist_path = filedialog.askopenfilename()
    wordlist_entry.delete(0, tk.END)
    wordlist_entry.insert(0, wordlist_path)

def start_extraction():
    file_name = file_entry.get()
    wordlist_file = wordlist_entry.get()

    password_found = False
    wordlist = get_wordlist(wordlist_file)
    max_value = len(wordlist)

    with Bar('Processing', max=max_value) as bar:
        for p in wordlist:
            if extract(file_name, p):
                result_label.config(text=f"Password found: {p}", foreground="green")
                password_found = True
                break
            bar.next()

    if not password_found:
        result_label.config(text='Zip Password not found, try another wordlist', fg="red")


root = tk.Tk()
root.title("Zip Password Cracker")

file_label = ttk.Label(root, text="Select compressed file:")
file_label.grid(row=0, column=0, padx=10, pady=10)

file_entry = ttk.Entry(root, width=40)
file_entry.grid(row=0, column=1, padx=10, pady=10)

file_button = ttk.Button(root, text="Browse", command=browse_file)
file_button.grid(row=0, column=2, padx=10, pady=10)

wordlist_label = ttk.Label(root, text="Select wordlist:")
wordlist_label.grid(row=1, column=0, padx=10, pady=10)

wordlist_entry = ttk.Entry(root, width=40)
wordlist_entry.grid(row=1, column=1, padx=10, pady=10)

wordlist_button = ttk.Button(root, text="Browse", command=browse_wordlist)
wordlist_button.grid(row=1, column=2, padx=10, pady=10)

start_button = ttk.Button(root, text="Start Extraction", command=start_extraction)
start_button.grid(row=2, column=1, pady=20)

result_label = ttk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=3, column=0, columnspan=3, pady=10)

made_by_label = ttk.Label(root, text="Made By Wilecurity", font=("Helvetica", 10), foreground="gray")
made_by_label.grid(row=4, column=0, columnspan=3, pady=5)

root.mainloop()





