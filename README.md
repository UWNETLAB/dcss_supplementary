<a href="https://uk.sagepub.com/en-gb/eur/doing-computational-social-science/book266031"><img src="https://www.johnmclevey.com/images/DCSS.png" width="150"  align="right"/></a>

# DOING COMPUTATIONAL SOCIAL SCIENCE

Hello! This git repository contains the supplementary materials for [John McLevey (2021) *Doing Computational Social Science*, Sage, UK](https://uk.sagepub.com/en-gb/eur/doing-computational-social-science/book266031). A few small things have changed in this repo since the book was published. **If you are using this repo alongside the book, please take a moment to read this file carefully.** It will make it easier to access and use the resources you are looking for. If you run into any problems, please [file an issue](https://github.com/UWNETLAB/dcss_supplementary/issues). 

# THE DCSS VIRTUAL ENVIRONMENT

## Recommended setup in 2026: pixi

The pinned 2021-era conda environments below still document what the book was written against, but many of those pins are hard to install on current machines (especially Apple Silicon Macs). The simplest way to get a working environment today is [pixi](https://pixi.sh):

```bash
# install pixi once (see https://pixi.sh for other options)
curl -fsSL https://pixi.sh/install.sh | sh

# then, from the root of this repository:
pixi install
pixi run lab   # launches Jupyter Lab inside the environment
```

The `pixi.toml` manifest in this repository targets current macOS (Apple Silicon) and Linux, and installs modern versions of the full stack used in the book: pandas, scikit-learn, spaCy (with the small and medium English models), gensim, networkx, graph-tool, igraph/leidenalg, and PyMC 5 with ArviZ. The chapter and module notebooks in this repository have been updated to run against these modern versions. Where an updated library changed an API the book text shows (for example PyMC3 versus PyMC 5, or scikit-learn's `get_feature_names_out`), the notebooks note the difference inline.

Two heavyweight optional stacks live in separate pixi environments so the default environment stays small. `pixi install -e deep` adds TensorFlow and Keras for Chapter 23 and Module 10, and `pixi install -e trf` adds spacy-transformers, PyTorch, and the `en_core_web_trf` model for Chapter 32. Two book-era tools are not installable on a current stack at all: `twec` and `whatlies`, both unmaintained. Chapter 31 explains what they did and how to build a legacy environment if you want to reproduce that analysis.

## Book-era setup: conda

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

The easiest way to get Mamba is to install [Miniforge](https://github.com/conda-forge/miniforge), which ships both `conda` and `mamba`. (Note: the book and earlier versions of this README pointed to the "Mambaforge" installer, which was deprecated in 2024 and is no longer distributed. Use Miniforge3 instead.) In most cases, you should be able to just run the command below, which downloads the Miniforge install script (with `curl`) and then runs the installer.

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

Once you have Miniforge installed, you can use `mamba` in place of Conda. 

```bash
mamba env create -f environment.yml
```

and to activate, 

```bash
mamba activate dcss
```

## What to do if you are on a Windows system and are unable to install the environment

The DCSS environment comes with [Tiago Peixoto's](https://skewed.de/tiago) [`graph-tool`](http://graph-tool.skewed.de), which is challenging to install on Windows systems. If you are running into this issue and don't have access to a system running linux or macOS, then you can install a version of the DCSS environment that does not include `graph-tool`. That environment is `environment-windows-no-gt.yml`, and you can also find in the root directory. 

```bash
mamba env create -f environment-windows-no-gt.yml
mamba activate dcss
```

# THE DCSS ENVIRONMENT AND JUPYTER

Installing the DCSS environment is only helpful if you can make use of it in your development environment of choice. Throughout the book, we assume that you're using Jupyter (lab/notebook) to follow along with the code examples. To run code in the DCSS environment from within Jupyter, perform the following steps:

1. Activate the DCSS environment using `conda activate dcss`
2. Register the DCSS environment as a Jupyter kernel using `python -m ipykernel install --user --name=dcss`

If, when attempting this, you receive an error about `ipykernel` not being installed, you can install it using `conda install ipykernel` while the DCSS environment is active. 

If successful, you should be able to select a `dcss` kernel from the 'Change Kernel' menu in Jupyter (typically found in the 'Kernel' dropdown at the top of the screen). 


# THE DCSS PACKAGE

You can install the `dcss` package using pip: 

```bash
pip install dcss
```

The package source code is also hosted in this repo. If you like, you can browse it in [`src/dcss/`](src/dcss/).

> **Note (2026):** The published `dcss` package on PyPI (1.0.2) depends on `pymc3`, which has been superseded by [PyMC](https://www.pymc.io) (version 4 and later). `pip install dcss` into a modern Python environment may fail or pull in very old dependencies. To follow along with the book, install the pinned conda environment above, which already includes the compatible package versions. 

# DATASETS

The `data` directory contains all of the datasets that I use in the book, or in the accompanying problem sets (see below). However, some of these datasets are very large, are updated frequently, or are maintained by other people. In most cases, what you will find here are (1) large samples drawn from the original source datasets and (2) instructions on how to access the full datasets from their original sources. 

In `data/`, you will find: 

- A filtered and subsetted version of the Version 11 [Varieties of Democracy](https://www.v-dem.net/en/data/data/) data, released in 2021.
- A large sample from the [Canadian Hansard](https://www.ourcommons.ca/documentviewer/en/35-2/house/hansard-index).
- A large sample from the [British Hansard](https://hansard.parliament.uk).
- A variety of social network datasets collected by the [SocioPatterns Team](http://www.sociopatterns.org). 
- A variety of social network datasets collected by the [Copenhagen Networks Study Team](https://www.nature.com/articles/s41597-019-0325-x). 
- A "Freedom on the Net" dataset published by [Freedom House](https://freedomhouse.org/report/freedom-net) in 2020.
- A collection of small datasets related to campaign spending in the 2020 American General Election, as well as the [Cook Partisan Voting Index](https://en.wikipedia.org/wiki/Cook_Partisan_Voting_Index).
- Instructions on where to find the [European Values Survey](https://europeanvaluesstudy.eu) data, which is freely available but you have to register. 
- A sample of the Russian Trolls dataset distributed by [fivethirtyeight](https://fivethirtyeight.com/features/why-were-sharing-3-million-russian-troll-tweets/), available in full [here](https://github.com/fivethirtyeight/russian-troll-tweets/).

Other datasets may be added over time, depending on what I am teaching in my own classes and using in the problem sets (below), and what others generously make available.

# QUESTIONS AND PROBLEM SETS

> NOTE: More information coming soon. 

`questions_and_problem_sets` contains all of the questions and problems associated with each chapter in the book. These materials were developing collaboratively, with much of the work done by my PhD students [Pierson Browne](https://github.com/pbrowne88) and [Tyler Crick](https://github.com/tcrick) in the context of TAing the graduate and undergraduate versions of my Computational Social Science class at University of Waterloo in Winter and Spring 2021. These materials will grow and evolve over time (typically coinciding with semesters when I am teaching Computational Social Science).


# PRE-TRAINED EMBEDDING MODELS

The book contains several chapters on contextual embeddings models, including how to train a variety of different types of embedding models over long time periods (e.g., over 100 years of large-scale text data). 

Not everyone has access to the computational resources needed to train models like these, and there are very good reasons (e.g., limiting energy use) to avoid re-training them needlessly. My students and I trained a collection of embedding models for this book and for a few related projects in my lab using our own servers.

We previously distributed the models we trained for the Canadian Hansard and 120 years of academic scholarship on democracy and autocracy (see McLevey, Crick, Browne, and Durant 2022 "[A new method for computational cultural cartography: From neural word embeddings to transformers and Bayesian mixture models](https://onlinelibrary.wiley.com/doi/abs/10.1111/cars.12378)") via Git LFS in the `pretrained_models` directory. They were too large to keep in the repository, so that directory is currently an empty placeholder. If you need the pretrained models, please [file an issue](https://github.com/UWNETLAB/dcss_supplementary/issues) and we will arrange access. The notebooks that train models from scratch (e.g., Chapter 31) write their outputs to the `models/` directory in this repo. 

# INSTRUCTOR RESOURCES

Access information coming soon. 

# OTHER RESOURCES

## High Resolution Figures

The `figures` directory contains every figure from the book as vector graphics (PDF), and in a few cases (e.g., screenshots of websites) high-resolution PNGs. 

## Supplementary Chapter Content

`supplementary_content` is a placeholder for notebooks that go beyond what is covered in the book, including collecting data from social media APIs and web scraping with Selenium, as well as additional content on analytical Bayesian inference. **These notebooks are not yet available in this repository.** Please also note that the social media data collection landscape has changed substantially since the book was published: the free Twitter/X APIs used in the book era (including the academic research track) were discontinued in 2023, and Reddit moved to a paid API model in 2023. Treat any Twitter/X or Reddit data collection instructions from the book as historical, and check the current platform documentation before planning a data collection project. 

## Practical Advice from Other Computational Social Scientists and Data Scientists

`advice` is a collection of little bits of wisdom and practical advice from a number of computational social scientists and data scientists on a wide-variety of different topics. Many more will be added over time. 

# CITATION INFORMATION

For the book: 

```
@book{mclevey2022computational,
  title={Doing Computational Social Science},
  author={McLevey, John},
  year={2022},
  location={London, UK},
  publisher={Sage}
}
```

For this online supplement: 

```
@book{dcss,
  title={Doing Computational Social Science Online Supplement},
  author={McLevey, John and Browne, Pierson and Crick, Tyler and Graham, Sasha},
  year={2021},
  howpublished = "\url{https://github.com/UWNETLAB/doing_computational_social_science}"
}
```

