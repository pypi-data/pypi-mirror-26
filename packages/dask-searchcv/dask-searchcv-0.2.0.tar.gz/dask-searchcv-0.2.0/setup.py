from os.path import exists

from setuptools import setup
import versioneer

install_requires = ["dask >= 0.14.0",
                    "toolz >= 0.8.2",
                    "scikit-learn >= 0.18.0",
                    "scipy >= 0.13.0",
                    "numpy >= 1.8.0"]

setup(name='dask-searchcv',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      license='BSD',
      url='http://github.com/dask/dask-searchcv',
      maintainer='Jim Crist',
      maintainer_email='jcrist@continuum.io',
      install_requires=install_requires,
      description='Tools for doing hyperparameter search with Scikit-Learn and Dask',
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      packages=['dask_searchcv', 'dask_searchcv.tests'])
