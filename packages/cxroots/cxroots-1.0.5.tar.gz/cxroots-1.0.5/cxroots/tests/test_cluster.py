"""
References
----------
[DSZ] "Locating all the Zeros of an Analytic Function in one Complex Variable"
	M.Dellnitz, O.Schutze, Q.Zheng, J. Compu. and App. Math. (2002), Vol.138, Issue 2
[DL] "A Numerical Method for Locating the Zeros of an Analytic function", 
	L.M.Delves, J.N.Lyness, Mathematics of Computation (1967), Vol.21, Issue 100
[KB] "Computing the zeros of analytic functions" by Peter Kravanja, Marc Van Barel, Springer 2000
"""

import unittest
import numpy as np
from scipy import pi, sqrt, exp, sin, cos

from cxroots import Circle, Rectangle
from cxroots.tests.ApproxEqual import roots_approx_equal

class TestCluster(unittest.TestCase):
	def setUp(self):
		self.roots = roots = [3, 3.00001, 3.00002, 8, 8.00002, 8+0.00001j]
		self.multiplicities = [1,1,1,1,1,1]

		# self.C = Circle(0, 8.5)
		self.C = Rectangle([2,9], [-1,1])
		self.f = lambda z: np.prod([z-r for r in roots])
		self.df = lambda z: np.sum([np.prod([z-r for r in np.delete(roots,i)]) for i in range(len(roots))])

	def test_rootfinding_df(self):
		roots_approx_equal(self.C.roots(self.f, self.df), (self.roots, self.multiplicities), decimal=12)

	# def test_rootfinding_f(self):
	# 	roots_approx_equal(self.C.roots(self.f), (self.roots, self.multiplicities), decimal=12)

if __name__ == '__main__':
	# unittest.main(verbosity=3)

	roots = [3, 3.00001, 3.00002, 8, 8.00002, 8+0.00001j]
	multiplicities = [1,1,1,1,1,1]

	f = lambda z: np.prod([z-r for r in roots])
	df = lambda z: np.sum([np.prod([z-r for r in np.delete(roots,i)]) for i in range(len(roots))])

	# C = Circle(0, 8.5)
	C = Rectangle([2,9], [-1,1])
	C.approximate_roots(f, df, verbose=True)

	# # C.demo_roots(f, df)
