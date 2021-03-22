<a href="https://uwaterloo.ca/networks-lab/"><img src="http://www.johnmclevey.com/assets/img/logo.png" width="125"  align="right" /></a>

# Doing Computational Social Science

This repo contains all of the learning materials accompanying [John McLevey (2021) *Doing Computational Social Science*, Sage, UK.](johnmclevey.com). 

## Datasets

The `datasets` directory contains all of the data that I used in the book, or in the scaffolded problem sets (see below). It includes:

- A filtered and subsetted of the Version 11 [Varieties of Democracy](https://www.v-dem.net/en/data/data/) data, released in 2021.
- The [Canadian Hansards](LINK), DATE to DATE.
- The [British Hansards](LINK), DATE to DATE.
- A variety of social network datasets collected by the [SocioPatterns Team](http://www.sociopatterns.org). 
- A variety of social network datasets collected by the [Copenhagen Networks Study Team](https://www.nature.com/articles/s41597-019-0325-x). 
- A "Freedom on the Net" dataset published by [Freedom House](https://freedomhouse.org/report/freedom-net) in 2020.
- A collection of small datasets related to campaign spending in the 2020 American General Election, as well as the [Cook Partisan Voting Index](https://en.wikipedia.org/wiki/Cook_Partisan_Voting_Index).
- A subset of data from the [European Values Survey](https://europeanvaluesstudy.eu). 
- A subset of the Russian Trolls dataset collected by CITE and distributed by [fivethirtyeight](https://fivethirtyeight.com/features/why-were-sharing-3-million-

Other datasets may be added overtime, depending on what I am teaching in my own classes and using in the problem sets (below), and what others generously make available.

## Pre-trained Models

The book contains several chapters on contextual embeddings models, including how to train a variety of different types of embedding models over long time periods (e.g., over 100 years of large-scale text data). 

Not everyone has access to the computational resources needed to train models like these, and there are very good reasons (e.g., limiting energy use) to avoid re-training them needlessly. As such, my students and I have made all of the contextual embedding models we've trained for this book and for a few related projects available here. These models were trained in my lab using our own servers, and will be updated over time as new data is released.

Since the models themselves are too large to host in this GitHub repo, we are hosting them elsewhere. The relevant directories here (in `pretrained_models`) contain (*i*) the code used to train each model, (*ii*) a script to download the files to your local machine, and (*iii*) a notebook demonstrating how to load the models into a script or Jupyter notebook after you have downloaded them. 

Altogether, we've trained and provided $n$ models here. The list below is an overview of those models and the data they are trained on. 

- Contextual embedding models trained on the Canadian Hansards data (`pretrained_models/canadian_hansards`).
    - word2vec skip-gram models ($n$ total): 
        - one model for the entire dataset
        - one model for each political party across all years
        - one model for each decade
        - one model for each political party in each decade 
    - word2vec CBOW models ($n$ total):
        - one model for the entire dataset
        - one model for each political party across all years
        - one model for each decade
        - one model for each political party in each decade 
    - fastText models ($n$ total):
        - one model for the entire dataset
        - one model for each political party across all years
        - one model for each decade
        - one model for each political party in each decade 
    - gloVe models ($n$ total):
        - one model for the entire dataset
        - one model for each political party across all years
        - one model for each decade
        - one model for each political party in each decade 
- Contextual embedding models trained on the British Hansards data (`pretrained_models/british_hansards`).
    - word2vec skip-gram models ($n$ total):
        - one model for the entire dataset
        - one model for each political party across all years
        - one model for each decade
        - one model for each political party in each decade 
    - word2vec CBOW models ($n$ total):
        - one model for the entire dataset
        - one model for each political party across all years
        - one model for each decade
        - one model for each political party in each decade 
    - fastText models ($n$ total):
        - one model for the entire dataset
        - one model for each political party across all years
        - one model for each decade
        - one model for each political party in each decade 
    - gloVe models ($n$ total):
        - one model for the entire dataset
        - one model for each political party across all years
        - one model for each decade
        - one model for each political party in each decade 
- Contextual embedding models trained on the full text of every publication (including books and book chapters) indexed by JSTOR that mentioned democracy, autocracy, authoritarian, dictatorship, or any variation on those words. As of March 2021, the dataset includes $n$ publications published between YYYY and YYYY. We are, unfortunately, not allowed to share the data these models were trained on, but you can go through the process of getting the same data directly from JSTOR.  (`pretrained_models/democracy_autocracy`)
    - word2vec skip-gram models ($n$ total):
        - one model for the entire dataset
        - one model for each decade
    - word2vec CBOW models ($n$ total):
        - one model for the entire dataset
        - one model for each decade
    - fastText models ($n$ total):
        - one model for the entire dataset
        - one model for each decade
    - gloVe models ($n$ total):
        - one model for the entire dataset
        - one model for each decade
 
## Questions and Scaffolded Problem Sets for Each Chapter

`questions_and_problem_sets` contains all of the questions and problems associated with each chapter in the book. These materials were developing collaboratively, with much of the work done by my PhD students [Pierson Browne](https://github.com/pbrowne88) and [Tyler Crick](https://github.com/tcrick) in the context of TAing the graduate and undergraduate versions of my Computational Social Science class at University of Waterloo in Winter and Spring 2021. These materials will grow and evolve over time (typically coinciding with semesters when I am teaching Computational Social Science).

## Supplementary Chapter Content and Tutorials

`supplementary_content` contains a number of notebooks that go beyond what is covered in the book. As of right now, it contains notebooks on collecting data from social media APIs (Twitter and Reddit) and on web scraping with Selenium. It also contains some additional content on analytical Bayesian inference that is intended to provide some additional clarity on the basic logic of Bayesian inference. If Bayesian inference is new to you, I suggest working through this example after working on Chapters 23 and 24. 

## Practical Advice from Other Computational Social Scientists and Data Scientists

`advice` is a collection of little bits of wisdom and practical advice from a number of computational social scientists and data scientists on a wide-variety of different topics. Many more will be added over time. 

- [Rochelle Terman]() on...
- [Alix Rule]() on...
- [Jillian Anderson]() on...
- [Deena Abul-Fottouh]() on ...
- [Pierson Browne]() on ...
- [Tyler Crick]() on ...
- [Sasha Graham]() on ...
- *with many others on the way!*

## Citation

For the book: 

```
@book{mclevey2021computational,
  title={Doing Computational Social Science},
  author={McLevey, John},
  year={2021},
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
