# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:49:56 2024

@author: alext
"""
import tkinter as tk
from tkinter import ttk, messagebox
from run_model import run_simulation, save_results
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class CreateToolTip:
    """
    Create a tooltip for a given widget.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.show_tooltip()

    def leave(self, event=None):
        self.hide_tooltip()

    def show_tooltip(self):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=200)
        label.pack(ipadx=1)

    def hide_tooltip(self):
        if self.tw:
            self.tw.destroy()

def validate_input(value, param_type, min_val=None, max_val=None):
    try:
        val = param_type(value)
        if min_val is not None and val < min_val:
            return False
        if max_val is not None and val > max_val:
            return False
        return True
    except ValueError:
        return False

def on_submit(params, figure_canvas):
    try:
        width = int(params['width'])
        height = int(params['height'])
        density = float(params['density'])
        transmission_rate = float(params['transmission_rate'])
        latency_period = int(params['latency_period'])
        infection_duration = int(params['infection_duration'])
        recovery_rate = float(params['recovery_rate'])
        policy = params['policy']
        num_districts = int(params['num_districts'])
        initial_infected = int(params['initial_infected'])
        steps = int(params['steps'])
        
        if not validate_input(width, int, 1) or not validate_input(height, int, 1):
            raise ValueError("Width and height must be positive integers.")
        if not validate_input(density, float, 0.1, 10):
            raise ValueError("Density must be a float between 0.1 and 10.")
        if not validate_input(transmission_rate, float, 0.0, 1.0):
            raise ValueError("Transmission rate must be a float between 0.0 and 1.0.")
        if not validate_input(latency_period, int, 1):
            raise ValueError("Latency period must be a positive integer.")
        if not validate_input(infection_duration, int, 1):
            raise ValueError("Infection duration must be a positive integer.")
        if not validate_input(recovery_rate, float, 0.0, 1.0):
            raise ValueError("Recovery rate must be a float between 0.0 and 1.0.")
        if not validate_input(num_districts, int, 1):
            raise ValueError("Number of districts must be a positive integer.")
        if not validate_input(initial_infected, int, 0):
            raise ValueError("Initial infected must be a non-negative integer.")
        if not validate_input(steps, int, 1):
            raise ValueError("Steps must be a positive integer.")
        
        results = run_simulation(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected, steps)
        
        output_dir = params['output_dir']
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        csv_filename = f"{output_dir}/results_{policy.replace(' ', '_').lower()}.csv"
        save_results(results, csv_filename)
        print(f"Results saved to {csv_filename}")
        
        # Plotting results
        fig, ax = plt.subplots()
        results.plot(ax=ax, title=f"Policy: {policy}")
        
        # Clear the old plot and display the new one
        for widget in figure_canvas.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=figure_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def create_gui():
    root = tk.Tk()
    root.title("Epi-Simulator GUI")

    # Load and display logo
    logo = Image.open("C:/Users/alext/Documents/GitHub/Epi-Simulator/Epi-Simulator/Simulator/UVA logo.png")
    logo = logo.resize((150, 150), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(root, image=logo)
    logo_label.image = logo
    logo_label.grid(row=0, columnspan=2, pady=10)

    params = {
        'width': tk.StringVar(value="10"),
        'height': tk.StringVar(value="10"),
        'density': tk.StringVar(value="8"),
        'transmission_rate': tk.StringVar(value="0.4"),
        'latency_period': tk.StringVar(value="15"),
        'infection_duration': tk.StringVar(value="50"),
        'recovery_rate': tk.StringVar(value="0.3"),
        'policy': tk.StringVar(value="No Interventions"),
        'num_districts': tk.StringVar(value="5"),
        'initial_infected': tk.StringVar(value="50"),
        'steps': tk.StringVar(value="500"),
        'output_dir': tk.StringVar(value="results")
    }

    tooltips = {
        'width': "Width of the grid (positive integer).",
        'height': "Height of the grid (positive integer).",
        'density': "Density of the agents (float between 0.1 and 10).",
        'transmission_rate': "Probability of transmission per contact (float between 0.0 and 1.0).",
        'latency_period': "Number of steps an agent stays in the exposed state (positive integer).",
        'infection_duration': "Number of steps an agent stays in the infected state (positive integer).",
        'recovery_rate': "Probability of recovering from the infected state (float between 0.0 and 1.0).",
        'policy': "Policy applied to agents.",
        'num_districts': "Number of districts in the environment (positive integer).",
        'initial_infected': "Number of initially infected agents (non-negative integer).",
        'steps': "Number of steps to simulate (positive integer).",
        'output_dir': "Directory to save the results."
    }

    row = 1
    for param, var in params.items():
        tk.Label(root, text=f"{param.replace('_', ' ').title()}:").grid(row=row, column=0)
        entry = tk.Entry(root, textvariable=var)
        entry.grid(row=row, column=1)
        CreateToolTip(entry, tooltips[param])
        row += 1

    policy_combobox = ttk.Combobox(root, textvariable=params['policy'], values=["No Interventions", "Lockdown Only", "Mask Policy Only", "Combination of Lockdown and Mask Policy", "Mayor"])
    policy_combobox.grid(row=7, column=1)
    CreateToolTip(policy_combobox, tooltips['policy'])

    submit_button = tk.Button(root, text="Run Simulation", command=lambda: on_submit(params, figure_canvas))
    submit_button.grid(row=row, columnspan=2, pady=10)

    figure_canvas = tk.Frame(root)
    figure_canvas.grid(row=row + 1, columnspan=2, pady=10)

    # Add copyright information at the bottom
    copyright_label = tk.Label(root, text="© 2024 Agent Based Modeling Course, Group 8. All rights reserved.", font=("Helvetica", 10))
    copyright_label.grid(row=row + 2, columnspan=2, pady=10)

    root.mainloop()

create_gui()


