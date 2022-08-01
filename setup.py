import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "chaostoolkit_elasticsearch",
    version = "0.0.1",
    author = "Vodafone Systems Team",
    author_email = "gabor.gerencser@vodafone.com",
    description = "Elasticsearch module for chaostoolkit",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: No License",
        "Operating System :: OS Independent" ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
