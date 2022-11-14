#User: I don't understand could you re word that 
#Sally -> finds the longest word and replaces it with a synonym 

import random
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('omw-1.4')

sentence = "I recommend you wear"  

#Grab last sentence sally sent or ask user what they would like us to reword
#Takes sentence and returns the sentence reworded using synonym tool kit
def getRewordSentence(userSentence):
    if not len(userSentence):
        return "We can't reword an empty sentence"
    

    words = userSentence.split()
    longestWord = max(words, key=len)

    synonyms = []
    
    

    for syn in wordnet.synsets(longestWord):
        for l in syn.lemmas():
            synonyms.append(l.name())
    
    print(synonyms)
    
    #Remove same word from list
    uniqueSynonyms = set(synonyms)
    uniqueSynonyms.remove(longestWord)
    synonyms = list(uniqueSynonyms)
    print(synonyms)
    
    #If list is empty we can't reword it 
    if not len(synonyms):
        return "Sorry we can't re word that sentence"

    
    chosenSynonym = random.choice(synonyms)

    print(longestWord)
    print(chosenSynonym)

    #Replace the longest word
    index = words.index(longestWord)
    print(index)
    words[index] = chosenSynonym
    newSentence = " ".join(words)
        
    return newSentence
    

print(getRewordSentence(sentence))

