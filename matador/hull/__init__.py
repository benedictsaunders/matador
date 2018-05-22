# coding: utf-8
# Distributed under the terms of the MIT License.

""" The hull module provides functionality for creating phase diagrams,
voltage curves and volume curves, either directly from a database, or
from files.

"""


__all__ = ['QueryConvexHull', 'HullDiff', 'diff_hulls']
__author__ = 'Matthew Evans'
__maintainer__ = 'Matthew Evans'


from matador.hull.hull import QueryConvexHull
from matador.hull.hull_diff import HullDiff, diff_hulls