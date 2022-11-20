from pathlib import Path
from setuptools import setup


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="bayan_address",
    version="0.2.1",
    description="A Python-based address parser for Philippines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netervati/bayan_address",
    author="Christopher Tabula",
    author_email="netervati@gmail.com",
    license="MIT License",
    packages=["bayan_address", "bayan_address/parser", "bayan_address/lib"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
