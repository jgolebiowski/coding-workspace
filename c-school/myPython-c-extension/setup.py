#!/usr/bin/env python3

from distutils.core import setup, Extension
import os

extra_compile_args = ["-std=c++11", "-Wall", "-Wextra"]
extra_compile_args += ["-DNDEBUG", "-O3"]
extra_compile_args += ["-Wno-unused-parameter",
                       "-Wno-missing-field-initializers"]

os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"


module = Extension('helloworld',
                   include_dirs=['include'],
                   libraries=["stdc++"],
                   library_dirs=['lib'],
                   sources=["src/bind.cc", "src/libmypy.cc"],
                   extra_compile_args=extra_compile_args,
                   language='c++11',)


setup(
    name='helloworld',
    version='1.0',
    description='This is a demo package',
    author='Jacek Golebiowski',
    author_email='golebiowski.j@gmail.com',
    url='https://docs.python.org/extending/building',
    long_description='''
This is really just a demo package.
''',
    ext_modules=[module]
)
