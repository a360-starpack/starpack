# ![Starpack](misc/starpack-dark.svg)

[![PyPI version](https://badge.fury.io/py/starpack.svg)](https://badge.fury.io/py/starpack)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/starpack)
[![codecov](https://codecov.io/gh/a360-starpack/starpack/branch/main/graph/badge.svg?token=N077SV8NA8)](https://codecov.io/gh/a360-starpack/starpack)



Starpack is tool to package and deploy production-ready packages of maching learning models.

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
    * [Terminate](#terminate)
    * [Upload](#upload)
    * [Package](#package)
      * [Metadata](#metadata)
      * [Artifacts](#artifacts)
      * [Steps](#steps)
    * [Deploy](#deploy)
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

starpack.init(desired_directory)

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

The command, `starpack init`,  can be used to start up the Starpack Engine container in your local docker environment. 
Additionally, when provided with a local path as an argument, the Starpack Engine will generate files to help you start developing your package definition.

| Filename           | Usage                                                                                                                                                                                                                    |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `requirements.txt` | Define your Python requirements that are necessary to run your deployment script. Dependencies are installed using `pip`.                                                                                                |
| `predict.py`       | Python script that defines how to handle an ingested Pandas DataFrame of data and transform it into your prediction output. This script should handle any data transformations and model loading required for inference. |
| `starpack.yaml`    | YAML definition of your Starpack packaging and deployment information. This file should define the locations of all necessary artifacts and build steps.                                                                 |

The `starpack.yaml` file contains two main sections, `package` and `deployment`

Finally, if you pass the `--force` or `-F` flags, you will force the deletion of any existing Starpack Engines and create a new Docker container for the Engine.


### Terminate

The command, `starpack terminate`, is used to spin down any existing Starpack Engines running on your local machine. 
Additionally, the `--all` or `-A` flag can be passed to additionally delete any existing Docker Volumes and associated data from your machine.

### Upload

The command, `starpack upload`, takes in a directory path and uploads its contents to the Starpack Engine. 
The name of this directory will be the name of the artifacts location within the Engine for when you package and deploy your model.

### Package

The command, `starpack package`, takes in a path, either a directory or `starpack.yaml` in order to package your model. 
If given a directory, Starpack will upload the contents to the Starpack Engine, then find any `starpack.yaml` file in 
the given directory to send as a payload to the Starpack Engine.

The YAML packging section contains three main subsections:

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
If given just a starpack.yaml, only the deploy step will be run, with the assumption that the other steps have already been run previously.

