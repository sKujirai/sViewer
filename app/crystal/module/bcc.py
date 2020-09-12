import plotly.graph_objs as go
import numpy as np

from .rotation import Rotation


class BCC:
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
        self.point_vec0[:, 10] = [0.3, 0., 0.]
        self.point_vec0[:, 11] = [0., 0.3, 0.]
        self.point_vec0[:, 12] = [0., 0., 0.3]
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
            line=dict(width=6, color='black'),
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
            line=dict(width=6, color='black'),
            showlegend=False
        )

        go_side_1 = go.Scatter3d(
            x=[self.point_vec[0, 0], self.point_vec[0, 4]],
            y=[self.point_vec[1, 0], self.point_vec[1, 4]],
            z=[self.point_vec[2, 0], self.point_vec[2, 4]],
            line=dict(width=6, color='black'),
            showlegend=False
        )

        go_side_2 = go.Scatter3d(
            x=[self.point_vec[0, 1], self.point_vec[0, 5]],
            y=[self.point_vec[1, 1], self.point_vec[1, 5]],
            z=[self.point_vec[2, 1], self.point_vec[2, 5]],
            line=dict(width=6, color='black'),
            showlegend=False
        )

        go_side_3 = go.Scatter3d(
            x=[self.point_vec[0, 2], self.point_vec[0, 6]],
            y=[self.point_vec[1, 2], self.point_vec[1, 6]],
            z=[self.point_vec[2, 2], self.point_vec[2, 6]],
            line=dict(width=6, color='black'),
            showlegend=False
        )

        go_side_4 = go.Scatter3d(
            x=[self.point_vec[0, 3], self.point_vec[0, 7]],
            y=[self.point_vec[1, 3], self.point_vec[1, 7]],
            z=[self.point_vec[2, 3], self.point_vec[2, 7]],
            line=dict(width=6, color='black'),
            showlegend=False
        )

        go_axis_x = go.Scatter3d(
            x=[0., self.point_vec[0, 10]],
            y=[0., self.point_vec[1, 10]],
            z=[0., self.point_vec[2, 10]],
            line=dict(width=6, color='red'),
            showlegend=False
        )

        go_axis_y = go.Scatter3d(
            x=[0., self.point_vec[0, 11]],
            y=[0., self.point_vec[1, 11]],
            z=[0., self.point_vec[2, 11]],
            line=dict(width=6, color='blue'),
            showlegend=False
        )

        go_axis_z = go.Scatter3d(
            x=[0., self.point_vec[0, 12]],
            y=[0., self.point_vec[1, 12]],
            z=[0., self.point_vec[2, 12]],
            line=dict(width=6, color='green'),
            showlegend=False
        )

        self.data_go = [go_side, go_bottom, go_side_1, go_side_2, go_side_3, go_side_4, go_axis_x, go_axis_y, go_axis_z]

    def set_crystal_basis(self):

        self.base_s = np.zeros((3, 48))
        self.base_m = np.zeros((3, 48))

        # set slip direction vector
        self.base_s[0, 0] = -0.5773502691896257
        self.base_s[1, 0] = 0.5773502691896257
        self.base_s[2, 0] = 0.5773502691896257

        self.base_s[0, 1] = 0.5773502691896257
        self.base_s[1, 1] = -0.5773502691896257
        self.base_s[2, 1] = 0.5773502691896257

        self.base_s[0, 2] = 0.5773502691896257
        self.base_s[1, 2] = 0.5773502691896257
        self.base_s[2, 2] = -0.5773502691896257

        self.base_s[0, 3] = 0.5773502691896257
        self.base_s[1, 3] = 0.5773502691896257
        self.base_s[2, 3] = 0.5773502691896257

        self.base_s[0, 4] = 0.5773502691896257
        self.base_s[1, 4] = 0.5773502691896257
        self.base_s[2, 4] = -0.5773502691896257

        self.base_s[0, 5] = -0.5773502691896257
        self.base_s[1, 5] = 0.5773502691896257
        self.base_s[2, 5] = 0.5773502691896257

        self.base_s[0, 6] = 0.5773502691896257
        self.base_s[1, 6] = -0.5773502691896257
        self.base_s[2, 6] = 0.5773502691896257

        self.base_s[0, 7] = 0.5773502691896257
        self.base_s[1, 7] = 0.5773502691896257
        self.base_s[2, 7] = 0.5773502691896257

        self.base_s[0, 8] = 0.5773502691896257
        self.base_s[1, 8] = 0.5773502691896257
        self.base_s[2, 8] = -0.5773502691896257

        self.base_s[0, 9] = 0.5773502691896257
        self.base_s[1, 9] = -0.5773502691896257
        self.base_s[2, 9] = 0.5773502691896257

        self.base_s[0, 10] = 0.5773502691896257
        self.base_s[1, 10] = 0.5773502691896257
        self.base_s[2, 10] = 0.5773502691896257

        self.base_s[0, 11] = -0.5773502691896257
        self.base_s[1, 11] = 0.5773502691896257
        self.base_s[2, 11] = 0.5773502691896257

        self.base_s[0, 12] = -0.5773502691896257
        self.base_s[1, 12] = -0.5773502691896257
        self.base_s[2, 12] = 0.5773502691896257

        self.base_s[0, 13] = 0.5773502691896257
        self.base_s[1, 13] = 0.5773502691896257
        self.base_s[2, 13] = 0.5773502691896257

        self.base_s[0, 14] = 0.5773502691896257
        self.base_s[1, 14] = -0.5773502691896257
        self.base_s[2, 14] = 0.5773502691896257

        self.base_s[0, 15] = -0.5773502691896257
        self.base_s[1, 15] = 0.5773502691896257
        self.base_s[2, 15] = 0.5773502691896257

        self.base_s[0, 16] = -0.5773502691896257
        self.base_s[1, 16] = 0.5773502691896257
        self.base_s[2, 16] = -0.5773502691896257

        self.base_s[0, 17] = 0.5773502691896257
        self.base_s[1, 17] = 0.5773502691896257
        self.base_s[2, 17] = 0.5773502691896257

        self.base_s[0, 18] = -0.5773502691896257
        self.base_s[1, 18] = 0.5773502691896257
        self.base_s[2, 18] = 0.5773502691896257

        self.base_s[0, 19] = 0.5773502691896257
        self.base_s[1, 19] = 0.5773502691896257
        self.base_s[2, 19] = -0.5773502691896257

        self.base_s[0, 20] = 0.5773502691896257
        self.base_s[1, 20] = -0.5773502691896257
        self.base_s[2, 20] = -0.5773502691896257

        self.base_s[0, 21] = 0.5773502691896257
        self.base_s[1, 21] = 0.5773502691896257
        self.base_s[2, 21] = 0.5773502691896257

        self.base_s[0, 22] = 0.5773502691896257
        self.base_s[1, 22] = 0.5773502691896257
        self.base_s[2, 22] = -0.5773502691896257

        self.base_s[0, 23] = 0.5773502691896257
        self.base_s[1, 23] = -0.5773502691896257
        self.base_s[2, 23] = 0.5773502691896257

        self.base_s[0, 24] = -0.5773502691896257
        self.base_s[1, 24] = -0.5773502691896257
        self.base_s[2, 24] = 0.5773502691896257

        self.base_s[0, 25] = 0.5773502691896257
        self.base_s[1, 25] = -0.5773502691896257
        self.base_s[2, 25] = 0.5773502691896257

        self.base_s[0, 26] = -0.5773502691896257
        self.base_s[1, 26] = 0.5773502691896257
        self.base_s[2, 26] = 0.5773502691896257

        self.base_s[0, 27] = 0.5773502691896257
        self.base_s[1, 27] = 0.5773502691896257
        self.base_s[2, 27] = 0.5773502691896257

        self.base_s[0, 28] = 0.5773502691896257
        self.base_s[1, 28] = 0.5773502691896257
        self.base_s[2, 28] = -0.5773502691896257

        self.base_s[0, 29] = 0.5773502691896257
        self.base_s[1, 29] = -0.5773502691896257
        self.base_s[2, 29] = 0.5773502691896257

        self.base_s[0, 30] = 0.5773502691896257
        self.base_s[1, 30] = 0.5773502691896257
        self.base_s[2, 30] = 0.5773502691896257

        self.base_s[0, 31] = 0.5773502691896257
        self.base_s[1, 31] = 0.5773502691896257
        self.base_s[2, 31] = 0.5773502691896257

        self.base_s[0, 32] = 0.5773502691896257
        self.base_s[1, 32] = -0.5773502691896257
        self.base_s[2, 32] = 0.5773502691896257

        self.base_s[0, 33] = 0.5773502691896257
        self.base_s[1, 33] = 0.5773502691896257
        self.base_s[2, 33] = -0.5773502691896257

        self.base_s[0, 34] = 0.5773502691896257
        self.base_s[1, 34] = 0.5773502691896257
        self.base_s[2, 34] = 0.5773502691896257

        self.base_s[0, 35] = -0.5773502691896257
        self.base_s[1, 35] = 0.5773502691896257
        self.base_s[2, 35] = 0.5773502691896257

        self.base_s[0, 36] = 0.5773502691896257
        self.base_s[1, 36] = -0.5773502691896257
        self.base_s[2, 36] = 0.5773502691896257

        self.base_s[0, 37] = 0.5773502691896257
        self.base_s[1, 37] = 0.5773502691896257
        self.base_s[2, 37] = -0.5773502691896257

        self.base_s[0, 38] = 0.5773502691896257
        self.base_s[1, 38] = 0.5773502691896257
        self.base_s[2, 38] = 0.5773502691896257

        self.base_s[0, 39] = -0.5773502691896257
        self.base_s[1, 39] = 0.5773502691896257
        self.base_s[2, 39] = 0.5773502691896257

        self.base_s[0, 40] = -0.5773502691896257
        self.base_s[1, 40] = 0.5773502691896257
        self.base_s[2, 40] = 0.5773502691896257

        self.base_s[0, 41] = 0.5773502691896257
        self.base_s[1, 41] = 0.5773502691896257
        self.base_s[2, 41] = 0.5773502691896257

        self.base_s[0, 42] = 0.5773502691896257
        self.base_s[1, 42] = 0.5773502691896257
        self.base_s[2, 42] = -0.5773502691896257

        self.base_s[0, 43] = 0.5773502691896257
        self.base_s[1, 43] = -0.5773502691896257
        self.base_s[2, 43] = 0.5773502691896257

        self.base_s[0, 44] = -0.5773502691896257
        self.base_s[1, 44] = 0.5773502691896257
        self.base_s[2, 44] = 0.5773502691896257

        self.base_s[0, 45] = 0.5773502691896257
        self.base_s[1, 45] = 0.5773502691896257
        self.base_s[2, 45] = 0.5773502691896257

        self.base_s[0, 46] = 0.5773502691896257
        self.base_s[1, 46] = 0.5773502691896257
        self.base_s[2, 46] = -0.5773502691896257

        self.base_s[0, 47] = 0.5773502691896257
        self.base_s[1, 47] = -0.5773502691896257
        self.base_s[2, 47] = 0.5773502691896257

        # set normal to slip direction vector
        self.base_m[0, 0] = 0.7071067811865475
        self.base_m[1, 0] = 0.7071067811865475
        self.base_m[2, 0] = 0.0000000000000000

        self.base_m[0, 1] = 0.7071067811865475
        self.base_m[1, 1] = 0.7071067811865475
        self.base_m[2, 1] = 0.0000000000000000

        self.base_m[0, 2] = -0.7071067811865475
        self.base_m[1, 2] = 0.7071067811865475
        self.base_m[2, 2] = 0.0000000000000000

        self.base_m[0, 3] = -0.7071067811865475
        self.base_m[1, 3] = 0.7071067811865475
        self.base_m[2, 3] = 0.0000000000000000

        self.base_m[0, 4] = 0.7071067811865475
        self.base_m[1, 4] = 0.0000000000000000
        self.base_m[2, 4] = 0.7071067811865475

        self.base_m[0, 5] = 0.7071067811865475
        self.base_m[1, 5] = 0.0000000000000000
        self.base_m[2, 5] = 0.7071067811865475

        self.base_m[0, 6] = -0.7071067811865475
        self.base_m[1, 6] = 0.0000000000000000
        self.base_m[2, 6] = 0.7071067811865475

        self.base_m[0, 7] = -0.7071067811865475
        self.base_m[1, 7] = 0.0000000000000000
        self.base_m[2, 7] = 0.7071067811865475

        self.base_m[0, 8] = 0.0000000000000000
        self.base_m[1, 8] = 0.7071067811865475
        self.base_m[2, 8] = 0.7071067811865475

        self.base_m[0, 9] = 0.0000000000000000
        self.base_m[1, 9] = 0.7071067811865475
        self.base_m[2, 9] = 0.7071067811865475

        self.base_m[0, 10] = 0.0000000000000000
        self.base_m[1, 10] = -0.7071067811865475
        self.base_m[2, 10] = 0.7071067811865475

        self.base_m[0, 11] = 0.0000000000000000
        self.base_m[1, 11] = -0.7071067811865475
        self.base_m[2, 11] = 0.7071067811865475

        self.base_m[0, 12] = 0.4082482904638630
        self.base_m[1, 12] = 0.4082482904638630
        self.base_m[2, 12] = 0.8164965809277260

        self.base_m[0, 13] = -0.4082482904638630
        self.base_m[1, 13] = -0.4082482904638630
        self.base_m[2, 13] = 0.8164965809277260

        self.base_m[0, 14] = -0.4082482904638630
        self.base_m[1, 14] = 0.4082482904638630
        self.base_m[2, 14] = 0.8164965809277260

        self.base_m[0, 15] = 0.4082482904638630
        self.base_m[1, 15] = -0.4082482904638630
        self.base_m[2, 15] = 0.8164965809277260

        self.base_m[0, 16] = 0.4082482904638630
        self.base_m[1, 16] = 0.8164965809277260
        self.base_m[2, 16] = 0.4082482904638630

        self.base_m[0, 17] = -0.4082482904638630
        self.base_m[1, 17] = 0.8164965809277260
        self.base_m[2, 17] = -0.4082482904638630

        self.base_m[0, 18] = 0.4082482904638630
        self.base_m[1, 18] = 0.8164965809277260
        self.base_m[2, 18] = -0.4082482904638630

        self.base_m[0, 19] = -0.4082482904638630
        self.base_m[1, 19] = 0.8164965809277260
        self.base_m[2, 19] = 0.4082482904638630

        self.base_m[0, 20] = 0.8164965809277260
        self.base_m[1, 20] = 0.4082482904638630
        self.base_m[2, 20] = 0.4082482904638630

        self.base_m[0, 21] = 0.8164965809277260
        self.base_m[1, 21] = -0.4082482904638630
        self.base_m[2, 21] = -0.4082482904638630

        self.base_m[0, 22] = 0.8164965809277260
        self.base_m[1, 22] = -0.4082482904638630
        self.base_m[2, 22] = 0.4082482904638630

        self.base_m[0, 23] = 0.8164965809277260
        self.base_m[1, 23] = 0.4082482904638630
        self.base_m[2, 23] = -0.4082482904638630

        self.base_m[0, 24] = 0.2672612419124243
        self.base_m[1, 24] = 0.5345224838248487
        self.base_m[2, 24] = 0.8017837257372731

        self.base_m[0, 25] = -0.2672612419124243
        self.base_m[1, 25] = 0.5345224838248487
        self.base_m[2, 25] = 0.8017837257372731

        self.base_m[0, 26] = 0.2672612419124243
        self.base_m[1, 26] = -0.5345224838248487
        self.base_m[2, 26] = 0.8017837257372731

        self.base_m[0, 27] = 0.2672612419124243
        self.base_m[1, 27] = 0.5345224838248487
        self.base_m[2, 27] = -0.8017837257372731

        self.base_m[0, 28] = 0.5345224838248487
        self.base_m[1, 28] = 0.2672612419124243
        self.base_m[2, 28] = 0.8017837257372731

        self.base_m[0, 29] = -0.5345224838248487
        self.base_m[1, 29] = 0.2672612419124243
        self.base_m[2, 29] = 0.8017837257372731

        self.base_m[0, 30] = 0.5345224838248487
        self.base_m[1, 30] = -0.2672612419124243
        self.base_m[2, 30] = 0.8017837257372731

        self.base_m[0, 31] = 0.5345224838248487
        self.base_m[1, 31] = 0.2672612419124243
        self.base_m[2, 31] = -0.8017837257372731

        self.base_m[0, 32] = 0.2672612419124243
        self.base_m[1, 32] = 0.8017837257372731
        self.base_m[2, 32] = 0.5345224838248487

        self.base_m[0, 33] = -0.2672612419124243
        self.base_m[1, 33] = 0.8017837257372731
        self.base_m[2, 33] = 0.5345224838248487

        self.base_m[0, 34] = 0.2672612419124243
        self.base_m[1, 34] = -0.8017837257372731
        self.base_m[2, 34] = 0.5345224838248487

        self.base_m[0, 35] = 0.2672612419124243
        self.base_m[1, 35] = 0.8017837257372731
        self.base_m[2, 35] = -0.5345224838248487

        self.base_m[0, 36] = 0.5345224838248487
        self.base_m[1, 36] = 0.8017837257372731
        self.base_m[2, 36] = 0.2672612419124243

        self.base_m[0, 37] = -0.5345224838248487
        self.base_m[1, 37] = 0.8017837257372731
        self.base_m[2, 37] = 0.2672612419124243

        self.base_m[0, 38] = 0.5345224838248487
        self.base_m[1, 38] = -0.8017837257372731
        self.base_m[2, 38] = 0.2672612419124243

        self.base_m[0, 39] = 0.5345224838248487
        self.base_m[1, 39] = 0.8017837257372731
        self.base_m[2, 39] = -0.2672612419124243

        self.base_m[0, 40] = 0.8017837257372731
        self.base_m[1, 40] = 0.5345224838248487
        self.base_m[2, 40] = 0.2672612419124243

        self.base_m[0, 41] = -0.8017837257372731
        self.base_m[1, 41] = 0.5345224838248487
        self.base_m[2, 41] = 0.2672612419124243

        self.base_m[0, 42] = 0.8017837257372731
        self.base_m[1, 42] = -0.5345224838248487
        self.base_m[2, 42] = 0.2672612419124243

        self.base_m[0, 43] = 0.8017837257372731
        self.base_m[1, 43] = 0.5345224838248487
        self.base_m[2, 43] = -0.2672612419124243

        self.base_m[0, 44] = 0.8017837257372731
        self.base_m[1, 44] = 0.2672612419124243
        self.base_m[2, 44] = 0.5345224838248487

        self.base_m[0, 45] = -0.8017837257372731
        self.base_m[1, 45] = 0.2672612419124243
        self.base_m[2, 45] = 0.5345224838248487

        self.base_m[0, 46] = 0.8017837257372731
        self.base_m[1, 46] = -0.2672612419124243
        self.base_m[2, 46] = 0.5345224838248487

        self.base_m[0, 47] = 0.8017837257372731
        self.base_m[1, 47] = 0.2672612419124243
        self.base_m[2, 47] = -0.5345224838248487
