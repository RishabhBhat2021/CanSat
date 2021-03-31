from cansat_gui import *

def main():
    app = CansatGui()
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    app.mainloop()

if __name__ == "__main__":
    main()