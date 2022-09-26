from setuptools import find_packages, setup

# README load in
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="starpack",
    version="0.1.0",
    packages=find_packages(
        where='src'
    ),
    author="Irvin Shen",
    author_email="irvin.shen@andromeda360.ai",
    license="Apache License Version 2.0",
    description="This utility helps you deploy your code as an API locally on your machine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NAN",
    keywords=["Swagger", "OpenAPI", "ModelOps", "CLI", "DataScience"],
    project_urls={
        "Bug Tracker": "https://github.com/NAN/issues",
    },

    classifiers=[
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    install_requires=[
        "typer>=0.6.1,<1.0.0",
        "docker>=6.0.0,<7.0.0",
        "requests>=2.28.1,<3.0.0"
    ],
)
