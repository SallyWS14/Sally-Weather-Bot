import json
from pycorenlp import StanfordCoreNLP

#If user says "I would like to leave a review"

nlp = StanfordCoreNLP('http://localhost:9000')
userInput = "I like this chocolate. This chocolate is not good. The chocolate is delicious. Its a very tasty chocolate. This is so bad"

def createSentimentReply(usersReply):
    annot_doc = nlp.annotate(usersReply,
    properties={
       'annotators': 'sentiment',
       'outputFormat': 'json',
       'timeout': 1000,
    }) 
    annot_doc = json.loads(annot_doc)

    sentenceSentiments = []
    sallyReply = ""

    for sentence in annot_doc["sentences"]:
        sentenceSentiments.append(sentence["sentiment"])

    print(sentenceSentiments)

    stringSentiments = " ".join([str(x) for x in sentenceSentiments])

    #If the user reply is negative at all sally apologizes
    if ("Negative" in stringSentiments):
        sallyReply = "I'm sorry to hear that, what can we do to improve?"
    elif("Positive" in stringSentiments):
        sallyReply = "I'm happy to hear that. Let's talk again soon"
    elif ("Neutral" in stringSentiments):
        sallyReply = "Let's chat again soon"
        
    return sallyReply

    

print(createSentimentReply(userInput))

