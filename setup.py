import os
from distutils.core import setup
from setuptools import find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="marketify",
    packages=find_packages(),
    version="0.2.2",
    license="MIT",
    description="A micro-library that pulls data from exchanges",
    long_description=read("README.md"),
    author="Marcelino Franco",
    author_email="mcfranco16@gmail.com",
    url="https://github.com/mfranco1/marketify",
    download_url="https://github.com/mfranco1/marketify/archive/v_022.tar.gz",
    keywords=["Trading", "Market", "Exchange", "Websocket", "Async"],
    install_requires=["aiodns", "aiohttp", "Rx", "websockets"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
