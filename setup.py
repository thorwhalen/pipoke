import os


def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except:
        return ""


def my_setup(print_params=True, **setup_kwargs):
    from setuptools import setup
    if print_params:
        import json
        print("Setup params -------------------------------------------------------")
        print(json.dumps(setup_kwargs, indent=2))
        print("--------------------------------------------------------------------")
    setup(**setup_kwargs)


name = os.path.split(os.path.dirname(__file__))[-1]
version = '0.0.4'
root_url = 'https://github.com/thorwhalen'

setup_kwargs = dict(
    name=f"{name}",
    version=f'{version}',
    url=f"{root_url}/{name}",
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
    download_url=f'{root_url}/{name}/archive/v{version}.zip',

)

my_setup(**setup_kwargs)

# setup_kwargs = dict(
#     name='pipoke',
#     version='0.0.3',
#     url='https://https://github.com/thorwhalen/pipoke',
#     license='Apache Software License',
#     author='Thor Whalen',
#     install_requires=[
#         'bs4',
#         'requests',
#         'argh'
#     ],
#     author_email='thorwhalen1@gmail.com',
#     description='Utils to work with pypi, packaging, etc.',
#     include_package_data=True,
#     platforms='any',
# )
#
# my_setup(**setup_kwargs)
