from distutils.core import setup

__author__ = 'Rob MacKinnon <rob.mackinnon@gmail.com>'

setup(
    # Application name:
    name="Minecraft Overviewer DB",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Rob MacKinnon",
    author_email="rob.mackinnon@gmail.com",

    # Packages
    # Include additional files into the package
    include_package_data=False,

    # Details
    url="http://github.com/rmackinnon/Minecraft-Overviewer-DB",

    #
    license="LICENSE",
    description="Database backend for Minecraft Overviewer",

    # long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "sqlite3",
    ],
)
