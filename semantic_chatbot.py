import spacy, random
nlp = spacy.load('en_core_web_lg')

from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('bert-base-nli-mean-tokens')


# Load Movielines & Conversations
movie_lines = {}
for line in open("./cornell movie-dialogs corpus/movie_lines.txt",
                 encoding="latin1"):
    line = line.strip()
    parts = line.split(" +++$+++ ")
    if len(parts) == 5:
        movie_lines[parts[0]] = parts[4]
    else:
        movie_lines[parts[0]] = ""

import json
responses = {}
for line in open("./cornell movie-dialogs corpus/movie_conversations.txt",
                 encoding="latin1"):
    line = line.strip()
    parts = line.split(" +++$+++ ")
    line_ids = json.loads(parts[3].replace("'", '"'))
    for first, second in zip(line_ids[:-1], line_ids[1:]):
        responses[first] = second


import numpy as np
def sentence_mean(nlp, s):
    if s == "":
        s = " "
    doc = nlp(s, disable=['tagger', 'parser'])
    return np.mean(np.array([w.vector for w in doc]), axis=0)
sentence_mean(nlp, "This... is a test.").shape


def sentence_vector_trnf(embedder, s):
    if s == "":
        s = " "
    sentence_embedding = embedder.encode([s])
    return sentence_embedding[0]

from simpleneighbors import SimpleNeighbors

response_sample = random.sample(list(responses.keys()), 10000)
#  Using GLOVE
nns = SimpleNeighbors(300)
for i, line_id in enumerate(response_sample):
    # show progress
    if i % 1000 == 0: print(i, line_id, movie_lines[line_id])
    line_text = movie_lines[line_id]
    summary_vector = sentence_mean(nlp, line_text)
    if np.any(summary_vector):
        nns.add_one(line_id, summary_vector)
nns.build()

#  Predictions Using Glove
sentence = "how are you doing?"
sentence = "How's the weather?"
sentence = "Did you eat today?"

picked = nns.nearest(sentence_mean(nlp, sentence), 5)[0]
response_line_id = responses[picked]

print("Your line:\n\t", sentence)
print("Most similar turn:\n\t", movie_lines[picked])
print("Response to most similar turn:\n\t", movie_lines[response_line_id])


#  Predictions Using Sentence Embedder
nns_trf = SimpleNeighbors(768)
for i, line_id in enumerate(response_sample):
    # show progress
    if i % 10 == 0: print(i, line_id, movie_lines[line_id])
    line_text = movie_lines[line_id]
    summary_vector = sentence_vector_trnf(embedder, line_text)
    if np.any(summary_vector):
        nns_trf.add_one(line_id, summary_vector)
nns_trf.build()

sentence = "how are you?"
sentence = "How's the weather?"
sentence = "Did you eat today?"

picked = nns_trf.nearest(sentence_vector_trnf(embedder, sentence), 5)[0]
response_line_id = responses[picked]

print("Your line:\n\t", sentence)
print("Most similar turn:\n\t", movie_lines[picked])
print("Response to most similar turn:\n\t", movie_lines[response_line_id])
