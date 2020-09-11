import plotly.graph_objs as go
import numpy as np

from .rotation import Rotation


class FCC:
    def __init__(self):
        self.nVertex = 13
        self.nSlips = 1
        self.point_vec0 = np.zeros((3, self.nVertex), dtype='float')
        self.point_vec = np.zeros((3, self.nVertex), dtype='float')
        self.slip_direc = np.zeros((3, self.nSlips), dtype='float')
        self.c_axis = np.zeros(3, dtype='float')
        # Initial vertex
        self.point_vec0[:, 0] = [0.5, -0.5, 0.5]
        self.point_vec0[:, 1] = [0.5, 0.5, 0.5]
        self.point_vec0[:, 2] = [-0.5, 0.5, 0.5]
        self.point_vec0[:, 3] = [-0.5, -0.5, 0.5]
        self.point_vec0[:, 4] = [0.5, -0.5, -0.5]
        self.point_vec0[:, 5] = [0.5, 0.5, -0.5]
        self.point_vec0[:, 6] = [-0.5, 0.5, -0.5]
        self.point_vec0[:, 7] = [-0.5, -0.5, -0.5]
        self.point_vec0[:, 8] = [0., 0., 0.5]
        self.point_vec0[:, 9] = [0., 0., -0.5]
        self.point_vec0[:,10] = [0.3, 0., 0.]
        self.point_vec0[:,11] = [0., 0.3, 0.]
        self.point_vec0[:,12] = [0., 0., 0.3]
        # Vertex
        self.point_vec = self.point_vec0.copy()
        # Slip direction
        self.set_slip_direction()
        # c-axis
        self.set_c_axis()
        # Set graph object
        self.set_graph_object()
        # Set rotation class
        self.rot = Rotation()
        # Set basis
        self.set_crystal_basis()

    def update(self, the, rot_type):
        # Rotate
        self.rotate(the, rot_type)
        # Slip direction
        self.set_slip_direction()
        # c-axis
        self.set_c_axis()
        # Set graph object
        self.set_graph_object()

    def set_slip_direction(self):
        self.slip_direc[:, 0] = self.point_vec[:, 4] - self.point_vec[:, 6]

    def set_c_axis(self):
        self.c_axis = self.point_vec[:, 8] - self.point_vec[:, 9]

    def rotate(self, the, rot_type, *, degree=True):

        if degree:
            the = self.rot.degree_to_radius(the)

        R = self.rot.make_rotation_matrix(the, rot_type)

        for i in range(self.nVertex):
            self.point_vec[:, i] = R.dot(self.point_vec0[:, i])

        self.set_slip_direction()
        self.set_c_axis()

    def set_graph_object(self):

        go_side = go.Scatter3d(
            x=[self.point_vec[0, 0],
               self.point_vec[0, 1],
               self.point_vec[0, 2],
               self.point_vec[0, 3],
               self.point_vec[0, 0]],
            y=[self.point_vec[1, 0],
               self.point_vec[1, 1],
               self.point_vec[1, 2],
               self.point_vec[1, 3],
               self.point_vec[1, 0]],
            z=[self.point_vec[2, 0],
               self.point_vec[2, 1],
               self.point_vec[2, 2],
               self.point_vec[2, 3],
               self.point_vec[2, 0]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_bottom = go.Scatter3d(
            x=[self.point_vec[0, 4],
               self.point_vec[0, 5],
               self.point_vec[0, 6],
               self.point_vec[0, 7],
               self.point_vec[0, 4]],
            y=[self.point_vec[1, 4],
               self.point_vec[1, 5],
               self.point_vec[1, 6],
               self.point_vec[1, 7],
               self.point_vec[1, 4]],
            z=[self.point_vec[2, 4],
               self.point_vec[2, 5],
               self.point_vec[2, 6],
               self.point_vec[2, 7],
               self.point_vec[2, 4]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_1 = go.Scatter3d(
            x=[self.point_vec[0, 0], self.point_vec[0, 4]],
            y=[self.point_vec[1, 0], self.point_vec[1, 4]],
            z=[self.point_vec[2, 0], self.point_vec[2, 4]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_2 = go.Scatter3d(
            x=[self.point_vec[0, 1], self.point_vec[0, 5]],
            y=[self.point_vec[1, 1], self.point_vec[1, 5]],
            z=[self.point_vec[2, 1], self.point_vec[2, 5]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_3 = go.Scatter3d(
            x=[self.point_vec[0, 2], self.point_vec[0, 6]],
            y=[self.point_vec[1, 2], self.point_vec[1, 6]],
            z=[self.point_vec[2, 2], self.point_vec[2, 6]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_4 = go.Scatter3d(
            x=[self.point_vec[0, 3], self.point_vec[0, 7]],
            y=[self.point_vec[1, 3], self.point_vec[1, 7]],
            z=[self.point_vec[2, 3], self.point_vec[2, 7]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_axis_x = go.Scatter3d(
            x=[0., self.point_vec[0,10]],
            y=[0., self.point_vec[1,10]],
            z=[0., self.point_vec[2,10]],
            line = dict(width = 6, color='red'),
            showlegend=False
        )

        go_axis_y = go.Scatter3d(
            x=[0., self.point_vec[0,11]],
            y=[0., self.point_vec[1,11]],
            z=[0., self.point_vec[2,11]],
            line = dict(width = 6, color='blue'),
            showlegend=False
        )

        go_axis_z = go.Scatter3d(
            x=[0., self.point_vec[0,12]],
            y=[0., self.point_vec[1,12]],
            z=[0., self.point_vec[2,12]],
            line = dict(width = 6, color='green'),
            showlegend=False
        )

        self.data_go = [go_side, go_bottom, go_side_1, go_side_2, go_side_3, go_side_4, go_axis_x, go_axis_y, go_axis_z]

    def set_crystal_basis(self):

        self.base_s = np.zeros((3, 12))
        self.base_m = np.zeros((3, 12))

        # set slip direction vector
        self.base_s[0, 0] =  0.0000000000000000
        self.base_s[1, 0] = -0.7071067811865475
        self.base_s[2, 0] =  0.7071067811865475

        self.base_s[0, 1] =  0.7071067811865475
        self.base_s[1, 1] =  0.0000000000000000
        self.base_s[2, 1] =  0.7071067811865475

        self.base_s[0, 2] =  0.7071067811865475
        self.base_s[1, 2] =  0.7071067811865475
        self.base_s[2, 2] =  0.0000000000000000

        self.base_s[0, 3] =  0.0000000000000000
        self.base_s[1, 3] = -0.7071067811865475
        self.base_s[2, 3] =  0.7071067811865475

        self.base_s[0, 4] = -0.7071067811865475
        self.base_s[1, 4] =  0.0000000000000000
        self.base_s[2, 4] =  0.7071067811865475

        self.base_s[0, 5] = -0.7071067811865475
        self.base_s[1, 5] =  0.7071067811865475
        self.base_s[2, 5] =  0.0000000000000000

        self.base_s[0, 6] =  0.0000000000000000
        self.base_s[1, 6] =  0.7071067811865475
        self.base_s[2, 6] =  0.7071067811865475

        self.base_s[0, 7] =  0.7071067811865475
        self.base_s[1, 7] =  0.0000000000000000
        self.base_s[2, 7] =  0.7071067811865475

        self.base_s[0, 8] = -0.7071067811865475
        self.base_s[1, 8] =  0.7071067811865475
        self.base_s[2, 8] =  0.0000000000000000

        self.base_s[0, 9] =  0.0000000000000000
        self.base_s[1, 9] =  0.7071067811865475
        self.base_s[2, 9] =  0.7071067811865475

        self.base_s[0,10] = -0.7071067811865475
        self.base_s[1,10] =  0.0000000000000000
        self.base_s[2,10] =  0.7071067811865475

        self.base_s[0,11] =  0.7071067811865475
        self.base_s[1,11] =  0.7071067811865475
        self.base_s[2,11] =  0.0000000000000000

        # set normal to slip direction vector
        self.base_m[0, 0] = -0.5773502691896257
        self.base_m[1, 0] =  0.5773502691896257
        self.base_m[2, 0] =  0.5773502691896257

        self.base_m[0, 1] = -0.5773502691896257
        self.base_m[1, 1] =  0.5773502691896257
        self.base_m[2, 1] =  0.5773502691896257

        self.base_m[0, 2] = -0.5773502691896257
        self.base_m[1, 2] =  0.5773502691896257
        self.base_m[2, 2] =  0.5773502691896257

        self.base_m[0, 3] =  0.5773502691896257
        self.base_m[1, 3] =  0.5773502691896257
        self.base_m[2, 3] =  0.5773502691896257

        self.base_m[0, 4] =  0.5773502691896257
        self.base_m[1, 4] =  0.5773502691896257
        self.base_m[2, 4] =  0.5773502691896257

        self.base_m[0, 5] =  0.5773502691896257
        self.base_m[1, 5] =  0.5773502691896257
        self.base_m[2, 5] =  0.5773502691896257

        self.base_m[0, 6] = -0.5773502691896257
        self.base_m[1, 6] = -0.5773502691896257
        self.base_m[2, 6] =  0.5773502691896257

        self.base_m[0, 7] = -0.5773502691896257
        self.base_m[1, 7] = -0.5773502691896257
        self.base_m[2, 7] =  0.5773502691896257

        self.base_m[0, 8] = -0.5773502691896257
        self.base_m[1, 8] = -0.5773502691896257
        self.base_m[2, 8] =  0.5773502691896257

        self.base_m[0, 9] =  0.5773502691896257
        self.base_m[1, 9] = -0.5773502691896257
        self.base_m[2, 9] =  0.5773502691896257

        self.base_m[0,10] =  0.5773502691896257
        self.base_m[1,10] = -0.5773502691896257
        self.base_m[2,10] =  0.5773502691896257

        self.base_m[0,11] =  0.5773502691896257
        self.base_m[1,11] = -0.5773502691896257
        self.base_m[2,11] =  0.5773502691896257
