import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as f:
    README = f.read()

setup(
    name="watched-sdk",
    version="0.0.3",
    description="WATCHED.com Python SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/watchedcom/sdk-python",
    author="WATCHED",
    author_email="dev@watched.com",
    packages=find_packages(),
    install_requires=["watched-schema", "diskcache",
                      "flask", "requests", "markdown"],
    python_requires=">=3.4",
)
