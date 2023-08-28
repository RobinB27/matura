# This script implements functions used for training the Naive Bayes Classifier which is used for classifiying Head lines.
# This Script is a modified version of the script used in the tutorial linked here, which originally categorised Tweets binarily
# This modified version uses the Kaggle dataset 'FinancialPhraseBank' found in the same directory as this file and sorts News Headlines into 3 categories: Positive, Negative & Neutral
# Additionally, comments & Docstrings have been added to the whole file
# https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk#step-8-cleaning-up-the-code-optional

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import classify, NaiveBayesClassifier

from SentimentAnalysis.FileHandling import readData

import string, random, pickle

def remove_noise(tokens, stop_words = ()):
    """Removes noises from tokens: Stopwords are removed and words are converted into their lemmas

    Args:
        tokens (list): tokenised version of an example string
        stop_words (tuple, optional): List of stop words that should be excluded. Defaults to ().

    Returns:
        list: cleaned tokens
    """
    cleaned_tokens = []

    # pos_tag returns tuple (token, tag)
    for token, tag in pos_tag(tokens):

        if tag.startswith("NN"): pos = 'n'
        elif tag.startswith('VB'): pos = 'v'
        else: pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        # Remove punctuation and stop words, token is converted to lowercase
        if token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
            
    return cleaned_tokens


def trainClassifier():
    """Trains a Naive Bayes Classifier using the dataset

    Returns:
        Classifier: The trained classifier
    """

    stop_words = stopwords.words('english')
    dataset = readData()
    
    # Tokenize and prepare all data in the dataset
    for index, data in enumerate(dataset):
        # Extract and prepare data
        key = list(data[0].keys())[0]
        tokens = remove_noise(word_tokenize(key), stop_words)
        
        # Reintegrate token into dataset
        replacement = {}
        for token in tokens:
            replacement[token] = True
        
        dataset[index][0] = replacement

    random.shuffle(dataset)
    
    # Split dataset into Training and Test sets
    setMaxIndex = len(dataset) - 1
    testRatio = 0.7

    testAmount = int(setMaxIndex * testRatio)

    train_data = dataset[:testAmount]
    test_data = dataset[testAmount:]

    # Train classifier
    classifier = NaiveBayesClassifier.train(train_data)

    # Print useful information on classifier Training
    print("Accuracy is:", classify.accuracy(classifier, test_data))
    print(classifier.show_most_informative_features(10))

    # Manually entered headline to test the Classifier with
    custom_Headline = "insert Headline"
    custom_tokens = remove_noise(word_tokenize(custom_Headline))

    print(custom_Headline, classifier.classify(dict([token, True] for token in custom_tokens)))
    
    return classifier

def saveClassifier(classifier) -> None:
    path = "SentimentAnalysis/models/classifier.txt"
    with open(path, 'wb') as infile:
        pickle.dump(classifier, infile)

def loadClassifier():
    path = "SentimentAnalysis/models/classifier.txt"
    classifier = None
    with open(path, "rb") as outfile:
        classifier = pickle.load(outfile)
        
    return classifier