from setuptools import setup

setup(
    name='pipoke',
    version='0.0.1',
    url='https://https://github.com/thorwhalen/pipoke',
    license='Apache Software License',
    author='Thor Whalen',
    install_requires=[
        'bs4',
        'requests',
        'argh'
    ],
    author_email='thorwhalen1@gmail.com',
    description='Utils to acquire stuff from pypi and interrogate it.',
    include_package_data=True,
    platforms='any',
)
