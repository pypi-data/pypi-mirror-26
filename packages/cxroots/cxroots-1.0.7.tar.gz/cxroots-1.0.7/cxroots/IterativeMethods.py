from __future__ import division

def iterateToRoot(x0, f, df=None, steptol=1e-12, roottol=1e-12, maxIter=20):
	# iterate to a root using initial point x0
	if df is not None:
		try:
			# uses Newton-Raphson method if f and df are given.

			# SciPy implementation
			# import scipy.optimize
			# root = scipy.optimize.newton(f, x0, df, tol=steptol, maxiter=maxIter)
			# err = abs(f(root))
			
			root, err = newton(x0, f, df, steptol, 0, maxIter)

		except (RuntimeError, OverflowError):
			return None
	else:
		### For profiling number of function calls:
		# fcalls = [0,0]
		# def secant_f(z):
		# 	fcalls[0] += 1
		# 	return f(z)
		# def muller_f(z):
		# 	fcalls[1] += 1
		# 	return f(z)

		# # Secant method: 
		# x1, x2 = x0, x0 + (x0+1)*1e-8
		# root, err = secant(x1, x2, secant_f, steptol, 0, maxIter)
		# print('-----')
		# print('Secant:', fcalls[0], root, err)

		# # Muller's method:
		# x1, x2, x3 = x0, x0*(1 + 1e-8) + 1e-8, x0*(1 - 1e-8) - 1e-8
		# root, err = muller(x1, x2, x3, muller_f, steptol, 0, maxIter)
		# print('Muller:', fcalls[1], root, err)
		# print('-----')
		############################################

		# Muller's method:
		x1, x2, x3 = x0, x0*(1 + 1e-8) + 1e-8, x0*(1 - 1e-8) - 1e-8
		root, err = muller(x1, x2, x3, f, steptol, 0, maxIter)

	if err < roottol:
		return root

def muller(x1, x2, x3, f, steptol=1e-12, roottol=1e-12, maxIter=20, verbose=False, callback=None):
	"""
	Wrapper for mpmath's implementation of Muller's method.  

	Parameters
	----------
	x1 : float or complex
		An initial point for iteration, should be close to a 
		root of f.
	x2 : float or complex
		An initial point for iteration, should be close to a 
		root of f.  Should not equal x1.
	x3 : float or complex
		An initial point for iteration, should be close to a 
		root of f.  Should not equal x1 or x2.
	f : function
		Function of a single variable f(x)
	steptol: float, optional
		Routine will end if the step size, dx, between sucessive
		iterations of x satisfies abs(dx) < steptol
	roottol: float, optional
		The routine will end if abs(f(x)) < roottol
	maxIter : int, optional
		Routine ends after maxIter iterations
	callback : function, optional
		After each iteration the supplied function 
		callback(x, dx, f(x), iteration) will be called where 'x' is the current iteration 
		of the estimated root, 'dx' is the step size between the previous 
		and current 'x' and 'iteration' the number of iterations that have been taken.  
		If the callback function evaluates to True then the routine will end

	Returns
	-------
	xf : float
		The approximation to a root of f
	rooterr : float
		The error of the original function at xf, abs(f(xf))

	"""
	from mpmath import mp, mpmathify
	from mpmath.calculus.optimization import Muller


	# mpmath insists on functions accepting mpc
	f_mpmath = lambda z: mpmathify(f(complex(z))) 

	mull = Muller(mp, f_mpmath, (x1, x2, x3), verbose=verbose)
	iteration = 0
	x0 = x3

	try:
		for x, err in mull:
			dx = x - x0

			if callback is not None and callback(x, dx, err, iteration+1):
				break

			if abs(dx) < steptol or err < roottol or iteration > maxIter:
				break

			iteration += 1
			x0 = x

	except ZeroDivisionError:
		# ZeroDivisionError comes up if the error is evaluated to be zero
		pass

	# cast mpc and mpf back to regular complex and float
	return complex(x), float(err)


def newton(x0, f, df, steptol=1e-12, roottol=1e-12, maxIter=20, callback=None):
	"""
	Find an approximation to a point xf such that f(xf)=0 for a 
	scalar function f using Newton-Raphson iteration starting at 
	the point x0.

	Parameters
	----------
	x0 : float or complex
		Initial point for Newton iteration, should be as close as
		possible to a root of f
	f : function
		Function of a single variable f(x)
	df : function
		Function of a single variable, df(x), providing the
		derivative of the function f(x) at the point x
	steptol: float, optional
		Routine will end if the step size, dx, between sucessive
		iterations of x satisfies abs(dx) < steptol
	roottol: float, optional
		The routine will end if abs(f(x)) < roottol
	maxIter : int, optional
		Routine ends after maxIter iterations
	callback : function, optional
		After each iteration the supplied function 
		callback(x, dx, f(x), iteration) will be called where 'x' is the current iteration 
		of the estimated root, 'dx' is the step size between the previous 
		and current 'x' and 'iteration' the number of iterations that have been taken.  
		If the callback function evaluates to True then the routine will end

	Returns
	-------
	xf : float
		The approximation to a root of f
	rooterr : float
		The error of the original function at xf, abs(f(xf))
	"""

	# XXX: Could use deflated polynomials to ensure that known roots are not found again?
	
	# print('--newton--')

	x, y = x0, f(x0)
	for iteration in range(maxIter):
		dx = -y/df(x)
		x += dx
		y  = f(x)

		if callback is not None and callback(x, dx, y, iteration+1):
			break

		# print(iteration, y, abs(y))

		if abs(dx) < steptol or abs(y) < roottol:
			break

	return x, abs(y)

def secant(x1, x2, f, steptol=1e-12, roottol=1e-12, maxIter=30, callback=None):
	"""
	Find an approximation to a point xf such that f(xf)=0 for a 
	scalar function f using the secant method.  The method requires
	two initial points x1 and x2, ideally close to a root
	and proceeds iteratively.

	Parameters
	----------
	x1 : float or complex
		An initial point for iteration, should be close to a 
		root of f.
	x2 : float or complex
		An initial point for iteration, should be close to a 
		root of f.  Should not equal x1.
	f : function
		Function of a single variable f(x)
	steptol: float, optional
		Routine will end if the step size, dx, between sucessive
		iterations of x satisfies abs(dx) < steptol
	roottol: float, optional
		The routine will end if abs(f(x)) < roottol
	maxIter : int, optional
		Routine ends after maxIter iterations
	callback : function, optional
		After each iteration the supplied function 
		callback(x, dx, f(x), iteration) will be called where 'x' is the current iteration 
		of the estimated root, 'dx' is the step size between the previous 
		and current 'x' and 'iteration' the number of iterations that have been taken.  
		If the callback function evaluates to True then the routine will end

	Returns
	-------
	xf : float
		The approximation to a root of f
	rooterr : float
		The error of the original function at xf, abs(f(xf))
	"""

	# As in "Numerical Recipies 3rd Edition" pick the bound with the 
	# smallest function value as the most recent guess
	y1, y2 = f(x1), f(x2)
	if abs(y1) < abs(y2):
		x1, x2 = x2, x1
		y1, y2 = y2, y1

	# print('--secant--')

	for iteration in range(maxIter):
		dx =  -(x2-x1)*y2/(y2-y1)
		x1, x2 = x2, x2 + dx
		y1, y2 = y2, f(x2)

		if callback is not None and callback(x2, dx, y2, iteration+1):
			break

		# print(iteration, x2, abs(dx), abs(y2))

		if abs(dx) < steptol or abs(y2) < roottol:
			break

	return x2, abs(y2)
