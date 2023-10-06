# This file implements the getSentiment function which is used
# to access the pretrained Sentiment Classifier. The function takes a head line text
# and outputs the classification into the categories 'positive', 'negative' or 'neutral'
# which the classifier model has produced.

from SentimentAnalysis.Training import Training

from nltk.tokenize import word_tokenize

def getSentiment(text: str) -> str:
    """Returns the sentiment for a given String. Uses the Naive Bayes Classifier trained on the Kaggle Dataset, if saved.

    Args:
        text (str): News Headline to be analysed

    Raises:
        Exception: Raises Exception if the classifier could not be loaded

    Returns:
        str: Sentiment result. Either 'positive', 'negative' or 'neutral'
    """
    classifier = None
    try:
        classifier = Training.loadClassifier()
    except Exception:
        print("Classifier could not be loaded")
        raise Exception
    
    # Prepare text
    tokens = Training.remove_noise(word_tokenize(text))
    
    sentiment = classifier.classify(dict([token, True] for token in tokens))
    return sentiment