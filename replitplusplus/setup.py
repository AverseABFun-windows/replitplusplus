import setuptools

with open("replitplusplus/README.md", "r") as fhandle:
    long_description = fhandle.read()

setuptools.setup(
    name="replitplusplus",
    version="1.0",
    author="AverseABFun",
    author_email="averse.abfun@gmail.com",
    description="The replit package, but better!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AverseABFun-windows/replitplusplus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
