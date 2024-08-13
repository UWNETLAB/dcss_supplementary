<a href="https://uk.sagepub.com/en-gb/eur/doing-computational-social-science/book266031"><img src="https://www.johnmclevey.com/images/DCSS.png" width="150"  align="right"/></a>

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

The DCSS environment comes with [Tiago Peixoto's](https://skewed.de/tiago) [`graph-tool`](http://graph-tool.skewed.de), which is challenging to install on Windows systems. If you are running into this issue and don't have access to a system running linux or macOS, then you can install a version of the DCSS environment that does not include `graph-tool`. That environment is `environment-windows-no-gt.yml`, and you can also find in the root directory. 

```bash
mamba env create -f environment-windows-no-gt.yml
mamba activate dcss
```

# THE DCSS ENVIRONMENT AND JUPYTER

Installing the DCSS environment only helpful if you can make use of it in your development environment of choice. Throughout the book, we assume that you're using Jupyter (lab/notebook) to follow along with the code examples. To run code in the DCSS environment from within Jupyter, perform the following steps:

1. Activate the DCSS environment using `conda activate dcss`
2. Register the DCSS environment as a Jupyter kernel using `python -m ipykernel install --user --name=dcss`

If, when attempting this, you receive an error about `ipykernel` not being installed, you can install it using `conda install ipykernel` while the DCSS environment is active. 

If successful, you should be able to select a `dcss` kernel from the 'Change Kernel' menu in Jupyter (typically found in the 'Kernel' dropdown at the top of the screen). 


# THE DCSS PACKAGE

You can install the `dcss` package using pip: 

```bash
pip install dcss
```

The package source code is also hosted in this repo. If you like, you can browse it in `PATH TO PACKAGE SOURCE CODE`. 

# DATASETS

The `data` directory contains all of the datasets that I use in the book, or in the accompanying problem sets (see below). However, some of these datasets are very large, are updated frequently, or are maintained by other people. In most cases, what you will find here are (1) large samples drawn from the original source datasets and (2) instructions on how to access the full datasets from their original sources. 

In `data/`, you will find: 

- A filtered and subsetted of the Version 11 [Varieties of Democracy](https://www.v-dem.net/en/data/data/) data, released in 2021.
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

Not everyone has access to the computational resources needed to train models like these, and there are very good reasons (e.g., limiting energy use) to avoid re-training them needlessly. As such, my students and I have made all of the contextual embedding models we've trained for this book and for a few related projects available here. These models were trained in my lab using our own servers, and will be updated over time as new data is released.

The `pretrained_models` directory contains the models we trained for the Canadian Hansard and 120 years of academic scholarship on democracy and autocracy (see McLevey, Crick, Browne, and Durant 2022 "[A new method for computational cultural cartography: From neural word embeddings to transformers and Bayesian mixture models](https://onlinelibrary.wiley.com/doi/abs/10.1111/cars.12378)"). 

# INSTRUCTOR RESOURCES

Access information coming soon. 

# OTHER RESOURCES

## High Resolution Figures

The `figures` directory contains every figure from the book as vector graphics (PDF), and in a few cases (e.g., screenshots of websites) high-resolution PNGs. 

## Supplementary Chapter Content

`supplementary_content` contains a number of notebooks that go beyond what is covered in the book. As of right now, it contains notebooks on collecting data from social media APIs (Twitter and Reddit) and on web scraping with Selenium. It also contains some additional content on analytical Bayesian inference that is intended to provide some additional clarity on the basic logic of Bayesian inference. If Bayesian inference is new to you, I suggest working through this example after working on Chapters 23 and 24. 

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

