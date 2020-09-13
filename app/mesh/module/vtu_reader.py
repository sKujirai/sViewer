import xml.etree.ElementTree as ET
import os
import sys
import glob
import shutil
import numpy as np


class VtkReader:
    """
    VTK file reader
    """

    def __init__(self):

        # 各種タグ
        self.root_tag = r'{VTK}UnstructuredGrid'
        self.piece_tag = r'{VTK}Piece'
        self.attrib_tag = r'Name'
        self.ncomp_tag = r'NumberOfComponents'
        self.nelm_tag = r'NumberOfCells'
        self.npts_tag = r'NumberOfPoints'
        self.pts_data_tag = r'{VTK}PointData'
        self.cell_data_tag = r'{VTK}CellData'
        self.points_tag = r'{VTK}Points'
        self.cells_tag = r'{VTK}Cells'
        self.darray_tag = r'{VTK}DataArray'

        self.MESHFREE = r'Meshfree'
        self.FEM = r'FiniteElement'

        self.tag_orientation = r'Crystal Orientation'

    def read(self, file_path):

        # Parse XML
        tree = ET.parse(file_path)
        root = tree.getroot()
        try:
            self.discretization_method = root.attrib['name']
        except Exception:
            try:
                self.discretization_method = root.attrib[self.attrib_tag]
            except Exception:
                self.discretization_method = self.FEM
        unstructured_grid = root.find(self.root_tag)
        piece = unstructured_grid.find(self.piece_tag)

        # \# of nodes, elements and coordinates
        self.nelements = int(piece.attrib[self.nelm_tag])
        self.npoints = int(piece.attrib[self.npts_tag])
        self.Coords = self.read_coordinates(piece)
        if self.discretization_method == self.MESHFREE:
            self.Lnodes = None
        else:
            self.Lnodes = self.read_connectivity(piece)

        try:
            point_data = piece.find(self.pts_data_tag)
            self.pts_data_array = point_data.findall(self.darray_tag)
        except Exception:
            self.pts_data_array = None

        try:
            cell_data = piece.find(self.cell_data_tag)
            self.cell_data_array = cell_data.findall(self.darray_tag)
        except Exception:
            self.cell_data_array = None

    def read_coordinates(self, piece):

        points = piece.find(self.points_tag)
        cods = points.find(self.darray_tag)

        coords_list = cods.text.split('\n')
        coords = np.zeros((3, self.npoints), dtype=float)
        ipnt = 0
        for cod_lst in coords_list:
            if cod_lst == '':
                continue
            cod = cod_lst.split(' ')
            for idof in range(3):
                coords[idof, ipnt] = float(cod[idof])
            ipnt += 1

        return coords

    def read_connectivity(self, piece):
        cells = piece.find(self.cells_tag)
        darray = cells.findall(self.darray_tag)
        lnodes = []
        for d in darray:
            if d.attrib[self.attrib_tag] == 'connectivity':
                lnodes_list = d.text.split('\n')
                for lnd_lst in lnodes_list:
                    if lnd_lst == '':
                        continue
                    lnd = lnd_lst.split(' ')
                    nod_lst = []
                    for nod in lnd:
                        if nod != '':
                            nod_lst.append(int(nod))
                    lnodes.append(nod_lst)

        lnodes = np.array(lnodes)

        return lnodes

    def is_nodal_mesh(self):

        return self.discretization_method == self.MESHFREE

    def get_data_dict(self):

        if self.discretization_method == self.MESHFREE:
            data_array = self.pts_data_array
        else:
            data_array = self.cell_data_array

        data_dict = {'Mesh': 1}
        for dat in data_array:
            name = dat.attrib[self.attrib_tag]
            nsys = dat.attrib[self.ncomp_tag]
            if name not in data_dict.keys():
                data_dict[name] = int(nsys)

        return data_dict

    def get_value(self, tag, *, system, nodal=False):

        if nodal:
            data_array = self.pts_data_array
            nvalue = self.npoints
        else:
            data_array = self.cell_data_array
            nvalue = self.nelements

        isFound = False
        val = np.zeros(nvalue, dtype=float)
        for dat in data_array:
            if tag == dat.attrib[self.attrib_tag]:
                val_list = dat.text.split('\n')
                ival = 0
                for vlst in val_list:
                    if vlst == '':
                        continue
                    vl = vlst.split()
                    if system == -1:
                        val = val.astype('int64')
                        for v in vl:
                            if v == '':
                                continue
                            val[ival] = int(v)
                            isFound = True
                            ival += 1
                    else:
                        isys = 0
                        for v in vl:
                            if v == '':
                                continue
                            if isys == system - 1:
                                val[ival] = float(v)
                                isFound = True
                            isys += 1
                        ival += 1
        if not isFound:
            print('[ERROR] Cannot find value: {} (System: {})'.format(tag, system))
            sys.exit(1)

        return val

    def get_basis(self, tag, *, nodal=True):

        basis = None
        nsystem = None

        if nodal:
            data_array = self.pts_data_array
            nvalue = self.npoints
        else:
            data_array = self.cell_data_array
            nvalue = self.nelements

        isFound = False
        for dat in data_array:
            if tag == dat.attrib[self.attrib_tag]:
                val_list = dat.text.split('\n')
                basis = []
                for vlst in val_list:
                    if vlst == '':
                        continue
                    vl = vlst.split()
                    if len(basis) == 0:
                        nsystem = int(len(vl) / 3)
                    val = np.zeros((nsystem, 3), dtype='float')
                    icnt = 0
                    for v in vl:
                        if v == '':
                            continue
                        val[icnt // 3, icnt % 3] = float(v)
                        isFound = True
                        icnt += 1
                    basis.append(val)
        if not isFound:
            print('[ERROR] Cannot find value: {}'.format(tag))
            sys.exit(1)

        if (basis is None) or (len(basis) != nvalue) or nsystem is None:
            print('[ERROR] Cannot set crystal basis: {}'.format(tag))
            sys.exit(1)

        return basis, nsystem

    def get_IDs(self, tag, *, nodal=False):

        if nodal:
            data_array = self.pts_data_array
            nvalue = self.npoints
        else:
            data_array = self.cell_data_array
            nvalue = self.nelements

        isFound = False
        for dat in data_array:
            if tag == dat.attrib[self.attrib_tag]:
                val_list = dat.text.split('\n')
                ids = []
                for vlst in val_list:
                    if vlst == '':
                        continue
                    vl = vlst.split()
                    for v in vl:
                        if v == '':
                            continue
                        ids.append(v)
                        isFound = True
                        break
        if not isFound:
            print('[ERROR] Cannot find value: {}'.format(tag))
            sys.exit(1)

        if len(ids) != nvalue:
            print('[ERROR] Cannot set ids: {}'.format(tag))
            sys.exit(1)

        return ids

    def get_crystal_orientation(self, *, nodal=False):

        if nodal:
            data_array = self.pts_data_array
            nvalue = self.npoints
        else:
            data_array = self.cell_data_array
            nvalue = self.nelements

        isFound = False
        for dat in data_array:
            if self.tag_orientation == dat.attrib[self.attrib_tag]:
                isFound = True
                val_list = dat.text.split('\n')
                orientations = []
                for vlst in val_list:
                    if vlst == '':
                        continue
                    vl = vlst.split()
                    orie = []
                    for v in vl:
                        if v == '':
                            continue
                        orie.append(v)
                    orientations.append(orie)
        if not isFound:
            print('[ERROR] Cannot find value: {}'.format(self.tag_orientation))
            sys.exit(1)

        orientations = np.array(orientations, dtype='float')

        if orientations.shape[0] != nvalue and orientations.shape[1] != 3:
            print('[ERROR] Cannot set crystal orientation properly: size {}x{}'.format(orientations.shape[0], orientations.shape[1]))
            sys.exit(1)

        return orientations
