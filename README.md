# ![Starpack](misc/starpack-dark.svg)

[![PyPI version](https://badge.fury.io/py/starpack.svg)](https://badge.fury.io/py/starpack)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/starpack)
[![codecov](https://codecov.io/gh/a360-starpack/starpack/branch/main/graph/badge.svg?token=N077SV8NA8)](https://codecov.io/gh/a360-starpack/starpack)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Starpack is tool to package and deploy production-ready packages of machine learning models.

This repository contains the code for the CLI and Python library for interacting with Starpack. To run Starpack locally, 
you will need to install a Python version listed in the badge above and 
[Docker Desktop](https://docs.docker.com/get-docker/) installed locally.

Currently, Starpack only supports packaging and deployment in local Docker Desktop or Docker Engine environments, 
but the generated Docker images can be pushed to remote repositories and deployed manually. 
It is currently on our roadmap to support deployment through Andromeda 360 down the line.


## Table of Contents

<!-- TOC -->
* [Starpack](#)
  * [Table of Contents](#table-of-contents)
  * [Quickstart](#quickstart)
  * [Full Command List](#full-command-list)
    * [Init](#init)
    * [Upload](#upload)
    * [Package](#package)
      * [Metadata](#metadata)
      * [Artifacts](#artifacts)
      * [Steps](#steps)
    * [Deploy](#deploy)
    * [Engine](#engine)
      * [Start](#start)
      * [Terminate](#terminate)
    * [Plugins](#plugins)
  * [Examples](#examples)
    * [Basic Example](#basic-example)
  * [Troubleshooting](#troubleshooting)
<!-- TOC -->

## Quickstart

To begin using Starpack, open a terminal and run 
```bash
pip install starpack
```

Then, you can initialize an existing or new directory with starter code and files by running the following in a terminal

```bash
starpack init ./path/you/want
```

Reconfigure your `starpack.yaml`, `predict.py`, and `requirements.txt` files to point to your model artifacts, properly ingest your data, and list your project dependencies, respectively. An example of these files can be found in the `examples` folder.

Finally, run the following terminal command to package and deploy your model locally

```bash
starpack deploy ./path/you/want
```



or alternatively in Python (such as in a notebook), the process can be run as follows:

```python
import starpack
from pathlib import Path

desired_directory = Path("./path/you/want")

starpack.initialize_directory(desired_directory)

# Reconfigure your files that have been initialized for your specific project

starpack.deploy_directory(desired_directory)
```


## Full Command List

A full command list can be found by running

```bash
starpack --help
```

Currently, the following top-level flags are available:

| Name               | Flag                   | Description                                                                                                     |
|--------------------|------------------------|-----------------------------------------------------------------------------------------------------------------|
| Version            | `--version`, `-v`      | Returns the version of the Starpack CLI installed in your environment                                           |
| Install Completion | `--install-completion` | Installs the auto-complete definitions for Starpack in your current terminal environment                        |
| Show Completion    | `--show-completion`    | Shows completion for your current shell so that you can copy or customize the configuration                     |
| Help               | `--help`               | Shows a nicely formatted table displaying the currently available commands, their flags, and their descriptions |

Additionally, we have a variety of commands to manage the Starpack Engine and generate packages.

### Init

The command, `starpack init`, when provided with a local path as an argument, will generate files to help you start developing your package definition. By default, Starpack will prompt for permission to overwrite existing files, unless the `--ovewrite/-o` flag is given.


| Filename           | Usage                                                                                                                                                                                                                    |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `requirements.txt` | Define your Python requirements that are necessary to run your deployment script. Dependencies are installed using `pip`.                                                                                                |
| `predict.py`       | Python script that defines how to handle an ingested Pandas DataFrame of data and transform it into your prediction output. This script should handle any data transformations and model loading required for inference. |
| `starpack.yaml`    | YAML definition of your Starpack packaging and deployment information. This file should define the locations of all necessary artifacts and build steps.                                                                 |


### Upload

The command, `starpack upload`, takes in a directory path and uploads its contents to the Starpack Engine. 
The name of this directory will be the name of the artifacts location within the Engine for when you package and deploy your model.

### Package

The command, `starpack package`, takes in a path, either a directory or `starpack.yaml` in order to package your model. 
If given a directory, Starpack will upload the contents to the Starpack Engine, then find any `starpack.yaml` file in 
the given directory to send as a payload to the Starpack Engine.


The `starpack.yaml` file contains two main sections, `package` and `deployment`. 
Furthermore, the YAML packaging section contains three main subsections:

1. Metadata
2. Artifacts
3. Steps


#### Metadata

Within the metadata section, you can define things such as the name, version, and author of the package. 
These fields should be generated when creating a directory using [`starpack init`](#init)

#### Artifacts

This section defines the name of your model artifacts location in the Engine system, as well as where you can find files such as your validation data, prediction script, and dependencies.

#### Steps

This section is an ordered list of your build steps. Each of your build steps uses either built-in or 
externally written plugins that can be called by name and optionally constrained by version of the plugin. 
Some plugins may need additional data, which will be included within the step's definition.

### Deploy

The command, `starpack deploy`, takes in a path, either a directory or `starpack.yaml` in order to deploy your packaged model.
If given a path, the assumption is made that the contents should be uploaded to the Engine, the YAML should be parsed for any packaging information, and finally, the deployment should be processed.
If given just a starpack.yaml, only the `deployment` step will be run, with the assumption that the other steps have already been run previously.


### Engine

There are several 

#### Start

The command, `starpack engine start`, is used to ensure the Starpack Engine is running or force the creation of a new container.

Finally, if you pass the `--force` or `-F` flags, you will force the deletion of any existing Starpack Engines and create a new Docker container for the Engine.

#### Terminate

The command, `starpack engine terminate`, is used to spin down any existing Starpack Engines running on your local machine. 
Additionally, the `--all` or `-A` flag can be passed to additionally delete any existing Docker Volumes and associated data from your machine.

### Plugins

The following plugins are available to use in either packaging or deployment:

| Name                 | Description                                                                              | Arguments                                                |
|----------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------|
| docker_desktop_push  | Tags an image and stores it in   the local Docker repository                             | `image_name`, `image_tags` (list), `wrapper`             |
| local_docker_deploy  | Deploys a packaged Starpack   model with a given wrapper to the local Docker environment | `port`, `wrapper` (list) with `name` and `port` for each |
| local_docker_find    | Finds already packaged model   artifacts in the local Docker environment                 | `wrapper`, `image` with `name` and `tag` sub-arguments   |
| fastapi              | Packages a set of model   artifacts with a FastAPI wrapper.                              |                                                          |
| streamlit            | Packages a set of model   artifacts with a Streamlit wrapper.                            |                                                          |

## Examples

### Basic Example

Under `examples/starpack_basic_example`, you can find a Jupyter notebook and associated files for deploying a Starpack package using both Streamlit and FastAPI. By following along with the notebook, then running `starpack deploy examples/starpack_basic_example` from the root of this repository, you will be able to see how one exports, defines, packages, and deploys a Starpack model.


## Troubleshooting

Before troubleshooting any issues, please run the two following commands in your terminal to ensure that you're running the latest version of both the Starpack CLI and Starpack Engine:

```
pip install starpack --upgrade
starpack engine start --force
```
