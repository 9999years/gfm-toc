from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gfmtoc',
    version='1.1.0',
    description='Generates Github-Flavored Markdown Tables of Contents from `readme.md`s',
    long_description=long_description,
    url='https://github.com/9999years/gfm-toc',
    author='Rebecca Turner',
    author_email='637275@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords='markdown toc table contents',

    packages=find_packages(),

    # Run-time dependencies
    install_requires=['urllib3'],

    entry_points={
        'console_scripts': [
            'gfmtoc=gfmtoc.gfmtoc:main',
        ],
    },
)
