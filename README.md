# Doing Computational Social Science

This repo contains all of the supplementary materials for [John McLevey (2021) *Doing Computational Social Science*, Sage, UK](https://uk.sagepub.com/en-gb/eur/doing-computational-social-science/book266031). 

## What's in here? 

1. [Datasets](#datasets)
2. [Instructions for downloading and installing the `dcss` Python package](#the-dcss-python-package)
3. [Pre-trained Language Models](#pre-trained-language-models)
4. [Questions and Problem Sets for Each Chapter](#questions-and-problem-sets-for-each-chapter)
5. [The DCSS Conda Environment](#dcss-conda-environment)
6. [High Resolution Figures](#high-resolution-figures)
7. [Supplementary Chapter Content](#supplementary-chapter-content)
8. [Practical Advice from Other Computational Social Scientists and Data Scientists](#practical-advice-from-other-computational-social-scientists-and-data-scientists)
9. [Citation Information](#citation-information)

## Datasets

The `datasets` directory contains all of the datasets that I use in the book, or in the accompanying problem sets (see below). They are:

- A filtered and subsetted of the Version 11 [Varieties of Democracy](https://www.v-dem.net/en/data/data/) data, released in 2021.
- The [Canadian Hansard](https://www.ourcommons.ca/documentviewer/en/35-2/house/hansard-index).
- The [British Hansard](https://hansard.parliament.uk).
- A variety of social network datasets collected by the [SocioPatterns Team](http://www.sociopatterns.org). 
- A variety of social network datasets collected by the [Copenhagen Networks Study Team](https://www.nature.com/articles/s41597-019-0325-x). 
- A "Freedom on the Net" dataset published by [Freedom House](https://freedomhouse.org/report/freedom-net) in 2020.
- A collection of small datasets related to campaign spending in the 2020 American General Election, as well as the [Cook Partisan Voting Index](https://en.wikipedia.org/wiki/Cook_Partisan_Voting_Index).
- Instructions on where to find the [European Values Survey](https://europeanvaluesstudy.eu) data. 
- A subset of the Russian Trolls dataset distributed by [fivethirtyeight](https://fivethirtyeight.com/features/why-were-sharing-3-million-russian-troll-tweets/), available in full [here](https://github.com/fivethirtyeight/russian-troll-tweets/).

Other datasets may be added over time, depending on what I am teaching in my own classes and using in the problem sets (below), and what others generously make available.

### The `dcss` Python package

All of these datasets can be downloaded and managed using [the `dcss` Python package](https://pypi.org/project/dcss/), which also contains a wide variety of utility functions used in the book and in the accompanying problem sets.

To install the `dcss` package, use `pip`.

```bash
pip install dcss
```

## Pre-trained Language Models

The book contains several chapters on contextual embeddings models, including how to train a variety of different types of embedding models over long time periods (e.g., over 100 years of large-scale text data). 

Not everyone has access to the computational resources needed to train models like these, and there are very good reasons (e.g., limiting energy use) to avoid re-training them needlessly. As such, my students and I have made all of the contextual embedding models we've trained for this book and for a few related projects available here. These models were trained in my lab using our own servers, and will be updated over time as new data is released.

The `pretrained_models` directory contains the models we trained for the Canadian Hansard and 120 years of academic scholarship on democracy and autocracy. 

## Questions and Problem Sets for Each Chapter

`questions_and_problem_sets` contains all of the questions and problems associated with each chapter in the book. These materials were developing collaboratively, with much of the work done by my PhD students [Pierson Browne](https://github.com/pbrowne88) and [Tyler Crick](https://github.com/tcrick) in the context of TAing the graduate and undergraduate versions of my Computational Social Science class at University of Waterloo in Winter and Spring 2021. These materials will grow and evolve over time (typically coinciding with semesters when I am teaching Computational Social Science).

## DCSS Conda Environment

The conda environment used in the book is available in `dcss_environment`. Once downloaded and set up, you can activate the environment from the command line: 

```bash
conda activate dcss
```

## High Resolution Figures

The `figures` directory contains every figure from the book as vector graphics (PDF), and in a few cases (e.g., screenshots of websites) high-resolution PNGs. 

## Supplementary Chapter Content

`supplementary_content` contains a number of notebooks that go beyond what is covered in the book. As of right now, it contains notebooks on collecting data from social media APIs (Twitter and Reddit) and on web scraping with Selenium. It also contains some additional content on analytical Bayesian inference that is intended to provide some additional clarity on the basic logic of Bayesian inference. If Bayesian inference is new to you, I suggest working through this example after working on Chapters 23 and 24. 

## Practical Advice from Other Computational Social Scientists and Data Scientists

`advice` is a collection of little bits of wisdom and practical advice from a number of computational social scientists and data scientists on a wide-variety of different topics. Many more will be added over time. 

## Citation Information

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
