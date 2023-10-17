# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

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
from nltk.metrics.confusionmatrix import ConfusionMatrix

from SentimentAnalysis.FileHandling import FileHandling

import string, random, pickle

class Training:
    """
    Class providing methods for traing a Naive Bayes Classifier and saving it to the models folder.
    """

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

    def getClassifierInfo(classifier):
        """
        Generates a confusion matrix of a classifier using the last 30% of the dataset, which the classifier has not previously seen.\n
        Also prints the accuracy and most relevant features of the classifier.
        """
        
        test_data = Training.getSplitDataset()[1]
        
        # Make confusion matrix based on test data
        # From: https://www.nltk.org/api/nltk.metrics.confusionmatrix.html
        
        # reference is labels from testdata
        reference = [data[1] for data in test_data]
        # test is labels as classified by the classifier based on testdata
        test = [classifier.classify(data[0]) for data in test_data]
        matrix = ConfusionMatrix(reference, test)
        print(matrix)
        print("Accuracy is:", classify.accuracy(classifier, test_data))
        print(classifier.show_most_informative_features(10))
     
    def getDataset() -> list:
        """Prepares the dataset for use by the naive bayes classifier.

        Returns:
            list: cleaned dataset
        """
        stop_words = stopwords.words('english')
        dataset = FileHandling.readData()
        
        # Tokenize and prepare all data in the dataset
        for index, data in enumerate(dataset):
            # Extract and prepare data
            key = list(data[0].keys())[0]
            tokens = Training.remove_noise(word_tokenize(key), stop_words)
            
            # Reintegrate token into dataset
            replacement = {}
            for token in tokens:
                replacement[token] = True
            
            dataset[index][0] = replacement

        random.shuffle(dataset)
        
        return dataset
    
    def getSplitDataset() -> tuple[list, list]:
        """Returns training and test dataset

        Returns:
            tuple(list, list): Training dataset, test dataset
        """
        dataset = Training.getDataset()
        
        # Split dataset into Training and Test sets
        setMaxIndex = len(dataset) - 1
        testRatio = 0.7

        testAmount = int(setMaxIndex * testRatio)

        train_data = dataset[:testAmount]
        test_data = dataset[testAmount:]
        
        return train_data, test_data
           

    def trainClassifier():
        """Trains a Naive Bayes Classifier using the dataset

        Returns:
            Classifier: The trained classifier
        """
        train_data, test_data = Training.getSplitDataset()

        # Train classifier
        classifier = NaiveBayesClassifier.train(train_data)

        # Print useful information on classifier Training
        print("Accuracy is:", classify.accuracy(classifier, test_data))
        print(classifier.show_most_informative_features(10))

        # Manually entered fictional headline to test the Classifier with
        custom_Headline = "TSLA drops heavily after car crash in California"
        custom_tokens = Training.remove_noise(word_tokenize(custom_Headline))

        print(custom_Headline + "\n" + classifier.classify(dict([token, True] for token in custom_tokens)))
        
        return classifier

    def saveClassifier(classifier) -> None:
        """Saves a classifier to the models folder using pickle.dump()

        Args:
            classifier (classifier): Trained naive bayes classifier
        """
        path = "SentimentAnalysis/models/classifier.txt"
        with open(path, 'wb') as infile:
            pickle.dump(classifier, infile)

    def loadClassifier():
        """Returns the classifier currently saved in the models folder.

        Returns:
            classifier: Trained naive bayes classifier
        """
        path = "SentimentAnalysis/models/classifier.txt"
        classifier = None
        with open(path, "rb") as outfile:
            classifier = pickle.load(outfile)
            
        return classifier