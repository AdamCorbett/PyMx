import tkinter as tk
import pygubu

class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('canvas.ui')
        self.mainwindow = builder.get_object('frame_main', master)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)

    canvas = app.builder.get_object('canvas_img', app.mainwindow)
    canvas.create_polygon([50,50,100,50,150,100,50,150], outline='red', width=2)
    canvas.pack()

    root.mainloop()
