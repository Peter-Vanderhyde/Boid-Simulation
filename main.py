import tkinter
import threading
import random


if __name__ == "__main__":
    window = tkinter.Tk()

    canvas = tkinter.Canvas(window, background="white", width=1100, height=600)
    canvas.pack()

    window.mainloop()