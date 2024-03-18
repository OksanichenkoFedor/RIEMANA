import numpy as np

from res.step.parser.entities.ancestors import Entity, Drawable
from res.step.parser.entities.faces import AdvancedFace

class ClosedShell(Entity, Drawable):
    def extract_data(self, params, data):
        print("ClosedShell: ", params)
        params = np.array(params[1:-1].split(",")).astype("int")
        self.faces = []
        for i in range(len(params)):
            self.faces.append(data[params[i]])

    def check_data(self):
        for face in self.faces:
            if not isinstance(face, AdvancedFace):
                raise ValueError('Expected AdvancedFace, got ', type(face))

        self.min, self.max = np.array([0, 0, 0]), np.array([0, 0, 0])
        for face in self.faces:
            self.min[0], self.max[0] = np.min((face.min[0], self.min[0])), np.max((face.max[0], self.max[0]))
            self.min[1], self.max[1] = np.min((face.min[1], self.min[1])), np.max((face.max[1], self.max[1]))
            self.min[2], self.max[2] = np.min((face.min[2], self.min[2])), np.max((face.max[2], self.max[2]))
        self.coords = None
        for face in self.faces:
            cdata = face.generate_data_for_optimising()

            if self.coords is None:
                self.coords = cdata
            else:
                self.coords = np.concatenate((self.coords,cdata),axis=1)

        print(self.coords.shape)


    def draw(self, axis, color, is_plotting):
        color = np.random.random(3)
        if is_plotting:
            for i in range(self.coords.shape[1]):
                axis.plot(self.coords[0][i], self.coords[1][i], self.coords[2][i], ".", color=color)
        return self.min.reshape((3, 1)), self.max.reshape((3, 1))