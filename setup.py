import setuptools
import io

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = setuptools.find_packages(exclude=["unit_tests", "unit_tests.*"])

test_require = []
with io.open('requirements-dev.txt') as f:
    test_require = [l.strip() for l in f if not l.startswith('#')]

install_require = []
with io.open('requirements.txt') as f:
    install_require = [l.strip() for l in f if not l.startswith('#')]

setuptools.setup(
    name = "chaostoolkit_elasticsearch",
    long_description=long_description,
    license="Apache License Version 2.0",
    version = "0.0.1",
    author = "Vodafone Systems Team",
    author_email = "gabor.gerencser@vodafone.com",
    description = "Elasticsearch module for chaostoolkit",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent" ],
    packages=packages,
    install_requires=install_require,
    tests_require=test_require,
    python_requires=">=3.7",
)
