from abc import ABC, abstractmethod
import numpy as np


class Entity(ABC):
    def __init__(self, id, params, data):
        self.id = id
        self.extract_data(params, data)
        self.check_data()

    @abstractmethod
    def extract_data(self, params, data):
        pass

    @abstractmethod
    def check_data(self):
        pass


class Curve(Entity):

    @abstractmethod
    def extract_data(self, params, data):
        pass

    @abstractmethod
    def check_data(self):
        pass

    @abstractmethod
    def generate_draw_function(self, start_point, end_point):
        pass

    @abstractmethod
    def give_coords(self, number_points, start_coord, end_coord, orientation):
        pass


class Edge(Entity):

    @abstractmethod
    def extract_data(self, params, data):
        pass

    @abstractmethod
    def check_data(self):
        pass


class Surface(Entity):

    @abstractmethod
    def extract_data(self, params, data):
        pass

    @abstractmethod
    def check_data(self):
        pass


class Drawable(ABC):

    @abstractmethod
    def draw(self, axis, color, is_plotting):
        return np.array([0, 0, 0]).reshape((3, 1)), np.array([0, 0, 0]).reshape((3, 1))
