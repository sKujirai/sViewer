import plotly.graph_objs as go
import numpy as np

from .rotation import Rotation


class HCP:
    def __init__(self):
        self.nVertex = 17
        self.nSlips = 3  # Basal only
        self.point_vec0 = np.zeros((3, self.nVertex), dtype='float')
        self.point_vec = np.zeros((3, self.nVertex), dtype='float')
        self.slip_direc = np.zeros((3, self.nSlips), dtype='float')
        self.c_axis = np.zeros(3, dtype='float')
        # Initial vertex
        self.point_vec0[:, 0] = [np.sqrt(3.)/2., 0., np.sqrt(2.)/2.]
        self.point_vec0[:, 1] = [np.sqrt(3.)/4., 0.75, np.sqrt(2.)/2.]
        self.point_vec0[:, 2] = [-np.sqrt(3.)/4., 0.75, np.sqrt(2.)/2.]
        self.point_vec0[:, 3] = [-np.sqrt(3.)/2., 0., np.sqrt(2.)/2.]
        self.point_vec0[:, 4] = [-np.sqrt(3.)/4., -0.75, np.sqrt(2.)/2.]
        self.point_vec0[:, 5] = [np.sqrt(3.)/4., -0.75, np.sqrt(2.)/2.]
        self.point_vec0[:, 6] = [np.sqrt(3.)/2., 0., -np.sqrt(2.)/2.]
        self.point_vec0[:, 7] = [np.sqrt(3.)/4., 0.75, -np.sqrt(2.)/2.]
        self.point_vec0[:, 8] = [-np.sqrt(3.)/4., 0.75, -np.sqrt(2.)/2.]
        self.point_vec0[:, 9] = [-np.sqrt(3.)/2., 0., -np.sqrt(2.)/2.]
        self.point_vec0[:,10] = [-np.sqrt(3.)/4., -0.75, -np.sqrt(2.)/2.]
        self.point_vec0[:,11] = [np.sqrt(3.)/4., -0.75, -np.sqrt(2.)/2.]
        self.point_vec0[:,12] = [0., 0., np.sqrt(2.)/2.]
        self.point_vec0[:,13] = [0., 0., -np.sqrt(2.)/2.]
        self.point_vec0[:,14] = [0.3, 0., 0.]
        self.point_vec0[:,15] = [0., 0.3, 0.]
        self.point_vec0[:,16] = [0., 0., 0.3]
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
        self.slip_direc[:, 0] = self.point_vec[:, 1] - self.point_vec[:, 4]
        self.slip_direc[:, 1] = self.point_vec[:, 5] - self.point_vec[:, 2]
        self.slip_direc[:, 2] = self.point_vec[:, 3] - self.point_vec[:, 0]

    def set_c_axis(self):
        self.c_axis = self.point_vec[:, 12] - self.point_vec[:, 13]

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
               self.point_vec[0, 4],
               self.point_vec[0, 5],
               self.point_vec[0, 0]],
            y=[self.point_vec[1, 0],
               self.point_vec[1, 1],
               self.point_vec[1, 2],
               self.point_vec[1, 3],
               self.point_vec[1, 4],
               self.point_vec[1, 5],
               self.point_vec[1, 0]],
            z=[self.point_vec[2, 0],
               self.point_vec[2, 1],
               self.point_vec[2, 2],
               self.point_vec[2, 3],
               self.point_vec[2, 4],
               self.point_vec[2, 5],
               self.point_vec[2, 0]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_bottom = go.Scatter3d(
            x=[self.point_vec[0, 6],
               self.point_vec[0, 7],
               self.point_vec[0, 8],
               self.point_vec[0, 9],
               self.point_vec[0, 10],
               self.point_vec[0, 11],
               self.point_vec[0, 6]],
            y=[self.point_vec[1, 6],
               self.point_vec[1, 7],
               self.point_vec[1, 8],
               self.point_vec[1, 9],
               self.point_vec[1, 10],
               self.point_vec[1, 11],
               self.point_vec[1, 6]],
            z=[self.point_vec[2, 6],
               self.point_vec[2, 7],
               self.point_vec[2, 8],
               self.point_vec[2, 9],
               self.point_vec[2, 10],
               self.point_vec[2, 11],
               self.point_vec[2, 6]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_1 = go.Scatter3d(
            x=[self.point_vec[0, 0], self.point_vec[0, 6]],
            y=[self.point_vec[1, 0], self.point_vec[1, 6]],
            z=[self.point_vec[2, 0], self.point_vec[2, 6]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_2 = go.Scatter3d(
            x=[self.point_vec[0, 1], self.point_vec[0, 7]],
            y=[self.point_vec[1, 1], self.point_vec[1, 7]],
            z=[self.point_vec[2, 1], self.point_vec[2, 7]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_3 = go.Scatter3d(
            x=[self.point_vec[0, 2], self.point_vec[0, 8]],
            y=[self.point_vec[1, 2], self.point_vec[1, 8]],
            z=[self.point_vec[2, 2], self.point_vec[2, 8]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_4 = go.Scatter3d(
            x=[self.point_vec[0, 3], self.point_vec[0, 9]],
            y=[self.point_vec[1, 3], self.point_vec[1, 9]],
            z=[self.point_vec[2, 3], self.point_vec[2, 9]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_5 = go.Scatter3d(
            x=[self.point_vec[0, 4], self.point_vec[0, 10]],
            y=[self.point_vec[1, 4], self.point_vec[1, 10]],
            z=[self.point_vec[2, 4], self.point_vec[2, 10]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_side_6 = go.Scatter3d(
            x=[self.point_vec[0, 5], self.point_vec[0, 11]],
            y=[self.point_vec[1, 5], self.point_vec[1, 11]],
            z=[self.point_vec[2, 5], self.point_vec[2, 11]],
            line = dict(width = 6, color='black'),
            showlegend=False
        )

        go_axis_x = go.Scatter3d(
            x=[0., self.point_vec[0,14]],
            y=[0., self.point_vec[1,14]],
            z=[0., self.point_vec[2,14]],
            line = dict(width = 6, color='red'),
            showlegend=False
        )

        go_axis_y = go.Scatter3d(
            x=[0., self.point_vec[0,15]],
            y=[0., self.point_vec[1,15]],
            z=[0., self.point_vec[2,15]],
            line = dict(width = 6, color='blue'),
            showlegend=False
        )

        go_axis_z = go.Scatter3d(
            x=[0., self.point_vec[0,16]],
            y=[0., self.point_vec[1,16]],
            z=[0., self.point_vec[2,16]],
            line = dict(width = 6, color='green'),
            showlegend=False
        )

        self.data_go = [go_side, go_bottom, go_side_1, go_side_2, go_side_3, go_side_4, go_side_5, go_side_6, go_axis_x, go_axis_y, go_axis_z]

    def set_crystal_basis(self):

        self.base_s = np.zeros((3, 18))
        self.base_m = np.zeros((3, 18))

        # set slip direction vector
        self.base_s[0, 0] =  0.5000000000000000
        self.base_s[1, 0] =  0.8660254037844386
        self.base_s[2, 0] =  0.0000000000000000

        self.base_s[0, 1] =  0.5000000000000000
        self.base_s[1, 1] = -0.8660254037844386
        self.base_s[2, 1] =  0.0000000000000000

        self.base_s[0, 2] = -1.0000000000000000
        self.base_s[1, 2] =  0.0000000000000000
        self.base_s[2, 2] =  0.0000000000000000

        self.base_s[0, 3] =  0.5000000000000000
        self.base_s[1, 3] =  0.8660254037844386
        self.base_s[2, 3] =  0.0000000000000000

        self.base_s[0, 4] =  0.5000000000000000
        self.base_s[1, 4] = -0.8660254037844386
        self.base_s[2, 4] =  0.0000000000000000

        self.base_s[0, 5] = -1.0000000000000000
        self.base_s[1, 5] =  0.0000000000000000
        self.base_s[2, 5] =  0.0000000000000000

        self.base_s[0, 6] = -0.2621657211137508
        self.base_s[1, 6] = -0.4540843489719491
        self.base_s[2, 6] =  0.8515142621774624

        self.base_s[0, 7] = -0.2621657211137508
        self.base_s[1, 7] =  0.4540843489719491
        self.base_s[2, 7] =  0.8515142621774624

        self.base_s[0, 8] =  0.5243314422275015
        self.base_s[1, 8] =  0.0000000000000000
        self.base_s[2, 8] =  0.8515142621774624

        self.base_s[0, 9] =  0.2621657211137508
        self.base_s[1, 9] =  0.4540843489719491
        self.base_s[2, 9] =  0.8515142621774624

        self.base_s[0,10] =  0.2621657211137508
        self.base_s[1,10] = -0.4540843489719491
        self.base_s[2,10] =  0.8515142621774624

        self.base_s[0,11] = -0.5243314422275015
        self.base_s[1,11] =  0.0000000000000000
        self.base_s[2,11] =  0.8515142621774624

        self.base_s[0,12] = -0.1471256306792020
        self.base_s[1,12] = -0.2548290674319922
        self.base_s[2,12] =  0.9557280968920963

        self.base_s[0,13] =  0.1471256306792020
        self.base_s[1,13] = -0.2548290674319922
        self.base_s[2,13] =  0.9557280968920963

        self.base_s[0,14] =  0.2942512613584040
        self.base_s[1,14] =  0.0000000000000000
        self.base_s[2,14] =  0.9557280968920963

        self.base_s[0,15] =  0.1471256306792020
        self.base_s[1,15] =  0.2548290674319922
        self.base_s[2,15] =  0.9557280968920963

        self.base_s[0,16] = -0.1471256306792020
        self.base_s[1,16] =  0.2548290674319922
        self.base_s[2,16] =  0.9557280968920963

        self.base_s[0,17] = -0.2942512613584040
        self.base_s[1,17] =  0.0000000000000000
        self.base_s[2,17] =  0.9557280968920963

        # set normal to slip direction vector
        self.base_m[0, 0] =  0.0000000000000000
        self.base_m[1, 0] =  0.0000000000000000
        self.base_m[2, 0] =  1.0000000000000000

        self.base_m[0, 1] =  0.0000000000000000
        self.base_m[1, 1] =  0.0000000000000000
        self.base_m[2, 1] =  1.0000000000000000

        self.base_m[0, 2] =  0.0000000000000000
        self.base_m[1, 2] =  0.0000000000000000
        self.base_m[2, 2] =  1.0000000000000000

        self.base_m[0, 3] =  0.8660254037844386
        self.base_m[1, 3] = -0.5000000000000000
        self.base_m[2, 3] =  0.0000000000000000

        self.base_m[0, 4] = -0.8660254037844386
        self.base_m[1, 4] = -0.5000000000000000
        self.base_m[2, 4] =  0.0000000000000000

        self.base_m[0, 5] =  0.0000000000000000
        self.base_m[1, 5] = -1.0000000000000000
        self.base_m[2, 5] =  0.0000000000000000

        self.base_m[0, 6] =  0.4257571310887312
        self.base_m[1, 6] =  0.7374329827304453
        self.base_m[2, 6] =  0.5243314422275015

        self.base_m[0, 7] =  0.4257571310887312
        self.base_m[1, 7] = -0.7374329827304453
        self.base_m[2, 7] =  0.5243314422275015

        self.base_m[0, 8] = -0.8515142621774624
        self.base_m[1, 8] =  0.0000000000000000
        self.base_m[2, 8] =  0.5243314422275015

        self.base_m[0, 9] = -0.4257571310887312
        self.base_m[1, 9] = -0.7374329827304453
        self.base_m[2, 9] =  0.5243314422275015

        self.base_m[0,10] = -0.4257571310887312
        self.base_m[1,10] =  0.7374329827304453
        self.base_m[2,10] =  0.5243314422275015

        self.base_m[0,11] =  0.8515142621774624
        self.base_m[1,11] =  0.0000000000000000
        self.base_m[2,11] =  0.5243314422275015

        self.base_m[0,12] =  0.4778640484460481
        self.base_m[1,12] =  0.8276848110191108
        self.base_m[2,12] =  0.2942512613584040

        self.base_m[0,13] = -0.4778640484460481
        self.base_m[1,13] =  0.8276848110191108
        self.base_m[2,13] =  0.2942512613584040

        self.base_m[0,14] = -0.9557280968920963
        self.base_m[1,14] =  0.0000000000000000
        self.base_m[2,14] =  0.2942512613584040

        self.base_m[0,15] = -0.4778640484460481
        self.base_m[1,15] = -0.8276848110191108
        self.base_m[2,15] =  0.2942512613584040

        self.base_m[0,16] =  0.4778640484460481
        self.base_m[1,16] = -0.8276848110191108
        self.base_m[2,16] =  0.2942512613584040

        self.base_m[0,17] =  0.9557280968920963
        self.base_m[1,17] =  0.0000000000000000
        self.base_m[2,17] =  0.2942512613584040
