from setuptools import setup

setup(
    name="asciigraf",
    version="0.1.0",
    packages=["asciigraf"],
    description="A python library for making ascii-art into network graphs.",
    author="Peter Downs",
    author_email="antonlodder@gmail.com",
    url="https://github.com/AnjoMan/asciigraf",
    download_url="https://github.com/AnjoMan/asciigraf/archive/0.1.tar.gz",
    keywords=["graph", "network", "testing", "parser"],
    license="MIT",
    install_requires=[
        'networkx==1.11',
    ],
    extras_require={
        "test": ["pytest"],
    },
)
