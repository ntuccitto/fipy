#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "matplotlibVectorViewer.py"
 #                                    created: 9/14/04 {2:48:25 PM} 
 #                                last update: 2/26/07 {12:29:15 PM} { 2:45:36 PM}
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##
 
__docformat__ = 'restructuredtext'

from fipy.tools import numerix
from matplotlibViewer import MatplotlibViewer
from fipy.variables.faceVariable import FaceVariable
from fipy.variables.cellVariable import CellVariable

class MatplotlibVectorViewer(MatplotlibViewer):
    """
    Displays a vector plot of a 2D rank-1 `CellVariable` or
    `FaceVariable` object using Matplotlib_

    .. _Matplotlib: http://matplotlib.sourceforge.net/

    """

    def __init__(self, vars, limits = None, title = None):
        """
        Creates a `Matplotlib2DViewer`.
        
        :Parameters:
          - `vars`: A `CellVariable` object.
          - `limits`: A dictionary with possible keys `'xmin'`, `'xmax'`, 
            `'ymin'`, `'ymax'`, `'datamin'`, `'datamax'`. Any limit set to 
            a (default) value of `None` will autoscale.
          - `title`: displayed at the top of the Viewer window

        """
        MatplotlibViewer.__init__(self, vars = vars, limits = limits, title = title)

        self.colorbar = False
        
    def _getSuitableVars(self, vars):
        from fipy.meshes.numMesh.grid2D import Grid2D

        vars = [var for var in MatplotlibViewer._getSuitableVars(self, vars) \
                if (isinstance(var.getMesh(), Grid2D) \
                    and (isinstance(var, FaceVariable) \
                         or isinstance(var, CellVariable)) and var.getRank() == 1)]
        if len(vars) == 0:
            from fipy.viewers import MeshDimensionError
            raise MeshDimensionError, "The mesh must be a Grid2D instance"
        # this viewer can only display one variable
        return [vars[0]]
                
    def _plot(self):

        var = self.vars[0]
        mesh = var.getMesh()

        
        if isinstance(var, FaceVariable):
            ## only displays horizontel faces since quiver() takes a grid
            shape = (mesh.getShape()[1] + 1, mesh.getShape()[0])
            N = shape[0] * shape[1]
            X = numerix.reshape(mesh.getFaceCenters()[:N,0], shape)
            Y = numerix.reshape(mesh.getFaceCenters()[:N,1], shape)
            U = numerix.reshape(var[:N,0], shape)
            V = numerix.reshape(var[:N,1], shape)
        elif isinstance(var, CellVariable):
            shape = (mesh.getShape()[1], mesh.getShape()[0])
            X = numerix.reshape(mesh.getCellCenters()[:,0], shape)
            Y = numerix.reshape(mesh.getCellCenters()[:,1], shape)
            U = numerix.reshape(var[:,0], shape)
            V = numerix.reshape(var[:,1], shape)
        
        import pylab
        pylab.quiver2(X, Y, U, V, 0.15)
                            
        pylab.ylim(ymin = self._getLimit('ymin'))
        pylab.ylim(ymax = self._getLimit('ymax'))


        
