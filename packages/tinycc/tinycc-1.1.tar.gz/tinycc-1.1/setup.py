import os
from os.path import join as joinpath
import sys

#from setuptools import setup
from distutils.core import setup

# Pull version number out of package init file.
version = ""
with open(joinpath('tinycc','__init__.py')) as fid:
    for line in fid:
        if line.startswith('__version__'):
            version = line.split('"')[1]
            break
if not version:
    raise RuntimeError("Could not extract version number from package init")


# Walk the include tree keeping a list of directories to install.
include_dirs = ['include'] + [
    joinpath(path[7:], d)
    for path, dirs, _  in os.walk(joinpath('tinycc','include'))
    for d in dirs
    ]

# Pick the target architecture.
arch = "amd64" if sys.maxsize>2**32 else "x86"

# Note: tinycc.arch is a fake package used to trick package_data into
# combining data from different directories.  See the following:
#
#    https://stackoverflow.com/questions/37451084/combine-directories-using-distutils
#

# Put it all together...
setup(
    name="tinycc",
    version = version,
    description = "TinyCC compiler bundle for windows",
    long_description=open('README.rst').read(),
    author = "SasView Collaboration",
    author_email = "management@sasview.org",
    url = "https://github.com/SasView/tinycc",
    keywords = "ctypes compiler",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development :: Compilers',
    ],
    packages=['tinycc', 'tinycc.arch'],
    package_dir={'tinycc.arch': 'tinycc/%s/arch'%arch},
    package_data={
        'tinycc': [joinpath(d, "*.h") for d in include_dirs],
        'tinycc.arch': ['../*.exe', '../*.dll', '../lib/*', '../libtcc/*']
    },
    #install_requires = required,
)
