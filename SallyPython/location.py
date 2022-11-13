# pip install -U googemaps
# pip install pyspellchecker
# pip install nltk==3.5
# pip install numpy matplotlib
from datetime import datetime
from spellchecker import SpellChecker
import googlemaps
import json
import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")

# TODO: Named Entity Recognition, Spelling check

def extract_entity_names(t):
    entity_names = []
    if hasattr(t, "label") and t.label:
        if t.label() == "NE":
            entity_names.append(" ".join([child[0] for child in t]))
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
    return entities

def get_location():
    name = input("Enter your name: ")
    print("Hello", name)
    loc = input("Please input your location: ")
    print(loc)
    gmaps = googlemaps.Client(key="AIzaSyD1Ae_641pTLg2f_X2ElsRq21a5BYKNBlw")
    # Geocoding an address
    geocode_result = gmaps.geocode(get_entities(loc))
    print(
        "Latitude: "
        + str(geocode_result[0]["geometry"]["location"]["lat"])
        + "\nLongitude: "
        + str(geocode_result[0]["geometry"]["location"]["lng"])
    )
    used = False
    with open("data_location.json", "r") as infile:
        geo = json.load(infile)
        # print(geo)
    for names in geo:
        if names["name"] == name:
            print("You already have an account!")
            used = True
            break
    data = {
        "name": name,
        "location": get_entities(loc),
        "latitude": geocode_result[0]["geometry"]["location"]["lat"],
        "longitude": geocode_result[0]["geometry"]["location"]["lng"],
    }

    if used == False:
        geo.append(data)
    else:
        for names in geo:
            if names["name"] == name:
                geo.remove(names)
                geo.append(data)
                break

    json_obj = json.dumps(geo, indent=4)

    with open("data_location.json", "w") as f:
        f.write(json_obj)

    return data

print(get_location())
