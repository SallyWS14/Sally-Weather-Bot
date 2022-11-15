#pip install nltk
#pip install numpy
#pip install pandas
#pip install scikit-learn

import nltk
nltk.download('vader_lexicon') 
from nltk.sentiment.vader import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer() 


def isNegOrIsPos(sentence):
    posValue = vader.polarity_scores(sentence)['pos']
    negValue = vader.polarity_scores(sentence)['neg']
    print('pos:')
    print(posValue)
    if (negValue > posValue):
        return 'Sorry if this is not what you wanted to hear'
    if (posValue < 0.25):
        return 'We hope you enjoy the alright weather'
    if (posValue > negValue and (posValue > 0.25)):
        return 'We hope you enjoy the nice weather'
        
