from setuptools import setup, find_packages

setup(
    name="meow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.4.3",
        "black>=23.11.0",
        "mypy>=1.7.1",
    ],
    entry_points={
        "console_scripts": [
            "meow=meow.meow:main",
        ],
    },
) 