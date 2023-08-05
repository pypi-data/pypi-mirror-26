pyGrad2Surf
===========

Software that effectively integrates two vector fields to obtain a scalar field. Example usage can be seen at [cthulhu](https://github.com/cjordan/cthulhu). This repo merely reflects a python translation of the MATLAB code supplied by Harker & O'Leary: [paper](https://arxiv.org/abs/1308.4292) and [code](http://www.mathworks.com/matlabcentral/fileexchange/43149-surface-reconstruction-from-gradient-fields--grad2surf-version-1-0).

Usage
-----
An excerpt from [cthulhu](https://github.com/cjordan/cthulhu):

        grid_x, grid_y = np.meshgrid(np.linspace(-self.radius, self.radius, resolution),
                                     np.linspace(-self.radius, self.radius, resolution))
        self.grid_dra = np.flipud(np.fliplr(griddata(np.vstack((ra, dec)).T, ra_shifts,
                                            (grid_x, grid_y), method=interp_method, fill_value=0)))
        self.grid_ddec = np.flipud(np.fliplr(griddata(np.vstack((ra, dec)).T, dec_shifts,
                                             (grid_x, grid_y), method=interp_method, fill_value=0)))
        self.tec = np.flipud(g2s_method(grid_x[0, :], grid_y[:, 0], self.grid_dra, self.grid_ddec))

where ```grid_dra``` and ```grid_ddec``` are generated from griddata from scipy.interpolate. Put simply, the gradient values (```ra_shifts``` and ```dec_shifts```) at the spatial positions (```ra``` and ```dec```) are gridded to form vector fields, which are then integrated by pyGrad2Surf.

Limitations
-----------
A number of g2s methods are detailed by Harker & O'Leary, however, only the basic g2s method is available here. The other methods require some work to translate, thanks to syntactic and functional differences between python and MATLAB. These may or may not be completed in the future, but pull requests are welcome.

Contact
-------
christopherjordan87 -at- gmail.com

Dependencies
------------
- python 2.7.x
- numpy
- scipy


