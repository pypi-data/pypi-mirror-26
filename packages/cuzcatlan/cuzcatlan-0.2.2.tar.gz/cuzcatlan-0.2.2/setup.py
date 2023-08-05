from setuptools import setup

setup(name='cuzcatlan',
      version='0.2.2',
      description="Edwin Juarez's personal library.",
      url='https://github.com/edjuaro/cuzcatlan',
      author='Edwin F. Juarez',
      author_email='ejuarez@ucsd.edu',
      license='MIT',
      packages=['cuzcatlan'],
      zip_safe=False,
      install_requires=[
          'numpy',
          'scipy',
          'pandas',
          'matplotlib',
          ],
      )
