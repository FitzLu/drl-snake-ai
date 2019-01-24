import numpy as np
from env.pixel import Pixel

class Environment(object):

    def __init__(self, width, height, pixel_size):
        self.pixels = None
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self._build()
    

    def _build(self):
        w = self.width // self.pixel_size
        h = self.height // self.pixel_size
        self.pixels = np.zeros((w, h))
        for i in range(0, w):
            self.pixels[i, 0] = Pixel.WALL
            self.pixels[i, h - 1] = Pixel.WALL
        for j in range(0, h):
            self.pixels[0, j] = Pixel.WALL
            self.pixels[w - 1, j] = Pixel.WALL


    def read_pixel(self, x, y):
        return self.pixels[x, y]


    def write_pixel(self, px, px_type):
        self.pixels[px.x, px.y] = px_type


    @property
    def pixel_total_count(self):
        w, h = np.shape(self.pixels)
        return w * h


    @property
    def shape(self):
        return np.shape(self.pixels)

    
    def reset(self):
        self._build()