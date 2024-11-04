# setup.py
from setuptools import setup, find_packages

setup(
    name="habit-tracker",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "pytest>=7.4.3",
        "python-json-logger>=2.0.7",
    ],
    entry_points={
        "console_scripts": [
            "habit-tracker=habit_tracker.cli:main",
        ],
    },
)