from setuptools import setup

setup(
    name="ESROM",
    version="1.0",
    packages=["esrom"],
    data_files=[("share/applications", ["esrom.desktop"])],
    entry_points={
        "console_scripts": [
            "esrom=esrom.main:main",
        ],
    },
    install_requires=[
        "numpy",
        "pygame",
        "PyQt5",
    ],    
)
