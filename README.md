<a href="https://uk.sagepub.com/en-gb/eur/doing-computational-social-science/book266031"><img src="http://www.johnmclevey.com/assets/images/dcss_cover.png" width="150"  align="right"/></a>

# DOING COMPUTATIONAL SOCIAL SCIENCE

Hello! This git repository contains the supplementary materials for [John McLevey (2021) *Doing Computational Social Science*, Sage, UK](https://uk.sagepub.com/en-gb/eur/doing-computational-social-science/book266031). A few small things have changed in this repo since the book was published. **If you are using this repo alongside the book, please take a moment to read this file carefully.** It will make it easier to access and use the resources you are looking for. If you run into any problems, please [file an issue](https://github.com/UWNETLAB/dcss_supplementary/issues). 

# THE DCSS VIRTUAL ENVIRONMENT

The book refers to a DCSS virtual environment that can be created from the YAML file `environment.yml`, which you can find in the root directory of this repo. It has all the packages and other dependencies needed to execute the code in the book. You can create it on your own system using Conda, as described in the book. From this directory:

```bash
conda env create -f environment.yml
```

Conda can be a little slow, so be patient. Once it has downloaded and installed the packages, you can activate and use the virtual environment as expected: 

```bash
conda activate dcss
```

But... what if things don't go as expected? 

## What to do if you run into memory issues and are unable to install the environment

As far as virtual environments go, this is a pretty big one. If you are on an older system, or one with limited memory, you might run into some installation issues. In that case, we recommend that you use [Mamba](https://mamba.readthedocs.io/en/latest/index.html) instead of Conda to install the environment. Mamba is a much faster and more efficient cross-platform package manager than Conda, and can easily handle installing the DCSS environment. You may want to use it even if you aren't using a system with limited memory!

You can find the installation instructions for Mamba [here](https://github.com/conda-forge/miniforge#mambaforge). In most cases, you should be able to just run the command below, which downloads the Mamba install script (with `curl`) and then runs the installer.

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
bash Mambaforge-$(uname)-$(uname -m).sh
```

Once you have Mamba installed, you can use it in place of Conda. 

```bash
mamba env create -f environment.yml
```

and to activate, 

```bash
mamba activate dcss
```

## What to do if you are on a Windows system and are unable to install the environment

The DCSS environment comes with [Tiago Peixoto's](https://skewed.de/tiago) (`graph-tool`)[http://graph-tool.skewed.de], which is challenging to install on Windows systems. If you are running into this issue and don't have access to a system running linux or macOS, then you can install a version of the DCSS environment that does not include `graph-tool`. That environment is `environment-windows-no-gt.yml`, and you can also find in the root directory. 

```bash
mamba env create -f environment-windows-no-gt.yml
mamba activate dcss
```

# THE DCSS PACKAGE

You can install the `dcss` package using pip: 

```bash
pip install dcss
```

The package source code is also hosted in this repo. If you like, you can browse it in `PATH TO PACKAGE SOURCE CODE`. 

# DATASETS

...

# QUESTIONS AND PROBLEM SETS

...

# INSTRUCTOR RESOURCES

... 
