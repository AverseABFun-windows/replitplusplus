"""
This template is the framework for creating and distributing
packages on the official Python Package Index (or PyPi).

The following commands will help you compile your 
project into a "dist" file for distribution.

Created by @IreTheKID
"""

import os

print("Upgrading pip")
os.system('pip install --upgrade pip')
print("Installing wheel")
os.system('pip install wheel')
print("Installing twine")
os.system('pip install twine')
print("Installing keyring")
os.system('pip install keyring')
print("Compiling project")
os.system('python replitplusplus/setup.py sdist bdist_wheel')
print("Uploading project")
os.system('twine upload dist/*')