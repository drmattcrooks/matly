from setuptools import find_packages, setup

setup(
    name='matly',
    version='0.3.7',
    license='',
    description='matplotlib syntax for plotly',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Matt Crooks',
)
