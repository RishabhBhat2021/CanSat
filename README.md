# CanSat
This App is developed by Rishabh Bhat for the CanSat 2021 Ground Control System (GCS).

This App reads arduino data from the serial port, the data is then saved in a csv file,
Then the data from the csv file is read using pandas, and then ploted with matplot, 
the plot is embedded into the tkiner GUI.

The arduino_cansat folder contains arduino_cansat.ino file, which contains the code 
for arduino to generate dummy data for the Project 