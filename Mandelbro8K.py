import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from tkinter import Tk, Button

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z**2 + c
        n += 1
    return n

class MandelbrotPlotter:
    def __init__(self, width, height, x_min, x_max, y_min, y_max, max_iter, num_threads):
        self.width = width
        self.height = height
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self.max_iter = max_iter
        self.num_threads = num_threads

        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        self.im = None
        self.reset_button = Button(self.fig.canvas.get_tk_widget().master, text="Reset", command=self.reset_image)
        self.reset_button.pack(side='top')

        self.generate_mandelbrot()

    def generate_mandelbrot_row(self, args):
        row, y, width = args
        c = np.full(width, y) + 1j * np.linspace(self.x_min, self.x_max, width)
        return np.vectorize(lambda c: mandelbrot(c, self.max_iter))(c)

    def generate_mandelbrot(self):
        y_values = np.linspace(self.y_min, self.y_max, self.height)
        args_list = [(row, y, self.width) for row, y in enumerate(y_values)]

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            results = list(executor.map(self.generate_mandelbrot_row, args_list))

        mandelbrot_set = np.vstack(results)
        if self.im is not None:
            self.im.set_data(mandelbrot_set)
        else:
            self.im = self.ax.imshow(mandelbrot_set, cmap='viridis', extent=(self.x_min, self.x_max, self.y_min, self.y_max))
            plt.colorbar(self.im)
            plt.title('Mandelbrot Set')
        self.fig.canvas.draw()

    def reset_image(self):
        self.generate_mandelbrot()

if __name__ == "__main__":
    width, height = 7680, 4320  # 8k resolution
    x_min, x_max = -2, 2
    y_min, y_max = -2, 2
    max_iter = 100
    num_threads = 32 #Remember to configure the threads of your processor, mine is a Ryzen 9 5950X 32-threads.

    plotter = MandelbrotPlotter(width, height, x_min, x_max, y_min, y_max, max_iter, num_threads)
    plt.show()
