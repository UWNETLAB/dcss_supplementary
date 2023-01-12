import os
import pandas as pd
from glob import glob

from multiprocessing import Process
from functools import partial
from joblib import Parallel, delayed, cpu_count
from itertools import chain, combinations
from spacy.util import minibatch
from sklearn.preprocessing import LabelBinarizer

import pandas as pd



def read_directory_csvs(directory):
    """
    This function expects a posix path, for example as returned by one of the paths from the dcss paths module,
    like russian_troll_tweets_path if you run:

        from dcss.paths import russian_troll_tweets_path

    It returns a Pandas dataframe with all the various csv files concatenated into one object.
    """
    files = os.listdir(directory)
    files = [f for f in files if '.csv' in f]

    df = pd.concat((pd.read_csv(directory / file, encoding='utf-8', low_memory=False)
                    for file in files),
                   ignore_index=False)
    return df




def save_to_file(q, file_name):
    with open(file_name, 'w') as out:
        while True:
            val = q.get()
            if val is None: break
            for speech in val:
                out.write('\n'.join(speech))

def mp_disk(items, function, file_name, q, *args):
    cpu = cpu_count()
    batch_size = 32
    partitions = minibatch(items, size=batch_size)
    p = Process(target = save_to_file, args = (q, file_name))
    p.start()
    Parallel(n_jobs=cpu, max_nbytes=None)(delayed(function)(v, *args) for v in partitions) #executes the function on each batch
    q.put(None)
    p.join()


def list_files(rootdir, extension):
    """
    This utility function returns a list of paths to files of a given type, e.g. all csv files in a nested directory structure.
    """
    PATH = rootdir
    EXT = f'*.{extension}'
    files = [file for path, subdir, files in os.walk(PATH) for file in glob(os.path.join(path, EXT))]
    return files

class IterSents(object):
    """
    Gensim can operate on one file at a time to prevent memory issues.
    This class is a simple iterator that will provide the data to
    Word2Vec one at a time.
    """
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for line in open(self.filename):
            yield line.split()

def mp(items, function, *args, **keywords):
    """Applies a function to a list or dict of items, using multiprocessing.

    This is a convenience function for generalized multiprocessing of any
    function that deals with a list or dictionary of items. The functions
    passed to `mp` must accept the list of items to be processed at the end
    of their function call, with optional arguments first. *args can be any
    number of optional arguments accepted by the function that will be
    multiprocessed. On Windows, functions must be defined outside of the
    current python file and imported, to avoid infinite recursion.
    """
    if isinstance(items, list) == False:
        print("Items must be a list")
        return

    if len(items) < 1:
        print("List of items was empty")
        return

    cpu = cpu_count()

    batch_size = 32
    partitions = minibatch(items, size=batch_size)
    executor = Parallel(n_jobs=cpu,
                        backend="multiprocessing",
                        prefer="processes")
    do = delayed(partial(function, *args, **keywords))
    tasks = (do(batch) for batch in partitions)
    temp = executor(tasks)

    results = list(chain(*temp))

    return results


def sparse_groupby(groups, sparse_m, vocabulary):
    grouper = LabelBinarizer(sparse_output=True)
    grouped_m = grouper.fit_transform(groups).T.dot(sparse_m)

    df = pd.DataFrame.sparse.from_spmatrix(grouped_m)
    df.columns = vocabulary
    df.index = grouper.classes_

    return df
