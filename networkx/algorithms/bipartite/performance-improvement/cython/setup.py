from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'cython_improved',
    ext_modules = cythonize("cython_improved.pyx")
)