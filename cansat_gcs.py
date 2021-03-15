import threading

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use('TkAgg')  # Backend for matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

from PIL import ImageTk, Image

import serial

import random

LARGE_FONT = ("Helvetica", 30)
MEDIUM_FONT = ("Helvetica", 20)
style.use('seaborn')  # Change the Graph style - seaborn

fig = Figure(figsize=(10,10), dpi=100)

altitude_plot = fig.add_subplot(221)
temperature_plot = fig.add_subplot(222)
speed_plot = fig.add_subplot(223)
pressure_plot = fig.add_subplot(224)

data_to_display = ""
want_to_read = True

my_list = []
y_list = []

def get_data():

    global data_to_display
    global want_to_read
    global my_list
    global y_list

    # timeout=0 makes sure the this while loop doesnt block other part of the code  
    arduinoSerialData = serial.Serial('com7', 9600, timeout=0, writeTimeout=0)  #9600 is the Baudrate

    while want_to_read == True:
        if (arduinoSerialData.inWaiting()>0):  # Only proceeds when there is something from arduino
            myData = arduinoSerialData.readline()
            print(myData.decode())

            data_to_display = data_to_display + myData.decode()

            ele_list = myData.decode().split(" ")
            
            if len(ele_list) > 3:
                last_element = ele_list[4]
                my_list.append(int(last_element))
                y_list.append(10*int(last_element) + 10*random.randint(-10,10))
                

def animate(i):

    global my_list
    global y_list

    xList = my_list
    yList = y_list

    # Clean the plot first
    altitude_plot.clear()  
    temperature_plot.clear()
    speed_plot.clear()
    pressure_plot.clear()

    altitude_plot.plot(xList, yList, label="Altitude", color="orange")
    temperature_plot.plot(xList, yList, label="Temperature", color="navy")
    speed_plot.plot(xList, yList, label="Speed", color="green")
    pressure_plot.plot(xList, yList, label="Pressure", color="red")

    # Showing the Legend for the graphs
    altitude_plot.legend() 
    temperature_plot.legend()
    speed_plot.legend()
    pressure_plot.legend()


class CansatApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.config(self)  
        tk.Tk.wm_title(self, "Space-Men Ground Control System")
        tk.Tk.iconbitmap(self, default="logo.ico")

        heading_frame = tk.Frame(self)  
        heading_frame.pack(padx=10, pady=10, side=tk.TOP, expand=True)

        heading_label = tk.Label(heading_frame, text="Space-Men   Ground Control System", font=LARGE_FONT) 
        heading_label.pack(padx=10, side=tk.RIGHT)
        
        # Use self.image_name for images, else image doesn't show up , only blank space appears
        self.team_logo = Image.open("cansat_logo.png")
        self.team_logo = self.team_logo.resize((90, 40), Image.ANTIALIAS)
        self.team_logo = ImageTk.PhotoImage(self.team_logo)
        self.logo_label = tk.Label(heading_frame, image=self.team_logo)
        self.logo_label.pack(padx=10, side=tk.LEFT)

        quit_button = ttk.Button(self, text="Quit", command=self.close_app)
        quit_button.pack(pady=(0,10), side=tk.BOTTOM)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # MENU BAR for the App
        menu_bar = tk.Menu(container)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save Settings")
        menu_bar.add_cascade(label="File", menu=file_menu) 

        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Quit", command=quit)
        menu_bar.add_cascade(label="Exit & Quit", menu=options_menu)

        tk.Tk.config(self, menu=menu_bar)

        self.frames = {}

        for F in (StartPage, DeveloperInfo, RawData):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
    def close_app(self):
    
        global want_to_read

        want_to_read = False
        quit()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        tk.Frame.config(self)
        
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


class RawData(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        heading_label = tk.Label(self, text="Raw Telemetry Data", font=MEDIUM_FONT) 
        heading_label.pack(padx=10, pady=10)

        home_button = ttk.Button(self, text="Go to Home Screen", command=lambda: controller.show_frame(StartPage))
        home_button.pack(padx=10, pady=10, side=tk.BOTTOM)

        # make a scrollbar
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Creating a Text box to display the raw telemetry
        self.log_display = tk.Text(self)
        self.log_display.pack(fill="both", expand=True)
        # Configuring the Text Box
        self.log_display.config(yscrollcommand=scrollbar.set)
        # Configuring the ScrollBar
        scrollbar.config(command=self.log_display.yview)

        self.update_textbox()

    def update_textbox(self):

        global data_to_display

        self.log_display.delete(1.0,tk.END)
        self.log_display.insert(tk.END, data_to_display)
        self.log_display.see(tk.END)

        # Set timer 
	    # 1 second = 1000
        self.after(1000, self.update_textbox)


class DeveloperInfo(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        dev_heading_label = tk.Label(self, text="Developer Information", font=MEDIUM_FONT)
        dev_heading_label.pack(padx=10, pady=10)

        info_label = tk.Label(self, text="Rishabh Bhat", font=MEDIUM_FONT)
        info_label.pack(padx=10, pady=10)

        home_button = ttk.Button(self, text="Go to Home Screen", command=lambda: controller.show_frame(StartPage))
        home_button.pack(padx=10, pady=10, side=tk.BOTTOM)


def main():

    try:
        # timeout=0 makes sure the this while loop doesnt block other part of the code  
        serial.Serial('com7', 9600, timeout=0, writeTimeout=0)  #9600 is the Baudrate
        
        thread1 = threading.Thread(target=get_data)
        thread1.start()

    except:
        print("Error: Arduino Not Connected")
        quit()

    app = CansatApp()
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    app.mainloop()

if __name__ == "__main__":
    main()