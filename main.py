import tkinter as tk
from tkinter import ttk, filedialog
import os
import time
import subprocess
import sys
import math

textC = "text"
sta_path = "config/conf.txt"

palette = {
    'window': '#DFDFFF',
    'foreground': '#004167',
    'button': '#ADD9DA',
    'tab': '#D9D9D9',
    'red': '#D9D9D9',
    'tabS': '#DFDFFF',
    'tabbg': '#DFDFFF'
}
#lis_path="./config/conf.txt"
#pla_path="./config/conf.txt"

options_a="#"
options_b="#"

font_style = "Consolas"
size = 10

class FigureLogic:
    FOS = "/pl/list.txt"  # figure of speech file
    TURN = "output.txt"    # current turn file
    PLAYERS = "/gm/stats.txt"

    @staticmethod
    def sigmoid(x):
        """Python implementation of the C++ sigmoid function"""
        return 10.0/(1.0 + math.pow(1.6, -x)) + 10.0

    @staticmethod
    def inverted_sigmoid(x):
        """Python implementation of the C++ invertedSigmoid function"""
        return -math.log((20.0-x)/(x-10.0))/math.log(1.6)

    @staticmethod
    def load_map(filepath):
        """Load figures and their scores from file"""
        figure_map = {}
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    if ';' in line:
                        figure, score = line.strip().split(';')
                        figure_map[figure] = float(score)
        except FileNotFoundError:
            print(f"Warning: Could not find file {filepath}")
        return figure_map

    @staticmethod
    def save_map(filepath, figure_map):
        """Save figures and their scores to file"""
        with open(filepath, 'w') as file:
            for figure, score in figure_map.items():
                file.write(f"{figure};{score}\n")

    @staticmethod
    def update_scores(figure_map):
        """Update scores using sigmoid functions"""
        for figure in figure_map:
            x = FigureLogic.inverted_sigmoid(figure_map[figure])
            if x > 0:
                figure_map[figure] = FigureLogic.sigmoid(int(math.sqrt(x)))
            else:
                figure_map[figure] = FigureLogic.sigmoid(int(math.sqrt(abs(x)) * -1.0))
        return figure_map

    @staticmethod
    def refresh(base_path):
        """Main refresh function that updates all figure scores"""
        fos_path = base_path + FigureLogic.FOS
        figure_map = FigureLogic.load_map(fos_path)
        figure_map = FigureLogic.update_scores(figure_map)
        FigureLogic.save_map(fos_path, figure_map)

    @staticmethod
    def get_path():
        """Get base path from path.txt"""
        try:
            with open("path.txt", 'r') as file:
                return file.readline().strip()
        except FileNotFoundError:
            return ""

class App:
    def __init__(self, root):
        self.lis_path = None
        self.button_var = tk.StringVar()
        self.root = root
        self.root.title("App")
        self.root.geometry("800x600")
        self.root.configure(bg=palette['red'])

        style = ttk.Style()
        style.configure('TButton', background=palette['button'], foreground=palette['foreground'], font=(font_style, size))
        style.configure('TCombobox', background=palette['button'], foreground=palette['foreground'], font=(font_style, size))
        style.configure('TLabel', background=palette['window'], foreground=palette['foreground'], font=(font_style, size))
        style.configure('TEntry', background=palette['window'], foreground=palette['foreground'], font=(font_style, size))
        style.configure("TNotebook.Tab", font=(font_style, size), background=palette['tab'], foreground=palette['foreground'])

        self.notebook = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="🖊 Gioco              ")
        self.notebook.add(self.tab2, text="📖 Classifica         ")
        self.notebook.add(self.tab3, text="⚙ Settings           ")

        style.map('TNotebook.Tab', background=[('selected', palette['tabS']), ('!selected', palette['tab'])])
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_tab1_widgets()
        self.create_tab2_widgets()
        self.create_tab3_widgets()
        
    def clear_tab1_widgets(self):
        for widget in self.tab1.winfo_children():
            widget.destroy()
            
    def clear_tab2_widgets(self):
        for widget in self.tab2.winfo_children():
            widget.destroy()

    def create_tab1_widgets(self):
        
        self.clear_tab1_widgets()
        
        canvas1 = tk.Canvas(self.tab1, bg=palette['tabbg'], bd=0)
        canvas1.pack(fill='both', expand=True)

        label_list = ttk.Label(canvas1, text="  ")
        label_list.grid(row=0, column=0, padx=10, pady=10)

        label_list = ttk.Label(canvas1, text="Lista:")
        label_list.grid(row=0, column=1, padx=10, pady=10)

        label_list = ttk.Label(canvas1, text="  ")
        label_list.grid(row=0, column=2, padx=10, pady=10)

        self.listbox_content = tk.Listbox(canvas1, width=25, height=30, font=(font_style, size), bd=0)
        self.listbox_content.grid(row=1, column=1, padx=10, pady=10)

        self.text_box = tk.Text(canvas1, width=85, height=15, font=("calibri", 23), bd=0)
        scrollbar = tk.Scrollbar(canvas1, command=self.text_box.yview, bg=palette['button'], relief="flat")
        scrollbar.grid(row=1, column=5, sticky='ns')
        self.text_box.config(yscrollcommand=scrollbar.set)
        self.text_box.grid(row=1, column=3, padx=10, pady=10, columnspan=2)

        ttk.Button(canvas1, text="Salva", command=self.save_file).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(canvas1, text="Carica", command=self.load_file).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(canvas1, text="Fine Round", command=self.end_round).grid(row=4, column=1, padx=1, pady=1)
        ttk.Button(canvas1, text="#", command=self.create_tab1_widgets).grid(row=5, column=1, padx=1, pady=1)

        self.load_list_content()
        global dropdown_a, dropdown_b
        global options_a, options_b

        dropdown_a = tk.StringVar()
        dropdown_a.set(options_a[0])
        menu_a = tk.OptionMenu(canvas1, dropdown_a, *options_a)
        menu_a.grid(row=2, column=3, padx=10, pady=10)  
        
        dropdown_b = tk.StringVar()
        dropdown_b.set(options_b[0])
        menu_b = tk.OptionMenu(canvas1, dropdown_b, *options_b)
        menu_b.grid(row=3, column=3, padx=10, pady=10)  
        
        tk.Button(canvas1, text="V", command=self.on_press_v).grid(row=2, column=4, padx=10, pady=10)  
        tk.Button(canvas1, text="F", command=self.on_press_f).grid(row=3, column=4, padx=10, pady=10) 
        


    def create_tab2_widgets(self):
        
        self.clear_tab2_widgets()
        
        canvasB = tk.Canvas(self.tab2, bg=palette['tabbg'], bd=0)
        canvasB.pack(fill='both', expand=True)
        
        canvas2 = tk.Canvas(canvasB, bg='white', bd=0, height=800, width=1400)
        canvas2.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(canvasB, text="Update", command=self.create_tab2_widgets).grid(row=1, column=2, padx=10, pady=10) 

        global sta_path
        # Read the content from the stats.txt file
        try:
            with open(sta_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("File 'stats.txt' not found.")
            return

        # Parse the content and display as grid
        for i, line in enumerate(lines):
            parts = line.strip().split("|")
            if len(parts) != 2:
                print(f"Error parsing line {i + 1}")
                continue
            row_label = parts[0]
            values = parts[1].split(";")
            canvas2.create_text(30, 20 + i * 30, anchor=tk.W, text=row_label)
            for j, value in enumerate(values):
                canvas2.create_text(60 + j * 40, 20 + i * 30, anchor=tk.W, text=f"[{value}]")

        
        

    def create_tab3_widgets(self):
        canvas3 = tk.Canvas(self.tab3, bg=palette['tabbg'], bd=0)
        canvas3.pack(fill='both', expand=True)

        label_t0 = ttk.Label(canvas3, text="Classe:")
        label_t0.grid(row=0, column=0, padx=10, pady=10)

        self.entry_t0 = ttk.Entry(canvas3)
        self.entry_t0.grid(row=0, column=1, padx=10, pady=10)

        label_s1 = ttk.Label(canvas3, text="Lista:")
        label_s1.grid(row=1, column=0, padx=10, pady=10)

        self.combobox_s1 = ttk.Combobox(canvas3, state="readonly")
        self.combobox_s1.grid(row=1, column=1, padx=10, pady=10)

        label_s2 = ttk.Label(canvas3, text="Salvataggio:")
        label_s2.grid(row=2, column=0, padx=10, pady=10)

        self.combobox_s2 = ttk.Combobox(canvas3, state="readonly")
        self.combobox_s2.grid(row=2, column=1, padx=10, pady=10)

        btn_action = ttk.Button(canvas3, text="Update", command=self.execute_action, style='TButton')
        btn_action.grid(row=3, column=0, columnspan=2, pady=10)

    def load_list_content(self):
        self.listbox_content.delete(0, tk.END)
        try:
            with open(lis_path, "r") as file:
                lines = file.readlines()
                lines.sort(key=lambda line: line.split(';')[0])
                lines.sort(key=lambda line: float(line.split(';')[1]))
                for line in lines:
                    line = line.strip()
                    if ';' in line:
                        word, number = line.split(';')
                        number = float(number)
                        number = int(number)
                        number = str(number).rjust(2, '0')
                        formatted_line = f"{word.ljust(20)}[{number.strip()}]"
                        self.listbox_content.insert(tk.END, formatted_line)
        except FileNotFoundError:
            print(lis_path)
        except Exception as e:
            print(f"Error reading file: {e}")
    
    def execute_action(self):
        current_file_path = os.path.abspath(sys.argv[0])
        main_path = os.path.dirname(current_file_path)
        t0_path = self.entry_t0.get()
        s1_path = os.path.join(main_path, t0_path, "pl")
        s2_path = os.path.join(main_path, t0_path, "gm")
        s3_path = os.path.join(main_path, t0_path, "gm")
        s1_files = os.listdir(s1_path)
        s2_files = os.listdir(s2_path)
        self.combobox_s1["values"] = s1_files
        self.combobox_s2["values"] = s2_files
        selected_fileA = self.combobox_s1.get()
        selected_fileB = self.combobox_s2.get()
        global lis_path, pla_path, sta_path
        lis_path = os.path.join(s1_path, selected_fileA)
        pla_path = os.path.join(s2_path, selected_fileB)
        sta_path = os.path.join(s3_path, "stats.txt")
        print(lis_path)
        print(pla_path)
        with open("path.txt", "w") as file:
            content = self.entry_t0.get()
            file.write(content)
        self.load_list_content()
        global options_a, options_b
        options_a = self.load_list()
        options_b = self.load_players()

    def load_file(self):
        self.text_box.delete(1.0, tk.END)
        try:
            file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    self.text_box.insert(tk.END, line)
        except FileNotFoundError:
            print(lis_path)
        except Exception as e:
            print(f"Error reading file: {e}")

    def save_file(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            with open(file_path, "w") as file:
                content = self.text_box.get("1.0", tk.END)
                file.write(content)
        except Exception as e:
            print(f"Error writing file: {e}")

    def on_press_v(self):
        self.button_var.set("1")
        self.create_file()
        self.execute_action()
        time.sleep(0.5)
        try:
            subprocess.run("calc.exe", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        time.sleep(0.5)
        self.load_list_content()

    def on_press_f(self):
        self.button_var.set("-1")
        self.create_file()
        self.execute_action()
        time.sleep(0.5)
        try:
            subprocess.run("calc.exe", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        time.sleep(0.5)
        self.load_list_content()

    def create_file(self):
        selected_item_a = dropdown_a.get()
        selected_item_b = dropdown_b.get()
        button_pressed = self.button_var.get()
        file_content = f"{selected_item_b[:2]};{selected_item_a[:-3]};{button_pressed}"
        with open("output.txt", "w") as file:
            file.write(file_content)
        print(file_content)

    def load_list(self):
        global lis_path
        with open(lis_path, "r") as file:
            lines = [line.strip().replace(";", " ") for line in file]
            options = [line.split(".")[0] for line in lines]
        return options


    def load_players(self):
        global pla_path
        with open(pla_path, "r") as file:
            options = [line.strip().replace(";", " ") for line in file]
        return options
    
    def end_round(self):
        try:
            base_path = FigureLogic.get_path()
            FigureLogic.refresh(base_path)
        except Exception as e:
            print(f"Error refreshing figures: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
