(base) john@buffy:/fast-data/john/doing_computational_social_science$ tree
.
├── datasets
│   ├── british_hansards
│   ├── canadian_hansards
│   ├── copenhagen_networks_study
│   ├── elections
│   ├── european_values_survey
│   ├── freedom_house
│   ├── russian_trolls
│   ├── sociopatterns
│   └── varieties_of_democracy
├── figures_high_resolution
├── LICENSE
├── pretrained_models
│   ├── british_hansards
│   │   ├── complete
│   │   ├── decades
│   │   └── parties
│   ├── canadian_hansards
│   │   ├── complete
│   │   ├── decades
│   │   └── parties
│   └── democracy_autocracy
├── questions_and_problem_sets
│   ├── Chapter_01
│   ├── Chapter_02
│   ├── Chapter_03
│   ├── Chapter_04
│   ├── Chapter_05
│   ├── Chapter_06
│   ├── Chapter_07
│   ├── Chapter_08
│   ├── Chapter_09
│   ├── Chapter_10
│   ├── Chapter_11
│   ├── Chapter_12
│   ├── Chapter_13
│   ├── Chapter_14
│   ├── Chapter_15
<a href="https://uwaterloo.ca/networks-lab/"><img src="http://www.johnmclevey.com/assets/img/logo.png" width="125"  align="right" /></a>

# Learning Materials for *Doing Computational Social Science*

This repo contains all of the learning materials accompanying [John McLevey (2021) *Doing Computational Social Science*, Sage, UK.](johnmclevey.com) It includes:

## Datasets

The `datasets` directory contains all of the data that I used in the book, or in the scaffolded problem sets (see below). It includes:

- a filtered and subsetted of the Version 11 [Varieties of Democracy](https://www.v-dem.net/en/data/data/) data, released in 2021
- the Canada Hansards, DATE to DATE
- the British Hansards, DATE to DATE
- a variety of social network datasets collected by the [SocioPatterns Team](http://www.sociopatterns.org)
- a variety of social network datasets collected by the [Copenhagen Networks Study Team](https://www.nature.com/articles/s41597-019-0325-x)
- a dataset on global internet freedoms published by Freedom House
- a collection of small datasets related to the 2020 American General Election
- a subset of data from the European Values Survey
- a subset of the Russian Trolls dataset collected by CITE and distributed by [fivethirtyeight](https://fivethirtyeight.com/features/why-were-sharing-3-million-

## Pre-trained Models

The code used to train a variety of contextual embeddings models, as well as scripts to download the pre-trained models and load them in scripts or notebooks. These models were trained in my lab using our own servers, and will be updated over time as new data is released.

- pre-trained models for the Canadian Hansards data
  - (*i*) word2vec skip-gram, word2vec cbow, fastText, gloVe models for (*ii*) all years, by decade, by party, and by decade and party
- pre-trained modelsfor the British Hansards data
  - (*i*) word2vec skip-gram, word2vec cbow, fastText, gloVe models for (*ii*) all years, by decade, by party, and by decade and party
- for the full text of N journal articles, indexed by JSTOR, on democracies and autocracies
  - (*i*) word2vec skip-gram, word2vec cbow, fastText models for (*ii*) the full corpus and for each decade

## Questions and Scaffolded Problem Sets for Each Chapter

These are the materials that I use in my own Computational Social Science classes at the University of Waterloo. They are developed collaboratively, many lead by my PhD students [Pierson Browne](https://github.com/pbrowne88) and [Tyler Crick](https://github.com/tcrick) in the context of TAing my Winter and Spring 2021 offerings of INTEG 440 / SOC 440 (undergraduate) and INTEG 640 / SOC 719 (graduate) Computational Social Science classes at the University of Waterloo.

These materials will grow and evolve over time (typically coinciding with semesters when I am teaching Computational Social Science).

## Supplementary Chapter Content and Tutorials

Including:

- collecting data from social media platforms, including
  - Twitter
  - Reddit
README.md                                                                                                                                                                    1,1            Top
-- INSERT --
