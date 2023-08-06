########
QuantiPy
########

.. image:: https://travis-ci.org/alexwie/quantipy.svg?branch=public
   :target: https://travis-ci.org/alexwie/quantipy
.. image:: https://img.shields.io/badge/Python%20versions-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
   :target: https://github.com/alexwie/quantipy

.. image:: misc/universitaet-innsbruck-logo-rgb-farbe.png
   :width: 3cm
	
A Python Framework for Quantum Many-Body simulations. 

:authors: Alexander Wietek, Michael Schuler
:license: GNU GPLv3

	     

*************
Main Features
*************

- creation of finite lattice geometries for simulating quantum
  many-body systems
- computation of model symmetries
- simple-to-use solvers for quantum many body systems,
  like Exact Diagonalization (QuickED package), Quantum Monte Carlo (t.b.a.)
  and DMRG (t.b.a.)
- plotting tools for visualizing results  

  
*************
Installation
*************
Using the python package manager pip, installation should be as simple as

.. code-block:: bash
		
    $ pip install quantipy

If you do not have root permissions try

.. code-block:: bash
		
    $ pip install quantipy --user

**************************
QuantiPy Documentation
**************************

The full QuantiPy documentation can be found at https://www.quantipy.org.

The QuantiPy documentation can be built from source when downloading the
source code. Change to directory

.. code-block:: bash
		
   '/path_to_quantipy/docs/'

and use

.. code-block:: bash
		
    $ make html

to build the documentation. The documentation can then be opened in a
browser with the link

.. code-block:: bash
		
   '/path_to_quantipy/docs/_build/html/index.html'

