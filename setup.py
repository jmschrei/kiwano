from setuptools import setup, find_packages

setup(
    name='kiwano',
    version='0.1.0',
    author='Jacob Schreiber',
    author_email='jmschreiber91@gmail.com',
    packages=['kiwano'],
    package_dir={'': 'src'},
    scripts=['kiwano'],
    url='http://pypi.python.org/pypi/kiwano/',
    license='LICENSE.txt',
    description='Kiwano is an implementation of an approach for prioritizing epigenomic and transcriptomic experiments.',
    install_requires=[
        "apricot-select >= 0.3.0",
        "numpy >= 1.16.2"
    ],
)