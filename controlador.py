from tkinter import Tk
from vista import *


class Controlador:
    if __name__ == "__main__":
        master = Tk()
        objeto = Ventana(master, "Stock.db")
        master.mainloop()

Controlador()