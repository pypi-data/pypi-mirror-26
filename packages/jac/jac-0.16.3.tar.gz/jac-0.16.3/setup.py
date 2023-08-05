import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='jac',
    author='Jayson Reis',
    author_email='santosdosreis@gmail.com',
    version='0.16.3',
    packages=find_packages(exclude=('tests*', )),
    install_requires=open('requirements.txt').readlines(),
    description='A Jinja extension (compatible with Flask and other frameworks) '
                'to compile and/or compress your assets.',
    long_description=read('README.md'),
    url='https://github.com/jaysonsantos/jinja-assets-compressor',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
