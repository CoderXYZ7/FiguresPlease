#!/usr/bin/env python3
"""
FiguresPlease - An educational game for learning rhetorical figures.
This application helps students practice identifying and evaluating rhetorical figures
through an interactive interface.
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os
import math
import time
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import sys

# UI Constants
PALETTE = {
    'window': '#DFDFFF',
    'foreground': '#004167',
    'button': '#ADD9DA',
    'tab': '#D9D9D9',
    'red': '#D9D9D9',
    'tabS': '#DFDFFF',
    'tabbg': '#DFDFFF'
}

FONT_STYLE = "Consolas"
FONT_SIZE = 10

class FigureLogic:
    """Handles the scoring and evaluation logic for rhetorical figures."""
    
    FOS = "/pl/list.txt"  # figure of speech file
    TURN = "output.txt"    # current turn file
    PLAYERS = "/gm/stats.txt"

    @staticmethod
    def sigmoid(x: float) -> float:
        """Calculate sigmoid function for scoring."""
        return 10.0/(1.0 + math.pow(1.6, -x)) + 10.0

    @staticmethod
    def inverted_sigmoid(x: float) -> float:
        """Calculate inverted sigmoid for score normalization."""
        return -math.log((20.0-x)/(x-10.0))/math.log(1.6)

    @staticmethod
    def load_map(filepath: str) -> Dict[str, float]:
        """Load figures and their scores from file."""
        figure_map = {}
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    if ';' in line:
                        figure, score = line.strip().split(';')
                        figure_map[figure] = float(score)
        except FileNotFoundError:
            print(f"Warning: Could not find file {filepath}")
        return figure_map

    @staticmethod
    def save_map(filepath: str, figure_map: Dict[str, float]) -> None:
        """Save figures and their scores to file."""
        with open(filepath, 'w', encoding='utf-8') as file:
            for figure, score in figure_map.items():
                file.write(f"{figure};{score}\n")

    @staticmethod
    def update_scores(figure_map: Dict[str, float]) -> Dict[str, float]:
        """Update scores using sigmoid functions."""
        for figure in figure_map:
            x = FigureLogic.inverted_sigmoid(figure_map[figure])
            if x > 0:
                figure_map[figure] = FigureLogic.sigmoid(int(math.sqrt(x)))
            else:
                figure_map[figure] = FigureLogic.sigmoid(int(math.sqrt(abs(x)) * -1.0))
        return figure_map

    @staticmethod
    def refresh(base_path: str) -> None:
        """Update all figure scores."""
        fos_path = base_path + FigureLogic.FOS
        figure_map = FigureLogic.load_map(fos_path)
        figure_map = FigureLogic.update_scores(figure_map)
        FigureLogic.save_map(fos_path, figure_map)

    @staticmethod
    def get_path() -> str:
        """Get base path from path.txt."""
        try:
            with open("path.txt", 'r', encoding='utf-8') as file:
                return file.readline().strip()
        except FileNotFoundError:
            return ""

class App:
    """Main application class for the FiguresPlease game."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_style()
        self.setup_notebook()
        self.create_tabs()
        
    def setup_window(self) -> None:
        """Configure the main window."""
        self.root.title("FiguresPlease")
        self.root.geometry("800x600")
        self.root.configure(bg=PALETTE['red'])
        
    def setup_variables(self) -> None:
        """Initialize instance variables."""
        # Initialize paths with default values
        self.lis_path = "config/conf.txt"  # Default list path
        self.pla_path = "config/conf.txt"  # Default player path
        self.sta_path = "config/stats.txt" # Default stats path
        
        # Initialize UI variables
        self.button_var = tk.StringVar()
        self.options_a = ["#"]
        self.options_b = ["#"]
        self.dropdown_a = tk.StringVar(value=self.options_a[0])
        self.dropdown_b = tk.StringVar(value=self.options_b[0])
        
    def setup_style(self) -> None:
        """Configure ttk styles."""
        style = ttk.Style()
        for widget in ['TButton', 'TCombobox', 'TLabel', 'TEntry']:
            style.configure(widget, 
                          background=PALETTE['button'],
                          foreground=PALETTE['foreground'],
                          font=(FONT_STYLE, FONT_SIZE))
        style.configure("TNotebook.Tab",
                       font=(FONT_STYLE, FONT_SIZE),
                       background=PALETTE['tab'],
                       foreground=PALETTE['foreground'])
        style.map('TNotebook.Tab',
                 background=[('selected', PALETTE['tabS']),
                            ('!selected', PALETTE['tab'])])
                            
    def setup_notebook(self) -> None:
        """Setup the notebook with tabs."""
        self.notebook = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab1, text="🖊 Gioco              ")
        self.notebook.add(self.tab2, text="📖 Classifica         ")
        self.notebook.add(self.tab3, text="⚙ Settings           ")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

    def create_tabs(self) -> None:
        """Create all tab contents."""
        self.create_tab1_widgets()  # Game tab
        self.create_tab2_widgets()  # Leaderboard tab
        self.create_tab3_widgets()  # Settings tab

    def clear_tab1_widgets(self) -> None:
        """Clear all widgets from the game tab."""
        for widget in self.tab1.winfo_children():
            widget.destroy()

    def clear_tab2_widgets(self) -> None:
        """Clear all widgets from the leaderboard tab."""
        for widget in self.tab2.winfo_children():
            widget.destroy()

    def create_tab1_widgets(self) -> None:
        """Create all widgets for the game tab."""
        self.clear_tab1_widgets()
        
        canvas1 = tk.Canvas(self.tab1, bg=PALETTE['tabbg'], bd=0)
        canvas1.pack(fill='both', expand=True)

        label_list = ttk.Label(canvas1, text="  ")
        label_list.grid(row=0, column=0, padx=10, pady=10)

        label_list = ttk.Label(canvas1, text="Lista:")
        label_list.grid(row=0, column=1, padx=10, pady=10)

        label_list = ttk.Label(canvas1, text="  ")
        label_list.grid(row=0, column=2, padx=10, pady=10)

        self.listbox_content = tk.Listbox(canvas1, width=25, height=30, font=(FONT_STYLE, FONT_SIZE), bd=0)
        self.listbox_content.grid(row=1, column=1, padx=10, pady=10)

        self.text_box = tk.Text(canvas1, width=85, height=15, font=("calibri", 23), bd=0)
        scrollbar = tk.Scrollbar(canvas1, command=self.text_box.yview, bg=PALETTE['button'], relief="flat")
        scrollbar.grid(row=1, column=5, sticky='ns')
        self.text_box.config(yscrollcommand=scrollbar.set)
        self.text_box.grid(row=1, column=3, padx=10, pady=10, columnspan=2)

        ttk.Button(canvas1, text="Salva", command=self.save_file).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(canvas1, text="Carica", command=self.load_file).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(canvas1, text="Fine Round", command=self.end_round).grid(row=4, column=1, padx=1, pady=1)
        ttk.Button(canvas1, text="#", command=self.create_tab1_widgets).grid(row=5, column=1, padx=1, pady=1)

        self.load_list_content()
        
        dropdown_a = tk.OptionMenu(canvas1, self.dropdown_a, *self.options_a)
        dropdown_a.grid(row=2, column=3, padx=10, pady=10)  
        
        dropdown_b = tk.OptionMenu(canvas1, self.dropdown_b, *self.options_b)
        dropdown_b.grid(row=3, column=3, padx=10, pady=10)  
        
        tk.Button(canvas1, text="V", command=self.on_press_v).grid(row=2, column=4, padx=10, pady=10)  
        tk.Button(canvas1, text="F", command=self.on_press_f).grid(row=3, column=4, padx=10, pady=10) 

    def create_tab2_widgets(self) -> None:
        """Create all widgets for the leaderboard tab."""
        self.clear_tab2_widgets()
        
        canvasB = tk.Canvas(self.tab2, bg=PALETTE['tabbg'], bd=0)
        canvasB.pack(fill='both', expand=True)
        
        canvas2 = tk.Canvas(canvasB, bg='white', bd=0, height=800, width=1400)
        canvas2.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(canvasB, text="Update", command=self.create_tab2_widgets).grid(row=1, column=2, padx=10, pady=10) 

        if not self.sta_path or not os.path.exists(self.sta_path):
            # If stats file doesn't exist, show a message in the canvas
            canvas2.create_text(400, 300, anchor=tk.CENTER, 
                              text="No statistics available.\nPlease configure paths in Settings tab.",
                              font=(FONT_STYLE, 12))
            return

        try:
            with open(self.sta_path, "r", encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            canvas2.create_text(400, 300, anchor=tk.CENTER,
                              text=f"Statistics file not found: {self.sta_path}",
                              font=(FONT_STYLE, 12))
            return
        except Exception as e:
            canvas2.create_text(400, 300, anchor=tk.CENTER,
                              text=f"Error reading statistics: {str(e)}",
                              font=(FONT_STYLE, 12))
            return

        if not lines:
            canvas2.create_text(400, 300, anchor=tk.CENTER,
                              text="No statistics data available.",
                              font=(FONT_STYLE, 12))
            return

        # Parse the content and display as grid
        for i, line in enumerate(lines):
            parts = line.strip().split("|")
            if len(parts) != 2:
                continue
            row_label = parts[0]
            values = parts[1].split(";")
            canvas2.create_text(30, 20 + i * 30, anchor=tk.W, text=row_label)
            for j, value in enumerate(values):
                canvas2.create_text(60 + j * 40, 20 + i * 30, anchor=tk.W, text=f"[{value}]")

    def create_tab3_widgets(self) -> None:
        """Create all widgets for the settings tab."""
        canvas3 = tk.Canvas(self.tab3, bg=PALETTE['tabbg'], bd=0)
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

    def load_list_content(self) -> None:
        """Load the list of figures from the file."""
        self.listbox_content.delete(0, tk.END)
        try:
            with open(self.lis_path, "r", encoding='utf-8') as file:
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
            print(self.lis_path)
        except Exception as e:
            print(f"Error reading file: {e}")
    
    def execute_action(self) -> None:
        """Execute the action based on the settings."""
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
        self.lis_path = os.path.join(s1_path, selected_fileA)
        self.pla_path = os.path.join(s2_path, selected_fileB)
        self.sta_path = os.path.join(s3_path, "stats.txt")
        print(self.lis_path)
        print(self.pla_path)
        with open("path.txt", "w", encoding='utf-8') as file:
            content = self.entry_t0.get()
            file.write(content)
        self.load_list_content()
        self.options_a = self.load_list()
        self.options_b = self.load_players()

    def load_file(self) -> None:
        """Load a file into the text box."""
        self.text_box.delete(1.0, tk.END)
        try:
            file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
            with open(file_path, "r", encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    self.text_box.insert(tk.END, line)
        except FileNotFoundError:
            print(self.lis_path)
        except Exception as e:
            print(f"Error reading file: {e}")

    def save_file(self) -> None:
        """Save the text box content to a file."""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            with open(file_path, "w", encoding='utf-8') as file:
                content = self.text_box.get("1.0", tk.END)
                file.write(content)
        except Exception as e:
            print(f"Error writing file: {e}")

    def on_press_v(self) -> None:
        """Handle positive evaluation button press."""
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

    def on_press_f(self) -> None:
        """Handle negative evaluation button press."""
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

    def create_file(self) -> None:
        """Create output file with current evaluation."""
        selected_item_a = self.dropdown_a.get()
        selected_item_b = self.dropdown_b.get()
        button_pressed = self.button_var.get()
        file_content = f"{selected_item_b[:2]};{selected_item_a[:-3]};{button_pressed}"
        with open(FigureLogic.TURN, "w", encoding='utf-8') as file:
            file.write(file_content)

    def load_list(self) -> List[str]:
        """Load list of figures from file."""
        try:
            with open(self.lis_path, "r", encoding='utf-8') as file:
                lines = [line.strip().replace(";", " ") for line in file]
                return [line.split(".")[0] for line in lines]
        except FileNotFoundError:
            print(f"Warning: Could not find file {self.lis_path}")
            return ["#"]

    def load_players(self) -> List[str]:
        """Load list of players from file."""
        try:
            with open(self.pla_path, "r", encoding='utf-8') as file:
                return [line.strip().replace(";", " ") for line in file]
        except FileNotFoundError:
            print(f"Warning: Could not find file {self.pla_path}")
            return ["#"]
    
    def end_round(self) -> None:
        """End the current round and update scores."""
        try:
            base_path = FigureLogic.get_path()
            FigureLogic.refresh(base_path)
        except Exception as e:
            print(f"Error refreshing figures: {e}")

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
