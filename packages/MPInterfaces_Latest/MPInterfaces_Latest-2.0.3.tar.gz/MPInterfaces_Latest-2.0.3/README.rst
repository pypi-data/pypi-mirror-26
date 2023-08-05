.. image:: https://travis-ci.org/henniggroup/MPInterfaces.svg?branch=master
.. image:: https://codecov.io/gh/henniggroup/MPInterfaces/coverage.svg?branch=master

MPinterfaces is a python package that enables high throughput Density
Functional Theory(DFT) analysis of arbitrary material interfaces(two dimensional
materials, hetero-structure, ligand capped
nanoparticles and surfaces in the presence of solvents) using
VASP_, VASPsol_, LAMMPS_, materialsproject_ database
as well as their open source tools_ and a little bit of ase_.

.. _materialsproject: https://github.com/materialsproject

.. _VASPsol: https://github.com/henniggroup/VASPsol

.. _VASP: http://www.vasp.at/

.. _tools: https://github.com/materialsproject

.. _LAMMPS: http://lammps.sandia.gov/

.. _ase: https://wiki.fysik.dtu.dk/ase/

.. image:: https://github.com/henniggroup/MPInterfaces/blob/master/docs/mpinterfaces-logo.png
   :width: 75 %
   :align: center

Installation
==============

Prepping - Setting up Virtual Environments with Miniconda
---------------------------------------------------------

We recommend setting up virtual environment
using Miniconda which can be installed according to their instructions from https://conda.io/miniconda.html

Follow the following steps to set up virtual environment using Miniconda

$ conda create -n name_of_your_environment python=3.6

On Mac OS and Linux

$ source activate name_of_your_environment

Install some useful packages with conda and link them to your created miniconda
virtual environment <name_of_your_environment>

$ conda install numpy scipy matplotlib ipython pandas

On Windows:

$ activate name_of_your_environment

Note: You will need to have C++ libraries properly
installed for the package to install correctly on Windows.

For teaching and demo purposes, we recommend using Microsoft Azure notebooks,
an example of which is at https://notebooks.azure.com/JoshGabriel92/libraries/PourbaixCourse
which contains two notebooks that illustrate installing pymatgen and pyhull for on the fly
data science tutorials. We have one notebook FeOH_Example.ipynb for Pourbaix diagrams and an MPInterfacesDemo that illustrate other features of the MPInterfaces code with more to come.

Note for SuperComputer Clusters with Linux OS:

HiperGator2 and other linux based supercomputing clusters
have shared modules one of which are the C++ modules under gcc.
This needs to be loaded before any of the aforementioned
gcc/5.2.0 has all the shared libraries
required for a successful installation.

Do the following on HiperGator2 before you create
the Miniconda environment:

$ module purge
$ module load gcc/5.2.0

Get the stable release version from PyPI
----------------------------------------

Once you have a nicely prepped virtual environment with miniconda
and you do not seek to do extensive code development/contributions,
we recommend installing from PyPI with:

$ pip install MPInterfaces_Latest

Configuration
--------------

Once installed MPInterfaces and its modules are available for usage in the
virtual environment <name_of_your_environment> that you created. To use the MPInterfaces
package for managing DFT calculations with the queuing system on your supercomputing cluster
(SLURM ad PBS suppported) we recommend using the command line functionality "mpint_flow" which is a command already installed into your virtual environment
path upon installation.

To understand its usage do:

$ mpint_flow -h

The mpint_flow command has a total of 6 subcommands, the first of which is load_settings and
will be used to load your configuration file. By configuring, we mean setting environment
variables for the pymatgen package and the submit file format for the batch queuing system.

$ mpint_flow load_settings -i '{"MAPI_KEY":"your_Materials_Project_Key","potentials":"path/to/your/pseudopotentials"}'

This loads your MAPI_KEY (materials project API key) and the POTCAR environment variable PMG_VASP_PSP_DIR

NOTE: your pseudopotentials should be arranged according to the directory structure:

POTCAR -
  - POT_GGA_PAW_PBE
     - Element
        - POTCAR
        - PSCTR
  - POT_LDA_PAW
    - Element
        - POTCAR
        - PSCTR
      ..etc.

For the batch system integration:

$ mpint_flow load_settings -i '{"QUEUE_SYSTEM":"your_batch_system"}'

and for the submit file using ipython:

$ ipython

.. code_block:: python

   import yaml
   from mpinterfaces import QUEUE_TEMPLATE
   qtemp = yaml.load(open(QUEUE_TEMPLATE+'qtemplate.yaml'))
   print (qtemp)
   # view the default qtemp and edit the keys and values according to
   # your batch system and finally doing qtemp.update({your_submit_file_as_a_dict})
   with open(QUEUE_TEMPLATE+'qtemplate.yaml', 'w') as new_qtemp:
      yaml.dump(qtemp, new_qtemp, default_flow_style=False)

Other configuration variables to configure include the path to your VASP binaries and the
vdW kernel file.

You can find a list of all such configuration variables by opening the config file that
was created for you by MPInterfaces in your home directory: ~/.mpint_config.yaml

$ mpint_flow load_settings -i '{"normal_binary":"your_non_2D_vasp_binary"}'

Running your first project
---------------------------

An example project_file.yaml is available in your PACKAGE_PATH and
we recommend that you read and understand this file and the comments
entered in it. You can create your own workflows based on this file by copying
it to your desired working directory, preferrably scratch space on your supercomputer.

When in your desired project directory, you can start your first project by doing:

$ mpint_flow start_project -i project_file.yaml

To validate the first step with MaterialsProject's Custodian package with its VaspErrorHandlers, use:

$ mpint_flow check_project -i project_file.yaml

If errors are encountered they are corrected as per Custodian's handlers and will be documented in
the <ProjectName>_<WorkflowStepName>_CustodianReport.yaml files. If you do not agree with the correction
you can always go to the individual directories listed in the CustodianReport.yaml and change according
to your decision.

To rerun the jobs which failed:

$ mpint_flow rerun_project -i <ProjectName>_<WorkflowStepName>_CustodianReport.yaml

To go to the next step of your computational workflow:

$ mpint_flow continue_project -i project_file.yaml

To analyze each step of your computational workflow by a specified script

$ mpint_flow analyze_project -i project_file.yaml


For Developers
--------------

Get the latest bleeding edge version:

If you would like to develop and contribute we recommend getting the bleeding edge
copy from the github repository.

If you already have a local copy, steps 1 and 2 of the following instructions
can be skipped. Just do a "git pull" from the MPInterfaces folder and go to
step 3(if the local copy was installed in the develop mode this step can be skipped too).

Note: on using virtual environments on your own machine, we recommend to use Miniconda.

1. Clone the latest version from github

  - git clone https://github.com/henniggroup/MPInterfaces.git

2. cd MPInterfaces

3. python setup.py install(or develop)

4. Copy the mpint_config.yaml file from config_files/mpint_config.yaml
   to mpinterfaces/mpint_config.yaml
   and update the file so that you have the following
   environment variables :

   - MAPI_KEY=the_key_obtained_from_materialsproject

   - PMG_VASP_PSP_DIR=path_to_vasp_potcar_files


How to Install Latest Pymatgen
------------------------------

See http://pymatgen.org/#getting-pymatgen


Documentation
==============

A very minimal documentation is avaiable at

http://henniggroup.github.io/MPInterfaces/

and work is underway to improve it.


Usage
==========

We use pymatgen tools for all structure manipulation tasks, so it would
be a good idea to start from here:

http://pymatgen.org/#using-pymatgen

The examples folder contain some sample scripts that demonstrate the
usage of mpinterfaces as well as materialsproject packages. For basic
usage please see **docs/usage.rst**.


Cite
======

If you use MPInterfaces for your work, please cite the paper: mpinterfaces-paper_

.. _mpinterfaces-paper: http://www.sciencedirect.com/science/article/pii/S0927025616302440


License
=======

MPInterfaces is released under the MIT License.::

    Copyright (c) 2014-2017 Henniggroup Cornell/University of Florida & NIST

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
    the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
    IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Contributing
=============

We try to follow the coding style used by pymatgen(PEP8):

http://pymatgen.org/contributing.html#coding-guidelines


Authors
=========

Kiran Mathew

Joshua Gabriel

Michael Ashton

Arunima Singh

Joshua T. Paul

Seve G. Monahan

Richard G. Hennig
