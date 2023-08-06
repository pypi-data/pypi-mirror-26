pyodesys
========

.. image:: http://hera.physchem.kth.se:9090/api/badges/bjodah/pyodesys/status.svg
   :target: http://hera.physchem.kth.se:9090/bjodah/pyodesys
   :alt: Build status
.. image:: https://img.shields.io/pypi/v/pyodesys.svg
   :target: https://pypi.python.org/pypi/pyodesys
   :alt: PyPI version
.. image:: https://img.shields.io/badge/python-2.7,3.4,3.5-blue.svg
   :target: https://www.python.org/
   :alt: Python version
.. image:: https://img.shields.io/pypi/l/pyodesys.svg
   :target: https://github.com/bjodah/pyodesys/blob/master/LICENSE
   :alt: License
.. image:: http://img.shields.io/badge/benchmarked%20by-asv-green.svg?style=flat
   :target: http://hera.physchem.kth.se/~pyodesys/benchmarks
   :alt: airspeedvelocity
.. image:: http://hera.physchem.kth.se/~pyodesys/branches/master/htmlcov/coverage.svg
   :target: http://hera.physchem.kth.se/~pyodesys/branches/master/htmlcov
   :alt: coverage
.. image:: https://zenodo.org/badge/43131469.svg
   :target: https://zenodo.org/badge/latestdoi/43131469
   :alt: Zenodo DOI

`pyodesys <https://github.com/bjodah/pyodesys>`_ provides a straightforward way
of numerically integrating systems of ordinary differential equations (initial value problems).
It unifies the interface of several libraries for performing the numerical integration as well as
several libraries for symbolic representation. It also provides a convenience class for 
representing and integrating ODE systems defined by symbolic expressions, e.g. `SymPy <http://www.sympy.org>`_
expressions. This allows the user to write concise code and rely on ``pyodesys`` to handle the subtle differences
between libraries.

The numerical integration is performed using either:

    - `scipy.integrate.ode <http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.ode.html>`_
    - `pygslodeiv2 <https://github.com/bjodah/pygslodeiv2>`_
    - `pyodeint <https://github.com/bjodah/pyodeint>`_
    - `pycvodes <https://github.com/bjodah/pycvodes>`_

Note that implicit steppers require a user supplied callback for calculating the Jacobian.
``pyodesys.SymbolicSys`` derives the Jacobian automatically.

The symbolic representation is usually in the form of `SymPy <https://www.sympy.org/>`_
expressions, but the user may choose another symbolic back-end (see `sym <https://github.com/bjodah/sym>`_).

When performance is of utmost importance, e.g. in model fitting where results are needed
for a large set of initial conditions and parameters, the user may transparently
rely on compiled native code (classes in ``pyodesys.native.native_sys`` can generate optimal C++ code).
The major benefit is that there is no need to manually rewrite the corresponding expressions in another
programming language.

Documentation
-------------
Auto-generated API documentation for latest stable release is found here:
`<https://bjodah.github.io/pyodesys/latest>`_
(and the development version for the current master branch is found here:
`<http://hera.physchem.kth.se/~pyodesys/branches/master/html>`_).


Installation
------------
Simplest way to install pyodesys and its (optional) dependencies is to use the
`conda package manager <http://conda.pydata.org/docs/>`_:

::

   $ conda install -c bjodah pyodesys pytest
   $ python -m pytest --pyargs pyodesys

alternatively you may also use `pip`:

::

   $ python -m pip install --user pyodesys[all]

see `setup.py <setup.py>`_ for optional requirements.

Examples
--------
The classic van der Pol oscillator (see `examples/van_der_pol.py <examples/van_der_pol.py>`_)

.. code:: python

   >>> from pyodesys.symbolic import SymbolicSys
   >>> def f(t, y, p):
   ...     return [y[1], -y[0] + p[0]*y[1]*(1 - y[0]**2)]
   ... 
   >>> odesys = SymbolicSys.from_callback(f, 2, 1)
   >>> xout, yout, info = odesys.integrate(10, [1, 0], [1], integrator='odeint', nsteps=1000)
   >>> _ = odesys.plot_result()
   >>> import matplotlib.pyplot as plt; plt.show()  # doctest: +SKIP

.. image:: https://raw.githubusercontent.com/bjodah/pyodesys/master/examples/van_der_pol.png

If the expression contains transcendental functions you will need to provide a ``backend`` keyword argument:

.. code:: python

   >>> import math
   >>> def f(x, y, p, backend=math):
   ...     return [backend.exp(-p[0]*y[0])]  # analytic: y(x) := ln(kx + kc)/k
   ... 
   >>> odesys = SymbolicSys.from_callback(f, 1, 1)
   >>> y0, k = -1, 3
   >>> xout, yout, info = odesys.integrate(5, [y0], [k], integrator='cvode', method='bdf')
   >>> _ = odesys.plot_result()
   >>> import matplotlib.pyplot as plt
   >>> import numpy as np
   >>> c = 1./k*math.exp(k*y0)  # integration constant
   >>> _ = plt.plot(xout, np.log(k*(xout+c))/k, '--', linewidth=2, alpha=.5, label='analytic')
   >>> _ = plt.legend(loc='best'); plt.show()  # doctest: +SKIP

.. image:: https://raw.githubusercontent.com/bjodah/pyodesys/master/examples/lnx.png

If you already have symbolic expressions created using e.g. SymPy you can create your system from those:

.. code:: python

   >>> import sympy as sp
   >>> t, u, v, k  = sp.symbols('t u v k')
   >>> dudt = v
   >>> dvdt = -k*u  # differential equations for a harmonic oscillator
   >>> odesys = SymbolicSys([(u, dudt), (v, dvdt)], t, [k])
   >>> result = odesys.integrate(7, {u: 2, v: 0}, {k: 3}, integrator='gsl', method='rk8pd', atol=1e-11, rtol=1e-12)
   >>> _ = plt.subplot(1, 2, 1)
   >>> _ = result.plot()
   >>> _ = plt.subplot(1, 2, 2)
   >>> _ = plt.plot(result.xout, 2*np.cos(result.xout*3**0.5) - result.yout[:, 0])
   >>> plt.show()  # doctest: +SKIP

.. image:: https://raw.githubusercontent.com/bjodah/pyodesys/master/examples/harmonic.png

You can also refer to the dependent variables by name instead of index:

.. code:: python

   >>> odesys = SymbolicSys.from_callback(
   ...     lambda t, y, p: {
   ...         'x': -p['a']*y['x'],
   ...         'y': -p['b']*y['y'] + p['a']*y['x'],
   ...         'z': p['b']*y['y']
   ...     }, names='xyz', param_names='ab', dep_by_name=True, par_by_name=True)
   ... 
   >>> t, ic, pars = [42, 43, 44], {'x': 7, 'y': 5, 'z': 3}, {'a': [11, 17, 19], 'b': 13}
   >>> for r, a in zip(odesys.integrate(t, ic, pars, integrator='cvode'), pars['a']):
   ...     assert np.allclose(r.named_dep('x'), 7*np.exp(-a*(r.xout - r.xout[0])))
   ...     print('%.2f ms ' % (r.info['time_cpu']*1e3))  # doctest: +SKIP
   ... 
   10.54 ms
   11.55 ms
   11.06 ms

Note how we generated a list of results for each value of the parameter ``a``. When using a class
from ``pyodesys.native.native_sys`` those integrations are run in separate threads (bag of tasks
parallelism):

.. code:: python

   >>> from pyodesys.native import native_sys
   >>> native = native_sys['cvode'].from_other(odesys)
   >>> for r, a in zip(native.integrate(t, ic, pars), pars['a']):
   ...     assert np.allclose(r.named_dep('x'), 7*np.exp(-a*(r.xout - r.xout[0])))
   ...     print('%.2f ms ' % (r.info['time_cpu']*1e3))  # doctest: +SKIP
   ... 
   0.42 ms
   0.43 ms
   0.42 ms

For this small example we see a 20x (serial) speedup by using native code. Bigger systems often see 100x speedup.
Since the latter is run in parallel the (wall clock) time spent waiting for the results is in practice
further reduced by a factor equal to the number of cores of your CPU (number of threads used is set by
the environment variable ``ANYODE_NUM_THREADS``).

For further examples, see `examples/ <https://github.com/bjodah/pyodesys/tree/master/examples>`_, and rendered
jupyter notebooks here: `<http://hera.physchem.kth.se/~pyodesys/branches/master/examples>`_

License
-------
The source code is Open Source and is released under the simplified 2-clause BSD license. See `LICENSE <LICENSE>`_ for further details.
Contributors are welcome to suggest improvements at https://github.com/bjodah/pyodesys

Author
------
Björn I. Dahlgren, contact:

    - gmail address: bjodah
    - kth.se address: bda
