import numpy as np


class Rotation:

    def degree_to_radius(self, the):
        return [np.pi*t/180. for t in the]

    def make_rotation_matrix_xyz(self, the):

        Rx = np.array([[1., 0., 0.],
                    [0., np.cos(the[0]), -np.sin(the[0])],
                    [0., np.sin(the[0]), np.cos(the[0])]])

        Ry = np.array([[np.cos(the[1]), 0., np.sin(the[1])],
                    [0., 1., 0.],
                    [-np.sin(the[1]), 0., np.cos(the[1])]])

        Rz = np.array([[np.cos(the[2]), -np.sin(the[2]), 0.],
                    [np.sin(the[2]), np.cos(the[2]), 0.],
                    [0., 0., 1.]])

        return np.dot(Rz, np.dot(Ry, Rx))

    def make_rotation_matrix_bunge(self, the):

        R1 = np.array([
            [np.cos(the[0]), np.sin(the[0]), 0.],
            [-np.sin(the[0]), np.cos(the[0]), 0.],
            [0., 0., 1]
        ])

        R2 = np.array([
            [1., 0., 0.],
            [0., np.cos(the[1]), np.sin(the[1])],
            [0., -np.sin(the[1]), np.cos(the[1])]
        ])

        R3 = np.array([
            [np.cos(the[2]), np.sin(the[2]), 0.],
            [-np.sin(the[2]), np.cos(the[2]), 0.],
            [0., 0., 1]
        ])

        return np.dot(R3, np.dot(R2, R1))

    def make_rotation_matrix(self, the, rot_type):

        if rot_type == 'Bunge':
            R = self.make_rotation_matrix_bunge(the)
        else:
            R = self.make_rotation_matrix_xyz(the)

        return R
