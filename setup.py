import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="repcal",
    packages=['repcal'],
    version="0.1",
    author="Tomas Thelander",
    author_email="tomas@tthe.se",
    description="The French Republican calendar and decimal time in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dekadans/repcal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_dir={'':'src'},
)
