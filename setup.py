from setuptools import setup
import os


def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except:
        return ""


ujoin = lambda *args: '/'.join(args)

name = os.path.basename(os.path.dirname(__file__))
version = '0.0.2'
root_url = 'https://github.com/thorwhalen/'

setup(
    name=f"{name}",
    version=f'{version}',
    url=ujoin(f"{root_url}", f"{name}"),
    license='Apache Software License',
    author='Thor Whalen',
    install_requires=[
        'bs4',
        'requests',
        'argh'
    ],
    author_email='thorwhalen1@gmail.com',
    description='Utils to acquire stuff from pypi and interrogate it.',
    keywords=['pip', 'pypi', 'packaging'],
    include_package_data=True,
    platforms='any',
    long_description=readme(),
    long_description_content_type="text/markdown",
    download_url=ujoin(f'{root_url}', f'archive/v{version}.zip'),

)
