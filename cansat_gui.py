from arduino_data import ArduinoData

from cansat_graph import *

import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

LARGE_FONT = ("Helvetica", 30)
MEDIUM_FONT = ("Helvetica", 20)


class CansatGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  
        tk.Tk.title(self, "Space-Men Ground Control System")
        tk.Tk.iconbitmap(self, default="logo_images/logo.ico")

        heading_frame = tk.Frame(self)  
        heading_frame.pack(padx=10, pady=10, side=tk.TOP, expand=True)

        heading_label = tk.Label(heading_frame, text="Space-Men   Ground Control System", font=LARGE_FONT) 
        heading_label.pack(padx=10, side=tk.RIGHT)
        
        # Use self.image_name for images, else image doesn't show up , only blank space appears
        self.team_logo = Image.open("logo_images/cansat_logo.png")
        self.team_logo = self.team_logo.resize((90, 40), Image.ANTIALIAS)
        self.team_logo = ImageTk.PhotoImage(self.team_logo)
        self.logo_label = tk.Label(heading_frame, image=self.team_logo)
        self.logo_label.pack(padx=10, side=tk.LEFT)

        quit_button = ttk.Button(self, text="Quit", command=quit)
        quit_button.pack(pady=(0,10), side=tk.BOTTOM)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, RawData, DeveloperInfo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Frame for Buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(padx=10, pady=10, side=tk.BOTTOM)

        raw_data_button = ttk.Button(buttons_frame, text="Show Raw Data", command=lambda: controller.show_frame(RawData))
        raw_data_button.pack(padx=10, side=tk.LEFT)

        dev_info_button = ttk.Button(buttons_frame, text="Developer Information", command=lambda: controller.show_frame(DeveloperInfo))
        dev_info_button.pack(padx=10, side=tk.LEFT)

        # Graph Canvas
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class RawData(tk.Frame, ArduinoData):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ArduinoData.__init__(self)

        heading_label = tk.Label(self, text="Raw Telemetry Data", font=MEDIUM_FONT) 
        heading_label.pack(padx=10, pady=10)

        home_button = ttk.Button(self, text="Go to Home Screen", command=lambda: controller.show_frame(StartPage))
        home_button.pack(padx=10, pady=10, side=tk.BOTTOM)

        # make a scrollbar
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Creating a Text box to display the raw telemetry
        self.text_box = tk.Text(self)
        self.text_box.pack(fill="both", expand=True)
        # Configuring the Text Box
        self.text_box.config(yscrollcommand=scrollbar.set)
        # Configuring the ScrollBar
        scrollbar.config(command=self.text_box.yview)

        self.display_telemetry()

    def display_telemetry(self):
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, "Altitude, Temperature, Velocity, Pressure, Duration\n")
        self.text_box.insert(tk.END, ArduinoData.get_arduino_data(self))
        self.text_box.see(tk.END)

        self.after(1000, self.display_telemetry)


class DeveloperInfo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        dev_heading_label = tk.Label(self, text="Developer Information", font=MEDIUM_FONT)
        dev_heading_label.pack(padx=10, pady=10)

        info_label = tk.Label(self, text="Rishabh Bhat", font=MEDIUM_FONT)
        info_label.pack(padx=10, pady=10)

        home_button = ttk.Button(self, text="Go to Home Screen", command=lambda: controller.show_frame(StartPage))
        home_button.pack(padx=10, pady=10, side=tk.BOTTOM)
