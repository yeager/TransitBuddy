"""Setup för TransitBuddy."""

from setuptools import setup, find_packages

setup(
    name="transitbuddy",
    version="1.0.0",
    description="Enkel reseplanerare med steg-för-steg-instruktioner",
    author="TransitBuddy",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["PyGObject>=3.42"],
    entry_points={
        "console_scripts": [
            "transitbuddy=transitbuddy.main:main",
        ],
    },
    data_files=[
        ("share/applications", ["se.transitbuddy.app.desktop"]),
    ],
)
