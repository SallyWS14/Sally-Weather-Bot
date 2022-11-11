# pip install textblob

from textblob import Word
import re

# sentence = 'I am in Kelowna'
# sentence = 'This is a sentencee to checkk!'
sentence = input("Please give me a sentence: ")


def check_word_spelling(word):
    word = Word(word)
    result = word.spellcheck()
    # print(result[0])
    if word == result[0][0]:
        return word
    else:
        return result[0][0]


def check_sentence_spelling(sentence):
    string = ""
    words = sentence.split()
    words = [word.lower() for word in words]
    words = [re.sub(r"[^A-Za-z0-9]+", "", word) for word in words]
    for word in words:
        string = string + check_word_spelling(word) + " "
    return string


print(check_sentence_spelling(sentence))
