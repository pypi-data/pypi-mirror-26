import os

from setuptools import setup
from setuptools.extension import Extension
from setuptools.command.sdist import sdist as _sdist

#Instalise the __version__ variable
execfile(os.path.join('parabam','_version.py'))

cmdclass = {}
ext_modules = [
      Extension("parabam.core", [ "parabam/core.c" ]),
      Extension("parabam.chaser", ["parabam/chaser.c"]),
      Extension("parabam.merger", ["parabam/merger.c"]),
      Extension("parabam.command.subset", ["parabam/command/subset.c"]),
      Extension("parabam.command.stat", ["parabam/command/stat.c"]),
      Extension("parabam.command.core", ["parabam/command/core.c"])] 

class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        from Cython.Build import cythonize
        cythonize(['parabam/chaser.pyx','parabam/core.pyx','parabam/merger.pyx',
                   'parabam/command/core.pyx','parabam/command/stat.pyx',
                   'parabam/command/subset.pyx'])
        _sdist.run(self)
        
cmdclass['sdist'] = sdist

setup(name='parabam',
      description='Parallel BAM File Analysis',
      version=__version__,
      author="JHR Farmery",
      license='GPL',
      author_email = 'jhrf2@cam.ac.uk',
      packages = ['parabam','parabam.command'],
      package_dir = {'parabam':'parabam','parabam.command':'parabam/command'},
      install_requires = ['numpy','argparse','pysam >= 0.10.0'],
      scripts = ['parabam/bin/parabam'],
      cmdclass = cmdclass,
      ext_modules=ext_modules
      )
