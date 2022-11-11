from textblob import Word
import re
# sentence = 'I am in Kelowna'
sentence = 'This is a sentencee to checkk!'

def check_word_spelling(word):
    word = Word(word)
    result = word.spellcheck()
    print(result[0])
    if word == result[0][0]:
        print(f'Spelling of "{word}" is correct!')
    else:
        print(f'Spelling of "{word}" is not correct!')
        print(f'Correct spelling of "{word}": "{result[0][0]}" (with {result[0][1]} confidence).')

def check_sentence_spelling(sentence):
    words = sentence.split()
    words = [word.lower() for word in words]
    words = [re.sub(r'[^A-Za-z0-9]+', '', word) for word in words]
    for word in words:
        check_word_spelling(word)

check_sentence_spelling(sentence)
