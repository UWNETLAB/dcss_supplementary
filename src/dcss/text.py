import re
import numpy as np
import os
import pandas as pd
from glob import glob

from collections import Counter

from itertools import chain, combinations

from gensim.models.phrases import Phrases, Phraser

from gensim.matutils import corpus2csc

import spacy
nlp = spacy.load('en_core_web_sm')

import seaborn as sns

import matplotlib.pyplot as plt

from spacy.training import Example

def bigram_process(texts, nlp=nlp, threshold=0.75, scoring='npmi', detokenize = True, n_process = 1):
    
    avail_cpu = os.cpu_count()
    if n_process > avail_cpu and avail_cpu > 1:
        n_process = avail_cpu -1
    elif avail_cpu == 1:
        n_process = avail_cpu
        
    sentences = []
    docs = []

    # sentence segmentation doesn't need POS tagging or lemmas.
    for doc in nlp.pipe(texts, disable=['tagger', 'lemmatizer', 'ner'], n_process=n_process):
        doc_sents = [[token.text.lower() for token in sent if token.text != '\n' and token.is_alpha]
                     for sent in doc.sents]
        # the flat list of tokenized sentences for training
        sentences.extend(doc_sents)
        # the nested list of documents, with a list of tokenized sentences in each
        docs.append(doc_sents)

    model = Phrases(sentences, min_count=1, threshold=threshold,
                    scoring=scoring)  # train the model
    # create more memory and processing efficient applicator of trained model
    bigrammer = Phraser(model) # bigrammer = model.freeze() # the same as above but for gensim 4.0 and higher
    bigrammed_list = [[bigrammer[sent] for sent in doc]
                      for doc in docs]  # apply the model to the sentences in each doc

    if detokenize == True:
        # rejoin the tokenized sentences into strings
        bigrammed_list = [[' '.join(sent) for sent in doc]
                          for doc in bigrammed_list]
        # rejoin the sentences to strings in each document
        bigrammed_list = [' '.join(doc) for doc in bigrammed_list]
    elif detokenize == "sentences":
        # rejoin the tokenized sentences into strings, returning a list of documents that are each a list of sentence strings
        bigrammed_list = [[' '.join(sent) for sent in doc]
                          for doc in bigrammed_list]
    else:
        # return a tokenized list of documents
        bigrammed_list = list(chain(*bigrammed_list))


    return model, bigrammed_list

    

def preprocess(texts, nlp=nlp, bigrams=False, detokenize=True, n_process = 1, custom_stops=[]):
    
    avail_cpu = os.cpu_count()
    if n_process > avail_cpu and avail_cpu > 1:
        n_process = avail_cpu -1
    elif avail_cpu == 1:
        n_process = avail_cpu
        
    processed_list = []    # list to store the final results
    # parts of speech to tell spaCy to keep
    allowed_postags = [92, 96, 84] # equivalent to: allowed_postags = ['NOUN', 'PROPN', 'ADJ']

    if bigrams == True:
        model, texts = bigram_process(texts, detokenize= True, n_process = n_process)

    for doc in nlp.pipe(texts, disable=['ner','parser'], n_process=n_process):

        processed = [token.lemma_ for token in doc if token.is_stop==False and len(token)>1
                    and token.pos in allowed_postags]

        if detokenize == True:
            processed = ' '.join(processed)
            processed_list.append(processed)
        else:
            processed_list.append(processed)

    if bigrams == True:
        return model, processed_list
    else:
        return processed_list






def see_semantic_context(search, text, window):
    keysearch = re.compile(search, re.IGNORECASE)
    contexts = []

    tokens = text.split()
    tokens = [t.lower() for t in tokens]
    token_count = Counter(tokens)

    for index in range(len(tokens)):
        if keysearch.match(tokens[index]):
            start = max(0, index-window)
            finish = min(len(tokens), index+window+1)
            left = " ".join(tokens[start:index])
            right = " ".join(tokens[index+1:finish])
            contexts.append("{} **{}** {}".format(left, tokens[index].upper(), right))

    return contexts, token_count[search]


def bow_to_df(gensim_corpus, gensim_vocab, tokens_as_columns=True):
    csr = corpus2csc(gensim_corpus)
    df = pd.DataFrame.sparse.from_spmatrix(csr)
    if tokens_as_columns is True:
        df = df.T
    df.columns = [v for k,v in gensim_vocab.items()]
    return df


def get_topic_words(vectorizer, model, n_top_words=10):
    """
    Given a vectorizer object and a fit model (e.g. LSA, NMF, LDA) from sklearn
    Gets the top words associated with each and returns them as a dict.
    """
    words = vectorizer.get_feature_names()

    topics = {}
    for i,topic in enumerate(model.components_):
        topics[i] = " ".join([words[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
    return topics

def get_topic_word_scores(df, n_words, topic_column, all_topics=False, as_tuples=True):
    df = df.sort_values(by=[topic_column], ascending = False)
    if all_topics is True:
        result = pd.concat([df.head(n_words), df.tail(n_words)]).round(4)
    else:
        result = pd.concat([df.head(n_words), df.tail(n_words)]).round(4)
        result = result[topic_column]
        if as_tuples is True:
            result = list(zip(result.index, result))
    return result 


def topic_to_dataframe(model, topic):
    topic = model.show_topic(topic, topn=30)
    df = pd.DataFrame(topic, columns = ['Word', 'Probability'])
    return df

def plot_topic(model, topic):
    df = topic_to_dataframe(model, topic)

    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='Probability', y='Word',
                    color='lightgray')

    for i in zip(df['Probability'], df['Word']):
        plt.text(x=i[0], y=i[1], s=i[1], fontsize=6)

    ax.set(yticklabels=[], ylabel='',
           xlabel='Probability',
           title=f'Topic {topic}')
    sns.despine(left=True)
    plt.show()







#CHAPTER 33 FUNCTIONS


def create_examples(text):

    examples = []
    for sent in nlp(text).sents:
        labels = {'entities':[]}
        sent_doc = sent.as_doc()
        for token in sent_doc:

            if token.text == "Cambridge" and token.nbor(1).text == "Analytica":
                label = (token.idx, token.nbor(1).idx + len(token.nbor(1)), "ORG")
                labels['entities'].append(label)

            if token.text == "Facebook":
                label = (token.idx, token.idx + len(token), "ORG")
                labels['entities'].append(label)

            if token.text == "Wylie":
                label = (token.idx, token.idx + len(token), "PERSON")
                labels['entities'].append(label)

        if len(labels['entities']) > 0:
            example_sent = nlp.make_doc(sent.text)
            examples.append(Example.from_dict(example_sent, labels))

    return examples


def entity_sentiment(doc, classifier, entity_names = [], entity_types = []):
    sentence_list = []
    entities_list = []
    sentiment_list = []
    sentiment_score_list = []
    sent_start_list = []
    sent_end_list = []

    for sent in doc.sents:
        entities = []
        for ent in sent.ents:
            if len(entity_names) > 0 and len(entity_types) > 0:
                for entity in entity_names:
                    if ent.text == entity and ent.label_ in entity_types:
                        entities.append(ent.text)
            elif len(entity_types) > 0:
                if ent.label_ in entity_types:
                    entities.append(ent.text)
            else:
                entities.append(ent.text)
        if len(entities) > 0:
                sentence_list.append(sent.text)
                sent_start_list.append(sent.start)
                sent_end_list.append(sent.end)
                entities_list.append(entities)
                sentiment = classifier(sent.text)
                sentiment_list.append(sentiment[0]['label'])
                sentiment_score_list.append(sentiment[0]['score'])

    df = pd.DataFrame()
    df['sentence'] = sentence_list
    df['entities'] = entities_list
    df['sentiment'] = sentiment_list
    df['sentiment_score'] = sentiment_score_list
    df['sent_signed'] = df['sentiment_score']
    df.loc[df['sentiment'] == 'NEGATIVE', 'sent_signed'] *= -1
    df['sentence_start'] = sent_start_list
    df['sentence_end'] = sent_end_list

    return df

def process_speeches_sentiment(df, nlp, sentiment):
    ent_types = ['GPE', 'ORG', 'PERSON']
    speakers = df['speakername'].tolist()
    speeches = df['speechtext'].tolist()
    speeches = [str(s).replace('\n',' ').replace('\r', '') for s in speeches]
    speeches_processed = [speech for speech in nlp.pipe(speeches)]
    print("Speeches processed, analyzing sentiment.")
    speaker_dfs = []
    for speaker, speech in zip(speakers, speeches_processed):
        temp_df = entity_sentiment(speech, sentiment, entity_types = ent_types)
        temp_df['speaker'] = speaker
        speaker_dfs.append(temp_df)

    new_df = pd.concat(speaker_dfs)

    return new_df


def create_speaker_edge_df(df, speaker):
    df['entities'] = df['entities'].map(set)
    df = df[df['entities'].map(len) > 1].copy()
    df = df[df['speaker'] == speaker].copy().reset_index(drop=True)

    temp = [[i,] + sorted(y) for i, x in df['entities'].items() for y in combinations(x,2)]
    temp_df = pd.DataFrame(temp, columns=['idx','source','target']).set_index('idx')
    df = temp_df.merge(df['sent_signed'], how='left', left_index=True, right_index=True).reset_index(drop=True)
    df.rename(columns={'sent_signed':'weight'}, inplace = True)

    df = df.sort_values(by='weight', ascending = False)

    return df

def shrink_sent_df(df):
    df = df.groupby(['source','target'])['weight'].agg(
        weight='count').reset_index()

    df = df.sort_values(by='weight', ascending = False)

    return df




def get_sentiment_blocks_df(G, state):

    try:
        import graph_tool as gt
    except:
        print("Error importing graph-tool. Make sure that it's correctly installed.")

    df = pd.DataFrame()
    ent_list = []
    block_list = []

    levels = state.get_levels()
    base_level = levels[0].get_blocks()

    for v in G.vertices():
        ent_list.append(G.vp['labels'][v])
        block_list.append(base_level[v])
    df['entity'] = ent_list
    df['block'] = block_list

    return df

def calculate_avg_block_sentiment(results_df, edges_df):

    block_df = results_df.groupby(['block'])['entity'].agg(entities=list).reset_index()

    block_df = block_df[block_df['entities'].map(len) > 1].copy()

    avg_sentiments = []

    ent_lists = block_df['entities'].tolist()

    for ent_list in ent_lists:
        sentiments = []
        sorted_combinations = [sorted(y) for y in combinations(ent_list,2)]
        for pair in sorted_combinations:
            sentiment = edges_df[(edges_df['source'] == pair[0]) & (edges_df['target'] == pair[1])].weight.mean()
            sentiments.append(sentiment)
        avg_sentiments.append(np.nanmean(sentiments))
    block_df['avg_sentiments'] = avg_sentiments

    return block_df
