# movie_data_fetcher/setup.py

from setuptools import setup, find_packages

setup(
    name="movie_data_fetcher",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas'
    ]
)