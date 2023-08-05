"""
CBMPy: setup.py
===============
PySCeS Constraint Based Modelling (http://cbmpy.sourceforge.net)
Copyright (C) 2010-2017 Brett G. Olivier, VU University Amsterdam, Amsterdam, The Netherlands

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

Author: Brett G. Olivier
Contact email: bgoli@users.sourceforge.net
Last edit: $Author: bgoli $ ($Id: setup.py 628 2017-10-20 12:33:26Z bgoli $)

"""

import os
local_path = os.path.dirname(os.path.abspath(os.sys.argv[0]))

USE_SETUPTOOLS = True

if USE_SETUPTOOLS:
    # setuptools
    from setuptools import setup
else:
    # distutils
    from distutils.core import setup

# new more elegant hack implemented to get rid of evil hack and allow pip install
"""
# I suspect this is a distutils specific evil hack to get the data into the install directory
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']
"""
mydata_files = []
# new hack should get rid of the need for this
#mydata_files.append((os.path.join('cbmpy', 'models'),\
#[os.path.join(local_path,'src','models',examplefile) for examplefile in os.listdir(os.path.join(local_path,'src','models'))\
#if examplefile.endswith('.xml')]))

# new hack should get rid of the need for this
#mydata_files.append((os.path.join('cbmpy', 'nosetests'),\
#[os.path.join(local_path,'src','nosetests',examplefile) for examplefile in os.listdir(os.path.join(local_path,'src','nosetests'))\
#if examplefile.endswith('.xml') or examplefile.endswith('.json')]))

# release
try:
    STATUS = 'r'+'$Rev: 628 $'.replace('Rev: ','').replace('$','').strip()
except:
    STATUS = 'beta'

mypackages= ['cbmpy', 'cbmpy.fluxmodules', 'cbmpy.models', 'cbmpy.nosetests', 'cbmpy.solver']

setup(
 package_dir = {'cbmpy' : 'src'},
 packages = mypackages,
 data_files = mydata_files,
 name = "cbmpy",
 summary = "CBMPy: Constraint Based Modelling in Python",
 #version = "0.7.19.{}".format(STATUS),
 version = "0.7.18",
 maintainer = 'Brett G. Olivier',
 author = 'Brett G. Olivier',
 maintainer_email = 'bgoli@users.sourceforge.net',
    url = "http://cbmpy.sourceforge.net",
    download_url = "http://sourceforge.net/projects/cbmpy/files/release/0.7/",
    license = "GNU General Public License (GPL)",
    keywords = "computational systems biology, modelling, simulation, genome scale models, sbml, constraint-based modelling, fbc, linear programming, groups, standard" ,
    #zip_safe = False,
    requires = ['numpy', 'sympy', 'libsbml', 'nose'],
    platforms = ["Windows", "Linux", "Mac"],
    classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Scientific/Engineering :: Chemistry'
     ],
 description = """PySCeS CBMPy (http://cbmpy.sourceforge.net) is a new platform for constraint based modelling and analysis. It has been designed using principles developed in the PySCeS simulation software project: usability, flexibility and accessibility"""
 )
try:
    import cbmpy
except ImportError:
    pass
