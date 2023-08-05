# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import versioneer

with open('README.rst') as f:
    readme = f.read()
    
setup(
    name='pybbfmr',
    author='Hannes Maier-Flaig',
    author_email='hannes@maier-flaig.de',
    url='https://gitlab.com/wmi/pybbfmr/',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    license='MIT',
    long_description=readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords='bbfmr broadband FMR ferromagnetic resonance magnon',
    install_requires=[
        'numpy',
        'lmfit',
        'matplotlib',
        'nptdms',
    ],
    python_requires='>=3',
)
