import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import Tree


ex = 'I\'m arriving at Kelowna, how are you doing in Taipei?'

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def get_continuous_chunks(text, label):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == label:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        if current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    return continuous_chunk

sent = preprocess(ex)
print(sent)

print(get_continuous_chunks(ex, "GPE"))
