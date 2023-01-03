from setuptools import setup
from Cython.Build import cythonize
import numpy
setup(
    name = 'cython_improved',
    ext_modules = cythonize("cython_improved.pyx"),
    include_dirs=[numpy.get_include()]
)