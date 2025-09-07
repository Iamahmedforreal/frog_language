"""
Setup script for Forg Language Compiler

This script allows the Forg compiler to be installed as a Python package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README", "r", encoding="utf-8") as f:
        return f.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="forg-compiler",
    version="1.0.0",
    author="Forg Team",
    author_email="forg@example.com",
    description="A modern programming language compiler that compiles Forg to LLVM IR",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/forg-compiler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "profiling": [
            "memory-profiler>=0.60.0",
            "line-profiler>=4.0.0",
            "psutil>=5.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "forg=main:main",
            "forg-test=test_runner:main",
            "forg-bench=performance:run_performance_suite",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["tests/*.forg", "debug/.gitkeep", "output/.gitkeep"],
    },
    project_urls={
        "Bug Reports": "https://github.com/example/forg-compiler/issues",
        "Source": "https://github.com/example/forg-compiler",
        "Documentation": "https://forg-compiler.readthedocs.io/",
    },
)
