JiTCODE stands for just-in-time compilation for ordinary differential equations and is an extension of `SciPy’s ODE <http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.ode.html>`_ (``scipy.integrate.ode``).
Where SciPy’s ODE takes a Python function as an argument, JiTCODE takes an iterable (or generator function) of `SymPy <http://www.sympy.org/>`_ expressions, which it translates to C code, compiles on the fly, and uses as the function to feed into SciPy’s ODE.
If you want to integrate delay or stochastic differential equations, check out
`JiTCDDE <http://github.com/neurophysik/jitcdde>`_, or
`JiTCSDE <http://github.com/neurophysik/jitcsde>`_, respectively.


* `Documentation <http://jitcode.readthedocs.io>`_

* `Issue Tracker <http://github.com/neurophysik/jitcode/issues>`_

* `Installation instructions <http://jitcde-common.readthedocs.io/#installation>`_ (or just ``pip install jitcode``).

This work was supported by the Volkswagen Foundation (Grant No. 88463).

