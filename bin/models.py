from collections import defaultdict

from nltk.stem import WordNetLemmatizer

import gensim
from gensim import corpora, models, similarities
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.ldamodel import LdaModel

import processtext

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def get_documents(transcripts):
    """
    Gets transcripts from FOX News, MSNBC, and combined as a dictionary.
    :param transcripts:
    :return: dict.
            The dictionary is of the format:

            {'MSNBC': msnbc_documents,
            'FOX': fox_documents,
            'combined': documents}

    """
    documents = []
    msnbc_documents = []
    fox_documents = []

    doc2network = dict()

    for i, tr in enumerate(transcripts):
        episode = processtext.Episode(tr)
        documents.append(episode.transcript)

        doc2network[i] = episode.network
        if episode.network == 'FOX':
            fox_documents.append(episode.transcript)
        elif episode.network == 'MSNBC':
            msnbc_documents.append(episode.transcript)
        else:
            print('NO Network assignment.')

    print(f"Number of episosdes, combined = {len(documents)}")
    print(f"Number of FOX episodes = {len(fox_documents)}")
    print(f"Number of MSNBC episodes = {len(msnbc_documents)}")

    return {'MSNBC': msnbc_documents,
            'FOX': fox_documents,
            'combined': documents,
            }, doc2network


def get_models_dict(documents_dict):

    stopwords = list(STOPWORDS)

    stopwords = stopwords + ['s', 't', 'thei', 'thi', 'hi', 'wa', 'ha', 'o',
                             'ar',
                             'right', 'sai', 'becaus', 'new', 'think', 'know',
                             'like',
                             'said', 'time', 'tonight', 'dont', 'people',
                             'peopl', 'want', 'todai', 'today', 'thing',
                             'look', 'let', 'come',
                             'wai', 'thats', 'u', 'got', 'im', 'year', 'going',
                             'lot',
                             'way', 'news', 'mean', 'president_trump',
                             'president',
                             'state', 'yes', 'theyre', 'youre',
                             'doe']  # 'didnt']

    models_dict = dict()

    lemmatizer = WordNetLemmatizer()

    for key, docs in documents_dict.items():
        print(key)

        num_topics = 3

        texts = [[lemmatizer.lemmatize(word) for word in document.split() if
                  lemmatizer.lemmatize(word) not in stopwords]
                 for document in docs]

        bigram = gensim.models.Phrases(texts)
        texts = [bigram[line] for line in texts]

        # remove words that appear only twice
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 2]
                 for text in texts]

        dictionary = corpora.Dictionary(texts)

        corpus = [dictionary.doc2bow(text) for text in texts]

        lda = LdaModel(corpus=corpus,
                       num_topics=num_topics,
                       minimum_probability=0.03,
                       id2word=dictionary,
                       passes=12)

        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=num_topics)
        index = similarities.MatrixSimilarity(lsi[corpus])

        models_dict[key] = {'model': lda,
                            'corpus': corpus,
                            'id2word': dictionary,
                            'lsi': lsi,
                            'index': index,
                            }

    return models_dict


def main():

    transcripts = processtext.main()
    documents_dict, doc2network = get_documents(transcripts)
    models_dict = get_models_dict(documents_dict)

    return models_dict, doc2network


if __name__ == "__main__":

    main()
