import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="",
    version="0.0.1",
    author="AB and JS",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: UNLICENSE",
        "Operating System :: Linux/Unix",
    ],
    python_requires=">3.5",
    install_requires=[
        "mne",
        "numpy",
        "scipy",
        "pandas",
        "statsmodels",
        "shiny"
    ],
)
