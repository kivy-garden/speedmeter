"""See README.md for package documentation."""

from setuptools import setup, find_packages

from glob import glob
from io import open
from os import path

from kivy_garden.speedmeter import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

URL = 'https://github.com/kivy-garden/speedmeter'

setup(
    name='kivy_garden.speedmeter',
    version=__version__,
    description=('A versatile gauge to display and input physical values '
                 'with a rotating handle / dial.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Ch. Tronche',
    author_email='ch@tronche.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    keywords='Kivy kivy-garden SpeedMeter',

    packages=['kivy_garden.speedmeter'],
    install_requires=[],
    extras_require={
        'dev': ['pytest>=2'],
        'travis': ['coveralls'],
    },
    package_data={'kivy_garden.speedmeter': [ 'images/*.png' ]},
    data_files=[('share/kivy_garden/speedmeter',
                 glob('demos/*.py') + glob('demos/*.kv') + glob('demos/*.png'))],
    entry_points={},
    project_urls={
        'Bug Reports': URL + '/issues',
        'Source': URL,
    },
)
