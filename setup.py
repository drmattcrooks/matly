from setuptools import find_packages, setup

setup(
    name='mattsplotlib-dev',
    version='0.1',
    license='',
    description='mattsplotlib-dev syntax for plotly',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Matt Crooks',
)