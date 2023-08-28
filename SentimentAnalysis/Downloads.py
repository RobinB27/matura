# This file contains a list of commands which need to be run to install
# the necessarry features of the NLTK library that are needed for training
# the Sentiment Classifier. These downloads are also required for simply running
# the pretrained Classifier file already included in this project.

import nltk

# Punkt = Tokenizer used by NLTK
# Wordnet = Lexcial database for english that is used in Normalisation
# Averaged Perceptron Tagger = Determines context of word in sentence
# stopwords = list of words that are considered irrelevant to nlp, like 'that', 'as', etc.

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')