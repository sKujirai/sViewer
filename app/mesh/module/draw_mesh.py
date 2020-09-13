import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as mtri


class DrawMesh:

    def set_domain(self, ax, *, domain):

        # Set display area
        self.xmin = domain['xmin']
        self.xmax = domain['xmax']
        self.ymin = domain['ymin']
        self.ymax = domain['ymax']
        self.aspect = domain['aspect']

        self.isSetRange = False

        self.set_mpl_params(ax)

    def set_mpl_params(self, ax):

        self.ax = ax

        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_aspect(self.aspect)

        self.ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)

        self.ax.tick_params(bottom=False, left=False, right=False, top=False)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def polyplot(self, coords, connectivity, value=None, **kwargs):

        vertices = coords[:2, :].T[np.asarray(connectivity)]
        pcm = mpl.collections.PolyCollection(vertices, **kwargs)
        if value is not None:
            pcm.set_array(value)
        if self.isSetRange:
            pcm.set_clim(vmin=self.vmin, vmax=self.vmax)
        self.ax.add_collection(pcm)

    def draw(self, *, coords, connectivity, value=None):

        edge_color = None
        marker_size = 1
        cmap = 'jet'
        show_colorbar = True

        self.ax.set_aspect('equal')

        nnodes = connectivity.shape[1]
        if nnodes == 6 or nnodes == 10:
            connectivity = connectivity[:, :3]
        elif nnodes == 4 or nnodes == 8 or nnodes == 12 or nnodes == 16:
            connectivity = connectivity[:, :4]

        if value is None:
            if edge_color is None:
                edge_color = 'k'
            self.polyplot(coords=coords, connectivity=connectivity, edgecolors=edge_color, facecolor="None", cmap=cmap)
        else:
            if connectivity is None or connectivity.shape[1] == 1:
                if self.isSetRange:
                    self.ax.scatter(coords[0, :], coords[1, :], c=value, cmap=cmap, vmin=self.vmin, vmax=self.vmax, s=marker_size)
                else:
                    self.ax.scatter(coords[0, :], coords[1, :], c=value, cmap=cmap, s=marker_size)
            else:
                self.polyplot(coords=coords, connectivity=connectivity, value=value, edgecolors=edge_color, cmap=cmap)
                if show_colorbar:
                    pcm = self.ax.get_children()[0]
                    plt.colorbar(pcm, ax=self.ax, orientation='vertical')
