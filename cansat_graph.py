import matplotlib
matplotlib.use('TkAgg')  # Backend for matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import pandas as pd

style.use('seaborn')  # Change the Graph style - seaborn

fig = Figure(figsize=(10,10), dpi=100)

altitude_plot = fig.add_subplot(221)
temperature_plot = fig.add_subplot(222)
speed_plot = fig.add_subplot(223)
pressure_plot = fig.add_subplot(224)

def animate(i):
    try:
        arduino_data = pd.read_csv("data.csv")

        altitude = arduino_data["Altitude"]
        temperature = arduino_data["Temperature"]
        velocity = arduino_data["Velocity"]
        pressure = arduino_data["Pressure"]
        duration = arduino_data["Duration"]

        # Clean the plot first
        altitude_plot.clear()  
        temperature_plot.clear()
        speed_plot.clear()
        pressure_plot.clear()

        altitude_plot.plot(duration, altitude, label="Altitude (m)", color="orange")
        temperature_plot.plot(duration, temperature, label="Temperature (`C)", color="navy")
        speed_plot.plot(duration, velocity, label="Speed (m/s)", color="green")
        pressure_plot.plot(duration, pressure, label="Pressure (atm)", color="red")

        # Showing the Legend for the graphs
        altitude_plot.legend() 
        temperature_plot.legend()
        speed_plot.legend()
        pressure_plot.legend()

    except:
        pass
