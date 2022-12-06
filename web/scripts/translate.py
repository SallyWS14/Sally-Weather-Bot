
import googletrans

#print(googletrans.LANGUAGES)
from googletrans import Translator
translator = Translator()

#text1 = "is it cold outside"
#text2 = "il fait froid dehors"
#text3 = "Hace frío afuera"

sentences = [ 'Cold', 'Warm','sunny','windy','rain','weather','snow','temperature']

result = translator.translate(sentences, src = 'en', dest = 'fr')

for trans in result:
    print(f'{trans.origin} -> {trans.text}')