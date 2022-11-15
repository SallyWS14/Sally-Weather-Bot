#import pprint
#from collections import defaultdict
import nltk
from nltk.corpus import wordnet 
syn = wordnet.synsets('weather')
#print(syn[0].definition())
#to print the definition of the weather

synonyms= []
for syn in wordnet.synsets('weather'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
<<<<<<< HEAD
    print(synonyms)
for syn in wordnet.synsets('atmosphere'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
    print(synonyms)
for syn in wordnet.synsets('climate'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
    print(synonyms)
for syn in wordnet.synsets('temperature'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
    print(synonyms)
=======
    print("Synonym of weather is"+ synonyms)
for syn in wordnet.synsets('atmosphere'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
    print("Synonym of atmosphere is"+ synonyms)
for syn in wordnet.synsets('climate'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
    print("Synonym of climate is" + synonyms)
for syn in wordnet.synsets('temperature'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
    print("Synonym of temperature is" + synonyms)
>>>>>>> f6c7c3ad2de931128c4aa54fa712b8e902de67e9

#def text_parser_synonym_antonym_extractor(weather):
   #from nltk.corpus import wordnet
   
   #for syn in wordnet.synsets("weather"):
          #for l in syn.lemmas():
              # synonyms.append(l.name())
               #if l.antonyms():
                   # antonyms.append(l.antonyms()[0].name())

   #print(set(synonyms)) 
  # print(set(antonyms))

#synonym_antonym_extractor(phrase="weather")
   # tokens = word_tokenize(text)
   # sentence = word_tokenize(sentence)
   # synonyms = defaultdict(list)
   # antonyms = defaultdict(list)
  #  for token in tokens:
      #  for syn in wn.synsets(token):
          #  for i in syn.lemmas():
                #synonyms.append(i.name())
                #print(f'{token} synonyms are: {i.name()}')
               # synonyms[token].append(i.name())
               # if i.antonyms():
                        #antonyms.append(i.antonyms()[0].name())
                        #print(f'{token} antonyms are: {i.antonyms()[0].name()}')
                        #antonyms[token].append(i.antonyms()[0].name())
    #for token in sentence:
      #  if token in synonyms[text]:
          #  print("Synonym for " + text+ ": ", token)
            # Run weather command
            
    
    #  pprint.pprint(dict(synonyms))
    #  pprint.pprint(dict(synonyms))
    #  synonym_output = pprint.pformat((dict(synonyms)))
    #  antonyms_output = pprint.pformat((dict(antonyms)))
    # with open(str(text[:5]) + ".txt", "a") as f:
    #     f.write("Starting of Synonyms of the Words from the Sentences: " + synonym_output + "\n")
    #     f.write("Starting of Antonyms of the Words from the Sentences: " + antonyms_output + "\n")
    #     f.close()

#text_parser_synonym_antonym_finder(sentence="What is the season today?", text="weather")
#print( wn.synsets('weather'));
# [Synset('weather.n.01'), Synset('climate.n.01'), Synset('season.n.03'), Synset('cad.n.01'),
# Synset('frank.n.02'), Synset('pawl.n.01'), Synset('andiron.n.01'), Synset('chase.v.01')]
#array_antonyms = []
#array_synonyms = []
#for vsyn in wordnet.synsets("weather"):
   #for l in vsyn.lemmas():
     #array_synonyms.append(l.name())
     #if l.antonyms():
     # array_antonyms.append(l.antonyms()[0].name())
      #print((array_synonyms))
      #print((array_antonyms))