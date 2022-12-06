#pip install wikipedia
import wikipedia

#Could you search {}?
def wikiResult(input):
   inputList = input.split(" ")
   length = len(inputList)
   lastWord = inputList[length-1] 
   print(lastWord)
   try: 
       return wikipedia.summary(lastWord, sentences=3)
   except wikipedia.exceptions.DisambiguationError:
        return "Try searching for something else, or try being a bit more specific"
   except wikipedia.exceptions.PageError:
       return "I couldn't find anything for that! Try something else"

print(wikiResult("Could you search clothes?"))
#print(wikiResult("Hat"))

#Could you show me something related to {word}
def findRelated(input):
    inputList = input.split(" ")
    length = len(inputList)
    lastWord = inputList[length-1]
   
    
    #Search last word
    list = wikipedia.search(lastWord, results=5)
    result = ""
    
    for word in list:
        if(word.lower() != lastWord.lower()):
            result = result + word + ", "
        
    return result

print(findRelated("Could you show me some searches related to winter"))