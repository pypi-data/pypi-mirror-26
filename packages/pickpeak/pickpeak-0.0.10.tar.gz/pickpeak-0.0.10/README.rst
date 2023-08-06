Pick Peak
=======================

Pick Peak is a `PyQtGraph <http://www.pyqtgraph.org/>`_-based tool. It aims
to provide a graphical user interface to allow the user easily selecting peaks of a
spectrum ploat.


----

README
""""""""""""""""" 

**Introduction**
 
To do.

**Installation**

For standard Python installations, install pickpeak using pip:

.. code:: bash

    pip install -U pip setuptools
    pip install pickpeak

**Usage**

.. code:: python
	
	from pickpeak.pickpeak import pickpeak as pp
	import numpy as np
	spectrum = np.random.rand(20) #sample of spectrum
	peaks = pp(spectrum) #spectrum shoud be type numpy.ndarray 1D
	print peaks # list of peaks
	

**Requirements**

* `Python 2.7 <https://www.python.org/downloads/>`_.
* `Setuptools <https://setuptools.readthedocs.io/en/latest/>`_.
* `PyQtGraph <http://www.pyqtgraph.org/>`_.
* `PyQt5 <https://pypi.python.org/pypi/PyQt5/5.9>`_.
* `NumPy <http://www.numpy.org/>`_.

**Status**

* We choose to move to PyQtGraph to have more GUI resources without losing simplicity.
