# CanSat
This App is developed by Rishabh Bhat for the Ground Control System (GCS).

This App reads arduino data from the serial port, the data is then saved to a csv file,
Then the data from the csv file is read using pandas, and then plotted with matplot, 
the plot is embedded into the tkinter GUI.

The arduino_cansat folder contains arduino_cansat.ino file, which contains the code 
for arduino to generate dummy data for the Project.

The logo_images folder contains logo for my team Space-Men.

![Screenshot (1)](https://user-images.githubusercontent.com/79303308/115732774-e8775c80-a3a5-11eb-9996-c72953657d2f.png)
Home Page, This data is randomly generated

![Screenshot (2)](https://user-images.githubusercontent.com/79303308/115732834-f7f6a580-a3a5-11eb-8d96-71714199674f.png)
This Page displays the Raw Telemetry Data

