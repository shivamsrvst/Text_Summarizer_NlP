from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
import numpy as np
import sys

nlp = English()
nlp.add_pipe('sentencizer')


inputstring = sys.stdin.read()



doc = nlp(inputstring.replace("\n", ""))
sentences = [sent.text.strip() for sent in doc.sents]


#print("Senetence are: \n", sentences)

# Let's create an organizer which will store the sentence ordering to later reorganize the 
# scored sentences in their correct order
sentence_organizer = {k:v for v,k in enumerate(sentences)}

#print("Our sentence organizer: \n", sentence_organizer)

# Let's now create a tf-idf (Term frequnecy Inverse Document Frequency) model
tf_idf_vectorizer = TfidfVectorizer(min_df=2,  max_features=None, 
                                    strip_accents='unicode', 
                                    analyzer='word',
                                    token_pattern=r'\w{1,}',
                                    ngram_range=(1, 3), 
                                    use_idf=1,smooth_idf=1,
                                    sublinear_tf=1,
                                    stop_words = 'english')

# Passing our sentences treating each as one document to TF-IDF vectorizer
tf_idf_vectorizer.fit(sentences)

# Transforming our sentences to TF-IDF vectors
sentence_vectors = tf_idf_vectorizer.transform(sentences)

# Getting sentence scores for each sentences
sentence_scores = np.array(sentence_vectors.sum(axis=1)).ravel()

# Sanity checkup
#print(len(sentences) == len(sentence_scores))


# Getting top-n sentences
N = 3
top_n_sentences = [sentences[ind] for ind in np.argsort(sentence_scores, axis=0)[::-1][:N]]

# Let's now do the sentence ordering using our prebaked sentence_organizer
# Let's map the scored sentences with their indexes
mapped_top_n_sentences = [(sentence,sentence_organizer[sentence]) for sentence in top_n_sentences]
#print("Our top_n_sentence with their index: \n")
#for element in mapped_top_n_sentences:
    #print(element)

# Ordering our top-n sentences in their original ordering
mapped_top_n_sentences = sorted(mapped_top_n_sentences, key = lambda x: x[1])
ordered_scored_sentences = [element[0] for element in mapped_top_n_sentences]

# Our final summary
summary = " ".join(ordered_scored_sentences)

print("\nSummary:  ", summary)














