.. include:: project-links.txt
.. include:: abbreviation.txt

.. _installation-page:

==============
 Installation
==============

**Note to Packagers: Please don't create Musica package (PiPY do the job)**

**Musica uses musica-toolkit on Pypi since the name is registered by an invalid empty project.** see
`PEP 541 -- Package Index Name Retention <https://www.python.org/dev/peps/pep-0541/>`_

On Windows
----------

Firstly, you have to install the `Anaconda Distribution <https://www.anaconda.com/download/>`_ so
as to get a full featured Python 3 environment.

Then open the `Anaconda Navigator <https://docs.continuum.io/anaconda/navigator/>`_ and launch a console for your root environment.

You can now run *pip* to install Musica in your root environment using this command:

.. code-block:: sh

  pip install musica-toolkit

On Linux
--------

Firstly, you have to install Python 3 from your distribution.

Then you can install Musica using *pip* or from source. See supra.

On OSX
------

There are several ways to get Python on OSX:

 * use the built in Python
 * install `Miniconda <https://conda.io/miniconda.html>`_
 * install the `Anaconda Distribution <https://www.anaconda.com/download/>`_.
 * install from Brew `brew install python3` **(reported to work)**

You can install Musica using *pip* or from source. See supra.

Installation from PyPi Repository
---------------------------------

Musica is available on the Python Packages |Pypi|_ repository at |Musica@pypi|

Run this command in the console to install the latest release:

.. code-block:: sh

  pip install musica-toolkit

Install a more recent version from Github
-----------------------------------------

If you want to install a version which is not yet released on Pypi, you can use one of theses
commands to install the stable or devel branch:

.. code-block:: sh

  pip install git+https://github.com/FabriceSalvaire/Musica

  pip install git+https://github.com/FabriceSalvaire/Musica@devel

Installation from Source
------------------------

The Musica source code is hosted at |Musica@github|

.. add link to pages ...

You have two solution to get the source code, the first one is to clone the repository, but if you
are not familiar with Git then you can simply download an archive either from the Musica Pypi page
(at the bottom) or the GitHub page (see clone or download button).

To clone the Git repository, run this command in a console:

.. code-block:: sh

  git clone https://github.com/FabriceSalvaire/Musica.git

Then to build and install Musica run these commands:

.. code-block:: sh

  python setup.py build
  python setup.py install

Dependencies
------------

Musica requires the following dependencies:

 * |Python|_ 3
 * |Numpy|_
 * Fixme: complete

Also it is recommanded to have these Python modules:

 * |IPython|_

.. * pip
.. * virtualenv

To generate the documentation, you will need in addition:

 * |Sphinx|_
