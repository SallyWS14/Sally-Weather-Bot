import nltk

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def get_entities(line):
    sentences = nltk.sent_tokenize(line)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    entities = []
    for tree in chunked_sentences:
        entities.extend(extract_entity_names(tree))

    print(entities)

# with open('sample.txt', 'r') as f:
    # for line in f:
    #     sentences = nltk.sent_tokenize(line)
    #     tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    #     tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    #     chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    #     entities = []
    #     for tree in chunked_sentences:
    #         entities.extend(extract_entity_names(tree))

    #     print(entities)

inputstr = input("Please enter a sentence: ")
