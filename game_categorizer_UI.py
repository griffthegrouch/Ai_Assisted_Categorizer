import tkinter as tk
import csv
from tkinter import filedialog
from tkinter import ttk
import threading
from threading import Event
import queue
from queue import Queue
import game_categorizer_module as game_categorizer


class GameCategorizerUI:



    def __init__(self):
        self.categories_file_path = "/Users/griffin/PycharmProjects/VideoGameCategorizer/categories_list.csv"
        self.games_file_path = "/Users/griffin/PycharmProjects/VideoGameCategorizer/games_list.csv"

        self.categories = []
        self.games = []
        self.categorized_games_dict = {}

        self.thread = threading
        self.event = Event()
        self.queue = Queue()

        self.root = tk.Tk()
        self.root.title("Game Categorizer")
        self.root.geometry("600x800")

        self.title = tk.Label(self.root, text="Welcome to Game Categorizer", font=("Helvetica", 16))
        self.title.pack()

        self.file_select_label = tk.Label(self.root,
                                          text="Select a file containing a list of games or drop a list of text here:")
        self.file_select_label.pack()

        file_entry_string = tk.StringVar(self.root, self.games_file_path)
        self.file_entry = tk.Entry(self.root, textvariable=file_entry_string)
        self.file_entry.pack()

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.games_list = ttk.Combobox(self.root, state="readonly")
        self.games_list.pack()

        self.platform_label = tk.Label(self.root, text="Select Platform:")
        self.platform_label.pack()

        # self.var_platform = tk.StringVar()
        # self.platform_mac = tk.Radiobutton(self.root, text="Mac", variable=self.var_platform, value="Mac")
        # self.platform_mac.pack()
        # self.platform_windows = tk.Radiobutton(self.root, text="Windows", variable=self.var_platform, value="Windows")
        # self.platform_windows.pack()

        self.categories_label = tk.Label(self.root, text="Select categories to search:")
        self.categories_label.pack()

        self.categories_list = ttk.Combobox(self.root, state="readonly")
        self.load_categories()
        self.categories_list.pack()
        self.add_category_button = tk.Button(self.root, text="Add category", command=self.add_category)
        self.add_category_button.pack()
        self.remove_category_button = tk.Button(self.root, text="Remove category", command=self.remove_category)
        self.remove_category_button.pack()

        self.custom_category_label = tk.Label(self.root, text="Enter a custom category to search for:")
        self.custom_category_label.pack()

        self.custom_category_entry = tk.Entry(self.root)
        self.custom_category_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack()

        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")
        self.progressbar.pack()

        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel)
        self.cancel_button.pack()

        self.results_button = tk.Button(self.root, text="Show Results", command=self.show_results)
        self.results_button.pack()

        self.save_results_button = tk.Button(self.root, text="Save Results", command=self.save_results)
        self.save_results_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit Program", command=self.exit_program)
        self.exit_button.pack()

        self.read_games(self.games_file_path)
        self.read_categories(self.categories_file_path)

    def browse_file(self):
        filepath = filedialog.askopenfilename()
        self.games_file_path = filepath
        self.read_games(filepath)

    def read_csv(self, filepath):
        items = []
        # Load items from file
        try:
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                for item in reader:
                    items.append(item[0])
            return items
        except FileNotFoundError:
            print(f"{filepath} not found.")
            return
        except:
            print("An error occurred while trying to read the file.")
        return

    def read_games(self, filepath):
        items = self.read_csv(filepath)
        self.games = items
        self.games_list['values'] = items

    def read_categories(self, filepath):
        items = self.read_csv(filepath)
        self.categories = items
        self.categories_list['values'] = items

    def add_category(self):
        pass
        category = self.custom_category_entry.get()
        self.categories_list['values'] += category
        self.save_categories()

    def remove_category(self):
        pass
        selected = self.categories_list.curselection()
        if selected:
            self.categories_list.delete(selected[0])
            self.save_categories()

    def load_categories(self):
        pass
        with open(self.categories_file_path, "r") as file:
            reader = csv.reader(file)
            categories = []
            for category in reader:
                categories.append(category)
            self.categories_list['values'] = categories

    def save_categories(self):
        pass
        with open(self.categories_file_path, "w") as file:
            writer = csv.writer(file)
            for idx in range(self.categories_list.size()):
                writer.writerow([self.categories_list.get(idx)])

    def start(self):

        filepath = self.games_file_path
        # categories = self.categories_list.get() #[self.categories_list.get(idx) for idx in self.categories_list.curselection()]
        custom_category = self.custom_category_entry.get()
        self.event.clear()
        print("starting categorization...")
        thread = threading.Thread(
            target=game_categorizer.categorize_games(self.games, self.categories, self.root, self.progressbar,
                                                     self.event, self.queue))
        #print("peek")
        ##print(self.queue())
        self.categorized_games_dict = self.queue.get()
        print(self.categorized_games_dict)
        print("done!")

    def cancel(self):
        # cancel the task
        self.event.set()
        self.progressbar['value'] = 0

    def show_results(self):
        win = tk.Toplevel()
        win.wm_title("Results")

        label = tk.Label(win, text="Results")
        label.grid(row=0, column=0)

        print("categorized_games_dict: ")
        print(self.categorized_games_dict)
        res = tk.Label(win, text=self.categorized_games_dict)
        res.grid(row=1, column=0)

        b = ttk.Button(win, text="Close", command=win.destroy)
        b.grid(row=2, column=0)

    def save_results(self):
        pass

    def exit_program(self):
        print("Program terminated manually!")
        exit()
        self.root.mainloop()
