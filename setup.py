from setuptools import find_packages, setup


# README load in
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="starpack",
    version="0.0.4",
    package_dir={"": "src"},
    packages=find_packages("src"),
    author="Irvin Shen",
    author_email="irvin.shen@andromeda360.ai",
    license="Apache License Version 2.0",
    description="A utility to package and productionize ML models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a360-starpack/starpack",
    keywords=["Swagger", "OpenAPI", "ModelOps", "CLI", "DataScience", "DevOps"],
    project_urls={
        "Bug Tracker": "https://github.com/a360-starpack/starpack/issues",
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
        "Programming Language :: Python :: 3.10"
    ],
    include_package_data=True,
    install_requires=[
        "typer[all]>=0.6.1,<1.0.0",
        "docker>=6.0.0,<7.0.0",
        "requests>=2.28.1,<3.0.0",
    ],
    extras_require={
        "dev": ["pytest==7.1.2",
                "pytest-cov==3.0.0",
                "requests-mock==1.10.0"
                ]
    },
    entry_points = {
        "console_scripts" : [
            "starpack = starpack.__main__:app"
        ]
    }
)
