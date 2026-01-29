import string
import numpy as np

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punk_tab')

with open('requirements-3nfr-60fr.txt') as file:
  requirements_list = [line.strip() for line in file if line.strip()]
  
text = requirements_list[0]

bucket1 = []
bucket2 = []
bucket3 = []


operational = word_tokenize(requirements_list[0])
usability = word_tokenize(requirements_list[1])
security = word_tokenize(requirements_list[2])
cats = [operational, usability, security]


# Prepare stop words and custom filter words
stop_words = set(stopwords.words('english'))
custom_filter = {'operational', 'usability', 'security'}

full_cats = {}
for i, cat in enumerate(cats):
    tag = f'NFR{i+1}'
    cats[i] = [
        word for word in cat
        if not re.fullmatch(r'NFR\d+', word)
        and word.lower() not in stop_words
        and word.lower() not in custom_filter
        and word not in string.punctuation
    ]
    full_cats[tag] = cats[i]

print(full_cats)


# Process functional requirements (FR)
fr_cats = {}
for i, requirement in enumerate(requirements_list[3:]):
    tag = f"FR{i+1}"
    words = word_tokenize(requirement)
    filtered_requirement = [
        word for word in words
        if word.lower() not in stop_words
        and word.lower() not in custom_filter
        and word not in string.punctuation
    ]
    fr_cats[tag] = filtered_requirement

# Prepare texts
nfr_texts = [' '.join(words) for words in full_cats.values()]
fr_texts = [' '.join(words) for words in fr_cats.values()]
all_texts = nfr_texts + fr_texts

# Vectorize
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_texts)

# Compute similarities: NFRs vs FRs
n_nfr = len(nfr_texts)
n_fr = len(fr_texts)
similarities = cosine_similarity(tfidf_matrix[:n_nfr], tfidf_matrix[n_nfr:])

# similarities[i][j] is the similarity between NFR i and FR j
print(similarities)

nfr_labels = list(full_cats.keys())
fr_labels = list(fr_cats.keys())

# For each FR, find the NFR with the highest similarity
assignments = {}
for j, fr in enumerate(fr_labels):
  # Get the index of the NFR with the highest similarity for this FR
  best_nfr_idx = np.argmax(similarities[:, j])
  best_nfr = nfr_labels[best_nfr_idx]
  score = similarities[best_nfr_idx, j]
  assignments[fr] = (best_nfr, score)

# Print the assignments
for fr, (nfr, score) in assignments.items():
  print(f"{fr} is most similar to {nfr} (score: {score:.3f})")