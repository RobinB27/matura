# These are all necessary modules that are required to run the Classifier Training.
# NOT required for using the saved Classifier.

import nltk

# Punkt = Tokenizer used by NLTK
# Wordnet = Lexcial database for english that is used in Normalisation
# Averaged Perceptron Tagger = Determines context of word in sentence
# stopwords = list of words that are considered irrelevant to nlp, like 'that', 'as', etc.

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')